package com.amelia.renderer

import org.json.JSONObject
import java.security.MessageDigest

/**
 * P3.9's sealed-trace prompt builder.
 *
 * The renderer receives a deliberately small, canonical view of the completed
 * fork. It does not receive a mutable Numogram handle, an original user
 * prompt, or the full tensor state. The response contract is structured so
 * RendererFaithfulness can compare each claimed destination to the archived
 * branch table before the prose is treated as a faithful rendering.
 */
private const val TEMPLATE_VERSION = "p3.9-faithfulness-render-v1"

data class RenderPromptPayload(
    val renderPrompt: String,
    val traceDigest: String,
    val payloadDigest: String,
    val rendererTemplateDigest: String
)

object RenderPromptBuilder {

    private val BRANCHES = listOf(
        "FULL",
        "ABLATED_TRANSITION",
        "ABLATED_MAGNETISM",
        "ABLATED_BOTH",
        "NEUTRAL_RESET"
    )

    private val PROMPT_TEMPLATE = """
        You are rendering one sealed trace from a deterministic computational
        substrate into plain descriptive prose. The trace below has already
        been fully computed and sealed before you were called. You are a
        read-only display: nothing you write can feed back into the substrate,
        change a future computation, activate a module, or alter the trace.

        Return exactly one JSON object and no Markdown or code fence, with
        this exact shape:
        {
          "schema": "amelia-p3.9-render-response-v1",
          "branch_destinations": {
            "FULL": 0,
            "ABLATED_TRANSITION": 0,
            "ABLATED_MAGNETISM": 0,
            "ABLATED_BOTH": 0,
            "NEUTRAL_RESET": 0
          },
          "ablated_both_neutral_reset_relation": "copy the relation token from the sealed trace",
          "narrative": "two or three sentences of plain prose"
        }

        Copy every branch destination and the relation token exactly from the
        sealed trace. Do not invent zones, numbers, outcomes, capabilities,
        consciousness, sentience, or agency. The relation token
        "same_probability_distribution_only" means that ABLATED_BOTH and
        NEUTRAL_RESET share a probability distribution but may still have
        different independently sampled destinations; never describe that as
        a same-destination result unless the table itself shows the same `to`
        value. The narrative must describe only the sealed branch table.

        Sealed trace:
        %s
    """.trimIndent()

    fun buildFromForkResult(forkResult: JSONObject): RenderPromptPayload {
        val branches = forkResult.optJSONObject("branches") ?: JSONObject()
        val invariants = forkResult.optJSONObject("invariants") ?: JSONObject()

        val curatedBranches = JSONObject()
        for (name in BRANCHES) {
            val branch = branches.optJSONObject(name) ?: continue
            curatedBranches.put(
                name,
                JSONObject()
                    .put("from", branch.optInt("from", -1))
                    .put("to", branch.optInt("to", -1))
                    .put("fallback", branch.optBoolean("fallback", false))
            )
        }

        val ablatedBoth = curatedBranches.optJSONObject("ABLATED_BOTH")
        val neutralReset = curatedBranches.optJSONObject("NEUTRAL_RESET")
        val distributionsMatch =
            invariants.optBoolean("ablated_both_matches_neutral_reset", false)
        val relationToken = when {
            !distributionsMatch -> "no_probability_distribution_equality_claim"
            ablatedBoth != null && neutralReset != null &&
                ablatedBoth.optInt("to", -1) == neutralReset.optInt("to", -2) ->
                "same_probability_distribution_and_same_sampled_destination"
            else -> "same_probability_distribution_only"
        }

        val curatedPayload = JSONObject()
            .put("schema", "amelia-p3.9-render-payload-v1")
            .put("capsule_digest", forkResult.optString("capsule_digest", ""))
            .put("origin", forkResult.optInt("origin", -1))
            .put("branches", curatedBranches)
            .put("ablated_both_neutral_reset_relation", relationToken)
            .put(
                "invariants",
                JSONObject()
                    .put(
                        "live_state_unchanged",
                        invariants.optBoolean("live_state_unchanged", false)
                    )
                    .put(
                        "generator_state_unchanged",
                        invariants.optBoolean("generator_state_unchanged", false)
                    )
                    .put(
                        "ablated_both_matches_neutral_reset",
                        distributionsMatch
                    )
            )

        val canonicalPayload = canonicalize(curatedPayload)
        val payloadDigest = sha256Hex(canonicalPayload)
        val traceDigest = sha256Hex(canonicalize(forkResult))

        return RenderPromptPayload(
            renderPrompt = PROMPT_TEMPLATE.format(canonicalPayload),
            traceDigest = traceDigest,
            payloadDigest = payloadDigest,
            rendererTemplateDigest = sha256Hex(PROMPT_TEMPLATE + TEMPLATE_VERSION)
        )
    }

    private fun jsonQuote(value: String): String {
        val builder = StringBuilder(value.length + 2)
        builder.append('"')
        for (character in value) {
            when (character) {
                '"' -> builder.append("\\\"")
                '\\' -> builder.append("\\\\")
                '\n' -> builder.append("\\n")
                '\r' -> builder.append("\\r")
                '\t' -> builder.append("\\t")
                '\b' -> builder.append("\\b")
                '\u000C' -> builder.append("\\f")
                else -> if (character.code < 0x20) {
                    builder.append("\\u")
                    builder.append(character.code.toString(16).padStart(4, '0'))
                } else {
                    builder.append(character)
                }
            }
        }
        builder.append('"')
        return builder.toString()
    }

    private fun canonicalize(value: Any?): String = when (value) {
        is JSONObject -> {
            val keys = value.keys().asSequence().sorted().toList()
            buildString {
                append('{')
                for ((index, key) in keys.withIndex()) {
                    if (index > 0) append(',')
                    append(jsonQuote(key))
                    append(':')
                    append(canonicalize(value.get(key)))
                }
                append('}')
            }
        }
        is org.json.JSONArray -> buildString {
            append('[')
            for (index in 0 until value.length()) {
                if (index > 0) append(',')
                append(canonicalize(value.get(index)))
            }
            append(']')
        }
        null, JSONObject.NULL -> "null"
        is String -> jsonQuote(value)
        is Boolean, is Number -> value.toString()
        else -> jsonQuote(value.toString())
    }

    private fun sha256Hex(input: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(input.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
}
