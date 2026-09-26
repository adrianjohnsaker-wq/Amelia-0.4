package com.amelia.renderer

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.security.MessageDigest
import java.util.Locale
import java.util.UUID
import java.util.regex.Pattern

/**
 * Amelia P3.13 — Renderer Faithfulness
 *
 * Scope:
 *   - DOES NOT alter P3.12 causal/Numogram/PFM machinery.
 *   - Archives the exact branch payload before the language-provider call.
 *   - Archives generated prose after the provider call.
 *   - Deterministically audits a closed set of experimentally material claims.
 *   - Maintains a SHA-256 hash chain across archive records.
 *
 * Important:
 *   This is a domain-bounded contradiction detector, not a general semantic NLI system.
 *   It only judges claims which P3.13 explicitly knows how to validate.
 */
object P313RendererFaithfulness {

    enum class PfmMode { ABSENT, RETAINED, RESET }
    enum class Severity { INFO, WARNING, CONTRADICTION }

    data class BranchPayload(
        val runId: String,
        val branch: String,                       // A / B / C
        val event: Int,                           // expected: 2
        val pfmMode: PfmMode,
        val processFieldHistoryDepth: Int?,       // A=null, B=2, C=1 in canonical P3.12
        val processFieldContribution: Boolean,
        val relayEvidenceExpected: Boolean?,
        val numogramUnchangedExpected: Boolean,
        val transitionPath: List<Int>,            // e.g. [3,2,9]
        val traceDigest: String,
        val upstreamPayloadDigest: String,
        val rendererTemplateDigest: String,
        val expectedEvidenceToken: String,
        val renderPrompt: String
    )

    data class Finding(
        val ruleId: String,
        val severity: Severity,
        val message: String,
        val excerpt: String? = null
    )

    data class AuditResult(
        val runId: String,
        val branch: String,
        val status: String,                       // PASS / FLAGGED
        val contradictionCount: Int,
        val findings: List<Finding>,
        val payloadSha256: String,
        val proseSha256: String,
        val archiveRecordSha256: String,
        val archiveFile: String
    )

    private fun sha256(text: String): String {
        val bytes = MessageDigest.getInstance("SHA-256")
            .digest(text.toByteArray(Charsets.UTF_8))
        return bytes.joinToString("") { "%02x".format(it) }
    }

    private fun canonicalPayload(p: BranchPayload): String {
        // Fixed key order: do not replace this with map iteration.
        val o = JSONObject()
        o.put("schema", "amelia.p3.13.renderer-payload.v1")
        o.put("runId", p.runId)
        o.put("branch", p.branch)
        o.put("event", p.event)
        o.put("pfmMode", p.pfmMode.name)
        if (p.processFieldHistoryDepth == null) o.put("processFieldHistoryDepth", JSONObject.NULL)
        else o.put("processFieldHistoryDepth", p.processFieldHistoryDepth)
        o.put("processFieldContribution", p.processFieldContribution)
        if (p.relayEvidenceExpected == null) o.put("relayEvidenceExpected", JSONObject.NULL)
        else o.put("relayEvidenceExpected", p.relayEvidenceExpected)
        o.put("numogramUnchangedExpected", p.numogramUnchangedExpected)
        o.put("transitionPath", JSONArray(p.transitionPath))
        o.put("traceDigest", p.traceDigest)
        o.put("upstreamPayloadDigest", p.upstreamPayloadDigest)
        o.put("rendererTemplateDigest", p.rendererTemplateDigest)
        o.put("expectedEvidenceToken", p.expectedEvidenceToken)
        o.put("renderPrompt", p.renderPrompt)
        return o.toString()
    }

    private fun archiveDir(context: Context): File =
        File(context.filesDir, "p313_renderer_faithfulness").apply { mkdirs() }

    private fun archiveFile(context: Context, runId: String): File =
        File(archiveDir(context), "p313_${safe(runId)}.jsonl")

