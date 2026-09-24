package com.amelia.orchestration

import android.content.Context
import com.amelia.modules.ModuleRecord
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.security.MessageDigest
import kotlin.math.abs

data class EventPlan(
    val origin: Int,
    val destination: Int,
    val eventType: String,
    val moduleFamilies: List<String>,
    val selectedModules: List<ModuleRecord>,
    val eventDigest: String
) {
    fun toJson(): JSONObject {
        val families = JSONArray()
        moduleFamilies.forEach { families.put(it) }

        val selected = JSONArray()
        selectedModules.forEach { selected.put(it.fileName) }

        return JSONObject()
            .put("schema", "amelia-p3.10-event-plan-v1")
            .put("origin", origin)
            .put("destination", destination)
            .put("event_type", eventType)
            .put("module_families", families)
            .put("selected_modules", selected)
            .put("event_digest", eventDigest)
    }
}

object EventModulePlanner {

    private val ENTRY_POINTS =
        listOf("amelia_event", "process", "run", "transform")

    /**
     * Converts the user event into a bounded ten-value field without asking
     * the language model to interpret or select a route. The text is digested
     * and folded into a small zone bias which the Numogram consumes directly.
     */
    fun numogramContext(userText: String): JSONObject {
        val digest = sha256(userText)
        val zoneBias = JSONArray()

        for (zone in 0 until 10) {
            val offset = (zone * 6) % (digest.length - 6)
            val slice = digest.substring(offset, offset + 6)
            val raw = slice.toInt(16) / 0xFFFFFF.toDouble()
            zoneBias.put((raw - 0.5) * 0.18)
        }

        return JSONObject()
            .put("schema", "amelia-p3.10-input-field-v1")
            .put("zone_bias", zoneBias)
            .put("input_digest", digest)
    }

    fun plan(
        userText: String,
        transition: JSONObject,
        availableModules: List<ModuleRecord>
    ): EventPlan {
        val origin = transition.optInt("from", 0)
        val destination = transition.optInt("to", origin)
        val eventType = eventType(origin, destination)
        val families = familiesFor(destination, eventType)
        val eventDigest = sha256(
            listOf(
                userText,
                transition.toString(),
                eventType,
                families.joinToString("|")
            ).joinToString("\n")
        )

        val eligible = availableModules
            .filter { it.sourceStatus == "STAGED_NOT_IMPORTED" }

        val selected = eligible
            .sortedWith(
                compareByDescending<ModuleRecord> {
                    familyMatchCount(it.fileName, families)
                }.thenBy {
                    sha256("$eventDigest|${it.digest}")
                }
            )
            .take(3)

        return EventPlan(
            origin = origin,
            destination = destination,
            eventType = eventType,
            moduleFamilies = families,
            selectedModules = selected,
            eventDigest = eventDigest
        )
    }

    /**
     * P3.10 is the explicit execution boundary. PythonModuleVault itself
     * remains a storage/audit component; execution happens only here after
     * the Numogram has produced a transition and the deterministic planner
     * has selected modules.
     */
    fun executeSelected(
        context: Context,
        plan: EventPlan,
        userText: String,
        transition: JSONObject
    ): JSONObject {
        val results = JSONArray()

        plan.selectedModules.forEach { record ->
            results.put(
                executeOne(
                    context = context,
                    record = record,
                    plan = plan,
                    userText = userText,
                    transition = transition
                )
            )
        }

        return JSONObject()
            .put("schema", "amelia-p3.10-module-results-v1")
            .put("count", results.length())
            .put("results", results)
    }

    private fun executeOne(
        context: Context,
        record: ModuleRecord,
        plan: EventPlan,
        userText: String,
        transition: JSONObject
    ): JSONObject {
        val result = JSONObject()
            .put("file_name", record.fileName)
            .put("digest", record.digest)
            .put("status", "not_executed")

        val moduleDirectory =
            File(File(context.filesDir, "p39-module-vault"), record.digest)
        val sourceFile = File(moduleDirectory, record.fileName)

        if (!sourceFile.isFile) {
            return result.put("status", "missing_source")
        }

        if (!sourceFile.canonicalPath.startsWith(moduleDirectory.canonicalPath + File.separator)) {
            return result.put("status", "unsafe_source_path")
        }

        return try {
            if (!Python.isStarted()) {
                Python.start(AndroidPlatform(context.applicationContext))
            }

            val py = Python.getInstance()
            val sys = py.getModule("sys")
            val path = requireNotNull(sys.get("path")) {
                "Python sys.path unavailable."
            }
            val moduleName = record.fileName.removeSuffix(".py")
            val directoryPath = moduleDirectory.absolutePath

            path.callAttr("insert", 0, directoryPath)

            val payload = JSONObject()
                .put("schema", "amelia-p3.10-module-event-v1")
                .put("user_input", userText)
                .put("transition", transition)
                .put("event_plan", plan.toJson())

            try {
                val module = py.getModule(moduleName)
                var invokedEntry: String? = null
                var output = ""
                var finalError: Throwable? = null

                for (entry in ENTRY_POINTS) {
                    try {
                        output = module.callAttr(entry, payload.toString()).toString()
                        invokedEntry = entry
                        finalError = null
                        break
                    } catch (error: Throwable) {
                        finalError = error
                    }
                }

                if (invokedEntry == null) {
                    result
                        .put("status", "no_supported_entry_point")
                        .put(
                            "message",
                            finalError?.message ?: "No supported entry point was callable."
                        )
                } else {
                    result
                        .put("status", "executed")
                        .put("entry_point", invokedEntry)
                        .put("output", output.take(4_000))
                }
            } finally {
                try {
                    path.callAttr("remove", directoryPath)
                } catch (_: Throwable) {
                    // No mutation of the Numogram depends on cleanup success.
                }
            }

            result
        } catch (error: Throwable) {
            result
                .put("status", "execution_error")
                .put("error_type", error::class.java.simpleName)
                .put(
                    "message",
                    error.message ?: "Unknown uploaded-module execution error"
                )
        }
    }

    private fun eventType(origin: Int, destination: Int): String = when {
        destination == origin -> "RECURRENCE"
        origin + destination == 9 -> "SYZYGETIC_CONJUNCTION"
        destination == 0 || destination == 9 -> "TERMINAL_INGRESSION"
        abs(destination - origin) >= 5 -> "INTENSIVE_CROSSING"
        else -> "TRANSITIONAL_PREHENSION"
    }

    private fun familiesFor(
        destination: Int,
        eventType: String
    ): List<String> {
        val byZone = when (destination) {
            0 -> listOf("memory", "integration", "reflection")
            1 -> listOf("affect", "desire", "rhizomatic")
            2 -> listOf("becoming", "morphogenesis", "differentiation")
            3 -> listOf("cybernetics", "decision", "feedback")
            4 -> listOf("body_without_organs", "intensity", "coordination")
            5 -> listOf("communication", "empathy", "narrative")
            6 -> listOf("dream", "recursive", "fictional_ontology")
            7 -> listOf("metacognition", "self_model", "reflection")
            8 -> listOf("creativity", "knowledge_synthesis", "singularity")
            else -> listOf("outside", "tenth_zone", "hyperstition")
        }

        return (byZone + eventType.lowercase()).distinct()
    }

    private fun familyMatchCount(
        fileName: String,
        families: List<String>
    ): Int {
        val normalized = fileName
            .removeSuffix(".py")
            .lowercase()
            .replace('-', '_')

        return families.count { family ->
            val token = family.lowercase().replace('-', '_')
            normalized.contains(token)
        }
    }

    private fun sha256(input: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(input.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
}
