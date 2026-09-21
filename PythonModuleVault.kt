package com.amelia.modules

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.security.MessageDigest

/**
 * P3.9 is a source-vault stage, not a dynamic-code-execution stage.
 *
 * A picked .py file is copied to app-private storage only after an explicit
 * size, UTF-8, filename, and lexical-capability audit. It is never added to
 * sys.path, imported, or called by this app. The audit is intentionally not
 * described as a sandbox: it is a conservative staging policy that helps a
 * user review source before a future separately-authorized execution design.
 */
private const val MAX_MODULE_BYTES = 128 * 1024
private val MODULE_FILENAME = Regex("^[A-Za-z_][A-Za-z0-9_]*\\.py$")
private val MODULE_DIGEST = Regex("^[0-9a-f]{64}$")

data class ModuleRecord(
    val fileName: String,
    val digest: String,
    val byteCount: Int,
    val storedAtEpochMs: Long,
    val sourceStatus: String,
    val findings: List<String>
) {
    fun toJson(): JSONObject {
        val findingArray = JSONArray()
        findings.forEach { findingArray.put(it) }
        return JSONObject()
            .put("schema", "amelia-p3.9-module-vault-record-v1")
            .put("file_name", fileName)
            .put("digest", digest)
            .put("byte_count", byteCount)
            .put("stored_at_epoch_ms", storedAtEpochMs)
            .put("source_status", sourceStatus)
            .put("findings", findingArray)
    }

    companion object {
        fun fromJson(json: JSONObject): ModuleRecord? {
            if (json.optString("schema", "") != "amelia-p3.9-module-vault-record-v1") {
                return null
            }
            val findings = json.optJSONArray("findings")
            val list = buildList {
                if (findings != null) {
                    for (index in 0 until findings.length()) {
                        add(findings.optString(index, ""))
                    }
                }
            }.filter { it.isNotBlank() }
            return ModuleRecord(
                fileName = json.optString("file_name", ""),
                digest = json.optString("digest", ""),
                byteCount = json.optInt("byte_count", -1),
                storedAtEpochMs = json.optLong("stored_at_epoch_ms", 0L),
                sourceStatus = json.optString("source_status", ""),
                findings = list
            )
        }
    }
}

class ModuleRejectedException(val findings: List<String>) :
    IllegalArgumentException(findings.joinToString("; "))

object PythonModuleVault {
    private data class AuditRule(val label: String, val pattern: Regex)

    private val AUDIT_RULES = listOf(
        AuditRule("dynamic import", Regex("\\b(?:__import__|importlib\\s*\\.|reload\\s*\\()", RegexOption.IGNORE_CASE)),
        AuditRule("process or shell access", Regex("\\b(?:subprocess|os\\.system|popen\\s*\\(|system\\s*\\()", RegexOption.IGNORE_CASE)),
        AuditRule("network capability", Regex("\\b(?:socket|requests|urllib|http\\.client|httpx|aiohttp|ssl)\\b", RegexOption.IGNORE_CASE)),
        AuditRule("file or environment access", Regex("\\b(?:(?:import|from)\\s+(?:os|sys)\\b|open\\s*\\(|pathlib|shutil|tempfile|os\\.|sys\\.)", RegexOption.IGNORE_CASE)),
        AuditRule("native or Android bridge", Regex("\\b(?:ctypes|cffi|java\\.|android\\.|jnius|chaquopy)\\b", RegexOption.IGNORE_CASE)),
        AuditRule("runtime evaluation or reflection", Regex("\\b(?:exec\\s*\\(|eval\\s*\\(|compile\\s*\\(|globals\\s*\\(|locals\\s*\\(|getattr\\s*\\(|setattr\\s*\\()", RegexOption.IGNORE_CASE))
    )

    fun ingest(context: Context, selectedDisplayName: String, bytes: ByteArray): ModuleRecord {
        val fileName = selectedDisplayName
            .substringAfterLast('/')
            .substringAfterLast('\\')

        val findings = mutableListOf<String>()
        if (!MODULE_FILENAME.matches(fileName)) {
            findings += "Filename must be a simple Python module name ending in .py."
        }
        if (bytes.isEmpty()) {
            findings += "Uploaded file is empty."
        }
        if (bytes.size > MAX_MODULE_BYTES) {
            findings += "Uploaded file exceeds the ${MAX_MODULE_BYTES}-byte staged-module limit."
        }

        val source = try {
            Charsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(bytes))
                .toString()
        } catch (_: Exception) {
            findings += "Uploaded file is not strict UTF-8 source."
            ""
        }

        if (source.indexOf('\u0000') >= 0) {
            findings += "Uploaded source contains a NUL character."
        }
        if (source.isNotBlank()) {
            AUDIT_RULES.forEach { rule ->
                if (rule.pattern.containsMatchIn(source)) {
                    findings += "Source policy rejected ${rule.label}."
                }
            }
        }

        if (findings.isNotEmpty()) throw ModuleRejectedException(findings.distinct())

        val digest = sha256Hex(bytes)
        val root = vaultRoot(context)
        val moduleDirectory = File(root, digest)
        require(moduleDirectory.mkdirs() || moduleDirectory.isDirectory) {
            "Unable to create the app-private module directory."
        }
        require(moduleDirectory.canonicalPath.startsWith(root.canonicalPath + File.separator)) {
            "Refusing an unsafe module storage path."
        }

        val sourceFile = File(moduleDirectory, fileName)
        require(sourceFile.canonicalPath.startsWith(moduleDirectory.canonicalPath + File.separator)) {
            "Refusing an unsafe module filename."
        }
        sourceFile.writeBytes(bytes)

        val record = ModuleRecord(
            fileName = fileName,
            digest = digest,
            byteCount = bytes.size,
            storedAtEpochMs = System.currentTimeMillis(),
            sourceStatus = "STAGED_NOT_IMPORTED",
            findings = listOf(
                "Copied to app-private storage.",
                "Source policy audit passed.",
                "Not added to Python's import path and not executed."
            )
        )
        File(moduleDirectory, "record.json").writeText(record.toJson().toString(), Charsets.UTF_8)
        return record
    }

    fun list(context: Context): List<ModuleRecord> {
        val root = vaultRoot(context)
        val directories = root.listFiles()?.filter { it.isDirectory } ?: emptyList()
        return directories.mapNotNull { directory ->
            if (!MODULE_DIGEST.matches(directory.name)) return@mapNotNull null
            try {
                val recordFile = File(directory, "record.json")
                if (!recordFile.isFile) return@mapNotNull null
                ModuleRecord.fromJson(JSONObject(recordFile.readText(Charsets.UTF_8)))
            } catch (_: Exception) {
                null
            }
        }.sortedByDescending { it.storedAtEpochMs }
    }

    private fun vaultRoot(context: Context): File {
        val root = File(context.filesDir, "p39-module-vault")
        require(root.mkdirs() || root.isDirectory) {
            "Unable to create the app-private module vault."
        }
        return root
    }

    private fun sha256Hex(bytes: ByteArray): String =
        MessageDigest.getInstance("SHA-256")
            .digest(bytes)
            .joinToString("") { "%02x".format(it) }
}