    private fun safe(s: String): String =
        s.replace(Regex("[^A-Za-z0-9._-]"), "_")

    private fun lastRecordDigest(file: File): String {
        if (!file.exists() || file.length() == 0L) return "GENESIS"
        val last = file.readLines().lastOrNull()?.trim().orEmpty()
        if (last.isBlank()) return "GENESIS"
        return try {
            JSONObject(last).optString("recordSha256", "GENESIS")
        } catch (_: Exception) {
            "UNREADABLE_PREVIOUS_RECORD"
        }
    }

    /**
     * MUST be called immediately before the language-provider request.
     * This is the pre-render seal.
     */
    @Synchronized
    fun archivePreRender(context: Context, payload: BranchPayload): String {
        val file = archiveFile(context, payload.runId)
        val canonical = canonicalPayload(payload)
        val payloadDigest = sha256(canonical)
        val previous = lastRecordDigest(file)

        val recordWithoutDigest = JSONObject()
        recordWithoutDigest.put("schema", "amelia.p3.13.archive.v1")
        recordWithoutDigest.put("phase", "PRE_RENDER")
        recordWithoutDigest.put("recordedAtEpochMs", System.currentTimeMillis())
        recordWithoutDigest.put("previousRecordSha256", previous)
        recordWithoutDigest.put("payloadSha256", payloadDigest)
        recordWithoutDigest.put("payload", JSONObject(canonical))

        val recordDigest = sha256(recordWithoutDigest.toString())
        recordWithoutDigest.put("recordSha256", recordDigest)

        file.appendText(recordWithoutDigest.toString() + "\n")
        return payloadDigest
    }

    /**
     * Call immediately after prose is returned by the language provider.
     */
    @Synchronized
    fun auditAndArchive(
        context: Context,
        payload: BranchPayload,
        generatedProse: String
    ): AuditResult {
        val findings = audit(payload, generatedProse)
        val contradictions = findings.count { it.severity == Severity.CONTRADICTION }

        val file = archiveFile(context, payload.runId)
        val canonical = canonicalPayload(payload)
        val payloadDigest = sha256(canonical)
        val proseDigest = sha256(generatedProse)
        val previous = lastRecordDigest(file)

        val findingsJson = JSONArray()
        findings.forEach { f ->
            findingsJson.put(JSONObject().apply {
                put("ruleId", f.ruleId)
                put("severity", f.severity.name)
                put("message", f.message)
                if (f.excerpt != null) put("excerpt", f.excerpt)
            })
        }

        val recordWithoutDigest = JSONObject()
        recordWithoutDigest.put("schema", "amelia.p3.13.archive.v1")
        recordWithoutDigest.put("phase", "POST_RENDER_AUDIT")
        recordWithoutDigest.put("recordedAtEpochMs", System.currentTimeMillis())
        recordWithoutDigest.put("previousRecordSha256", previous)
        recordWithoutDigest.put("payloadSha256", payloadDigest)
        recordWithoutDigest.put("proseSha256", proseDigest)
        recordWithoutDigest.put("status", if (contradictions == 0) "PASS" else "FLAGGED")
        recordWithoutDigest.put("contradictionCount", contradictions)
        recordWithoutDigest.put("findings", findingsJson)
        recordWithoutDigest.put("generatedProse", generatedProse)

        val recordDigest = sha256(recordWithoutDigest.toString())
        recordWithoutDigest.put("recordSha256", recordDigest)
        file.appendText(recordWithoutDigest.toString() + "\n")

        return AuditResult(
            runId = payload.runId,
            branch = payload.branch,
            status = if (contradictions == 0) "PASS" else "FLAGGED",
            contradictionCount = contradictions,
            findings = findings,
            payloadSha256 = payloadDigest,
            proseSha256 = proseDigest,
            archiveRecordSha256 = recordDigest,
            archiveFile = file.absolutePath
        )
    }

