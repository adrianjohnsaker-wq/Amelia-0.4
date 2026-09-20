package com.amelia.renderer

// Sits between NumogramBridge's raw JSON and RenderTransport's sealed
// capsule. Takes a completed run_fork() result and produces exactly what
// RenderCapsule.seal() needs: a renderPrompt string, and digests over the
// trace being rendered, the specific payload handed to the model, and the
// prompt template itself.
//
// Deliberately curated, not verbatim: the renderer gets origin, each
// branch's from/to/fallback, and the three invariant flags -- not the full
// probability vectors, not the capsule digest, not anything about seed or
// internal tensor state. This is the same principle P3.2's template
// renderer worked under ("received no original prompt, process-memory
// state, cohort record, or mutation handle") applied to a real LLM instead
// of a fixed phrase table: give it only what it needs to describe the
// trace, nothing that would let it reconstruct or reason about the
// substrate's internals beyond what's already been computed and sealed.
//
// PROMPT WORDING IS A FIRST DRAFT, NOT SETTLED: the actual phrasing here
// is mine, written to state the one-way/no-feedback boundary and the
// no-consciousness-claim discipline this project has held since P0 --
// not to dictate voice or philosophical framing, which is yours to adjust.
// Changing the prompt text changes rendererTemplateDigest, which is exactly
// the point: any change to what the renderer is told to do is itself
// tracked, not silently absorbed into "the same template" as before.

import org.json.JSONObject
import java.security.MessageDigest

private const val TEMPLATE_VERSION = "p3.8-fork-render-v1"

data class RenderPromptPayload(
    val renderPrompt: String,
    val traceDigest: String,
    val payloadDigest: String,
    val rendererTemplateDigest: String
)

object RenderPromptBuilder {

    private val PROMPT_TEMPLATE = """
        You are rendering one sealed trace from a deterministic computational
        substrate into plain descriptive prose. The substrate is a ten-zone
        Numogram (zones 0-9) with a torch-based tensor memory channel. The
        trace below has already been fully computed and sealed before you
        were called -- you are a read-only, one-way display. Nothing you
        write feeds back into the substrate, changes any future computation,
        or is stored as part of the trace itself.

        Do not invent zones, numbers, or outcomes beyond what is given below.
        Do not claim this trace is evidence of consciousness, sentience, or
        agency. Describe only the structural pattern the data actually
        shows: which branch went where, whether the ablated conditions
        diverged from the full condition, and whether the neutral-reset
        condition landed somewhere different. Two or three sentences of
        plain prose. No bullet points, no headers, no restating the raw
        numbers back verbatim.

        Sealed trace:
        %s
    """.trimIndent()

    fun buildFromForkResult(forkResult: JSONObject): RenderPromptPayload {
        val branches = forkResult.optJSONObject("branches") ?: JSONObject()
        val invariants = forkResult.optJSONObject("invariants") ?: JSONObject()

        val curatedBranches = JSONObject()
        for (name in listOf("FULL", "ABLATED_TRANSITION", "ABLATED_MAGNETISM", "ABLATED_BOTH", "NEUTRAL_RESET")) {
            val branch = branches.optJSONObject(name) ?: continue
            curatedBranches.put(
                name,
                JSONObject()
                    .put("from", branch.optInt("from", -1))
                    .put("to", branch.optInt("to", -1))
                    .put("fallback", branch.optBoolean("fallback", false))
            )
        }

        val curatedPayload = JSONObject()
            .put("schema", "amelia-p3.8-render-payload-v1")
            .put("capsule_digest", forkResult.optString("capsule_digest", ""))
            .put("origin", forkResult.optInt("origin", -1))
            .put("branches", curatedBranches)
            .put(
                "invariants",
                JSONObject()
                    .put("live_state_unchanged", invariants.optBoolean("live_state_unchanged", false))
                    .put("generator_state_unchanged", invariants.optBoolean("generator_state_unchanged", false))
                    .put(
                        "ablated_both_matches_neutral_reset",
                        invariants.optBoolean("ablated_both_matches_neutral_reset", false)
                    )
            )

        val canonicalPayload = canonicalize(curatedPayload)
        val payloadDigest = sha256Hex(canonicalPayload)

        // traceDigest covers the full, uncurated Numogram result -- what
        // was actually sealed by run_fork(), independent of how much of it
        // the renderer was actually shown. Lets a later check confirm the
        // render corresponds to a real, specific trace even though the
        // renderer itself never saw the whole thing.
        val traceDigest = sha256Hex(canonicalize(forkResult))

        val renderPrompt = PROMPT_TEMPLATE.format(canonicalPayload)
        val rendererTemplateDigest = sha256Hex(PROMPT_TEMPLATE + TEMPLATE_VERSION)

        return RenderPromptPayload(
            renderPrompt = renderPrompt,
            traceDigest = traceDigest,
            payloadDigest = payloadDigest,
            rendererTemplateDigest = rendererTemplateDigest
        )
    }

    /** org.json.JSONObject doesn't sort keys on toString(), and its parsed
     * form doesn't preserve source order either -- so re-serializing a
     * parsed JSONObject can legitimately produce different byte output than
     * what Python originally sent, even though Python's own _canonical()
     * already sorts keys. Digest stability requires sorting again here,
     * recursively, including through arrays in case an array element is
     * itself an object (not the case in the current fork-result shape, but
     * handled generally rather than relying on that happening to be true). */
    private fun canonicalize(value: Any?): String {
        return when (value) {
            is JSONObject -> {
                val keys = value.keys().asSequence().sorted().toList()
                val builder = StringBuilder("{")
                for ((index, key) in keys.withIndex()) {
                    if (index > 0) builder.append(",")
                    builder.append(JSONObject.quote(key)).append(":")
                    builder.append(canonicalize(value.get(key)))
                }
                builder.append("}")
                builder.toString()
            }
            is org.json.JSONArray -> {
                val builder = StringBuilder("[")
                for (i in 0 until value.length()) {
                    if (i > 0) builder.append(",")
                    builder.append(canonicalize(value.get(i)))
                }
                builder.append("]")
                builder.toString()
            }
            else -> JSONObject.valueToString(value)
        }
    }

    private fun sha256Hex(input: String): String =
        MessageDigest.getInstance("SHA-256").digest(input.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
}