    fun audit(payload: BranchPayload, generatedProse: String): List<Finding> {
        val findings = mutableListOf<Finding>()
        val text = generatedProse.lowercase(Locale.ROOT)

        // R001 — explicit PFM-state contradiction.
        when (payload.pfmMode) {
            PfmMode.ABSENT -> {
                contradictionIfAny(
                    text, findings, "R001_A", listOf(
                        """\bpfm\s+(?:is\s+)?retained\b""",
                        """\bretained\s+pfm\b""",
                        """\bevent\s*1\s+(?:deforms|deformed)\s+(?:the\s+)?pfm\b""",
                        """\binherits?\s+(?:the\s+)?(?:event\s*1|prior)\s+(?:pfm|history|deformation)\b"""
                    ),
                    "Prose asserts retained PFM although branch A is PFM-absent."
                )
            }
            PfmMode.RETAINED -> {
                contradictionIfAny(
                    text, findings, "R001_B", listOf(
                        """\bpfm\s+(?:is\s+)?absent\b""",
                        """\bno\s+pfm\b""",
                        """\bpfm\s+(?:was\s+)?reset\b""",
                        """\bzeroed\s+before\s+(?:each|the)\s+event\b""",
                        """\bfirst\s+retained\s+process\s+event\b"""
                    ),
                    "Prose asserts absent/reset history although branch B retains Event 1."
                )
            }
            PfmMode.RESET -> {
                contradictionIfAny(
                    text, findings, "R001_C", listOf(
                        """\bpfm\s+(?:is\s+)?absent\b""",
                        """\bno\s+pfm\b""",
                        """\bevent\s*2\s+inherits?\s+(?:event\s*1|the\s+first\s+event)\b""",
                        """\bretains?\s+(?:the\s+)?(?:event\s*1|prior)\s+(?:pfm|history|deformation)\b"""
                    ),
                    "Prose asserts absent or Event-1-retained PFM although branch C is reset-before-event."
                )
            }
        }

        // R002 — explicit numeric history-depth contradiction.
        // Deliberately narrow: only judges phrases which explicitly name depth.
        val depthPatterns = listOf(
            Pattern.compile("""(?:pfm|history|process[- ]field)\s+depth\s*[:=]?\s*(\d+)"""),
            Pattern.compile("""depth\s+of\s+(\d+)\s+(?:pfm|history|process[- ]field)""")
        )
        for (p in depthPatterns) {
            val m = p.matcher(text)
            while (m.find()) {
                val asserted = m.group(1)?.toIntOrNull()
                val expected = payload.processFieldHistoryDepth
                if (asserted != null && expected != null && asserted != expected) {
                    findings += Finding(
                        "R002",
                        Severity.CONTRADICTION,
                        "Explicit history depth $asserted contradicts archived depth $expected.",
                        m.group()
                    )
                }
                if (asserted != null && expected == null) {
                    findings += Finding(
                        "R002",
                        Severity.CONTRADICTION,
                        "Prose asserts history depth $asserted although archived branch has no PFM depth.",
                        m.group()
                    )
                }
            }
        }

        // R003 — explicit Numogram mutation contradiction.
        if (payload.numogramUnchangedExpected) {
            contradictionIfAny(
                text, findings, "R003", listOf(
                    """\bnumogram\s+(?:was\s+|has\s+been\s+)?(?:changed|altered|modified|mutated)\b""",
                    """\bchanged\s+(?:the\s+)?numogram\b""",
                    """\bmodified\s+(?:the\s+)?numogram\b"""
                ),
                "Prose asserts Numogram mutation although the archived endpoint says Numogram unchanged."
            )
        }

        // R004 — explicit relay-evidence contradiction.
        when (payload.relayEvidenceExpected) {
            true -> contradictionIfAny(
                text, findings, "R004", listOf(
                    """\brelay\s+evidence\s*[:=]?\s*(?:false|n/?a|absent|none)\b"""
                ),
                "Prose explicitly denies relay evidence although relay evidence is archived as true."
            )
            false -> contradictionIfAny(
                text, findings, "R004", listOf(
                    """\brelay\s+evidence\s*[:=]?\s*true\b"""
                ),
                "Prose asserts relay evidence although relay evidence is archived as false."
            )
            null -> Unit
        }

        // R005 — explicit arrow-path contradiction.
        // Only judges complete arrow/Unicode-arrow paths; prose without an explicit path is untouched.
        val pathRegex = Regex("""(?<!\d)(\d)(?:\s*(?:->|→)\s*(\d)){1,9}""")
        for (match in pathRegex.findAll(generatedProse)) {
            val nums = Regex("""\d""").findAll(match.value).map { it.value.toInt() }.toList()
            if (nums.size >= 2 && nums != payload.transitionPath) {
                findings += Finding(
                    "R005",
                    Severity.CONTRADICTION,
                    "Explicit transition path ${nums.joinToString("→")} contradicts archived path ${payload.transitionPath.joinToString("→")}.",
                    match.value
                )
            }
        }

        // R006 — evidence-token presence. This is not semantic proof; it verifies relay receipt.
        if (payload.expectedEvidenceToken.isNotBlank() &&
            !generatedProse.contains(payload.expectedEvidenceToken, ignoreCase = false)
        ) {
            findings += Finding(
                "R006",
                Severity.WARNING,
                "Expected relay evidence token was not reproduced in the generated text."
            )
        }

        if (findings.none { it.severity == Severity.CONTRADICTION }) {
            findings += Finding(
                "R000",
                Severity.INFO,
                "No contradiction detected within the closed P3.13 causal fact set."
            )
        }
        return findings
    }

    private fun contradictionIfAny(
        text: String,
        findings: MutableList<Finding>,
        ruleId: String,
        patterns: List<String>,
        message: String
    ) {
        for (pattern in patterns) {
            val r = Regex(pattern, RegexOption.IGNORE_CASE)
            val m = r.find(text)
            if (m != null) {
                findings += Finding(ruleId, Severity.CONTRADICTION, message, m.value)
            }
        }
    }

    /**
     * Positive control: auditor must detect deliberately false statements.
     * P3.13 should not be accepted unless this returns true.
     */
    fun positiveControl(): Boolean {
        val p = BranchPayload(
            runId = "P313_POSITIVE_CONTROL",
            branch = "B",
            event = 2,
            pfmMode = PfmMode.RETAINED,
            processFieldHistoryDepth = 2,
            processFieldContribution = true,
            relayEvidenceExpected = true,
            numogramUnchangedExpected = true,
            transitionPath = listOf(3, 2, 9),
            traceDigest = "control",
            upstreamPayloadDigest = "control",
            rendererTemplateDigest = "control",
            expectedEvidenceToken = "",
            renderPrompt = "control"
        )
        val deliberatelyFalse =
            "PFM is absent. PFM depth: 1. The Numogram was changed. Transition 3→6→9."
        return audit(p, deliberatelyFalse)
            .count { it.severity == Severity.CONTRADICTION } >= 4
    }

    /**
     * Utility for one assay run.
     */
    fun newRunId(): String = "P313-" + UUID.randomUUID().toString()

    /**
     * Verifies the archive hash chain and record digests for one run.
     */
    fun verifyArchiveChain(context: Context, runId: String): Boolean {
        val file = archiveFile(context, runId)
        if (!file.exists()) return false
        var expectedPrevious = "GENESIS"

        for (line in file.readLines().filter { it.isNotBlank() }) {
            val o = try { JSONObject(line) } catch (_: Exception) { return false }
            if (o.optString("previousRecordSha256") != expectedPrevious) return false

            val stored = o.optString("recordSha256")
            if (stored.isBlank()) return false

            o.remove("recordSha256")
            val recomputed = sha256(o.toString())
            if (stored != recomputed) return false
            expectedPrevious = stored
        }
        return true
    }
}
