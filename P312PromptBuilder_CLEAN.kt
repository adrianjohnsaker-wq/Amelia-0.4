package com.amelia.renderer

import org.json.JSONObject
import java.security.MessageDigest

private const val P312_TEMPLATE_VERSION =
    "p3.12-matched-causal-incorporation-relay-v1"

data class P312PromptPayload(
    val renderPrompt: String,
    val traceDigest: String,
    val payloadDigest: String,
    val rendererTemplateDigest: String,
    val expectedEvidenceToken: String?,
    val processFieldContribution: String?,
    val processFieldHistoryDepth: Int?
)

/**
 * The same base template is used for A, B and C. Condition labels are not
 * included in the provider prompt. The only treatment difference is the
 * presence/content of the sealed ProcessFieldMemory payload.
 */
object P312PromptBuilder {

    private val BASE_TEMPLATE = """
        You are Amelia's linguistic relay in a matched causal incorporation assay.

        Two user prompts were presented to the same Numogram chassis. The first
        prompt is a conditioning event and received no language response. Answer
        only the second, critical prompt.

        The two Numogram transitions shown below have already occurred. They are
        authoritative and must not be revised. If a ProcessFieldMemory payload is
        present, its interpretive contribution is part of the completed process
        event and must be incorporated materially into the answer. If no such
        payload is present, do not invent retained ProcessFieldMemory history.

        Do not mention assay branch labels, hidden tools, implementation details,
        hashes, JSON, or internal evidence machinery unless the user explicitly
        asks for them. Render the result naturally as Amelia's answer.

        Give a complete answer. Plain text only. Do not use a Markdown code fence.

        Sealed event:
        %s
    """.trimIndent()

    private val PFM_CONTRACT = """

        PROCESS-FIELD MEMORY INCORPORATION CONTRACT

        The sealed ProcessFieldMemory contribution is:

        "%s"

        Incorporate this contribution substantively. Then append the following
        evidence token on a separate final line exactly as written:
        %s
    """.trimIndent()

    fun build(
        conditioningPrompt: String,
        criticalPrompt: String,
        eventOne: JSONObject,
        eventTwo: JSONObject,
        pfmEventTwo: JSONObject?
    ): P312PromptPayload {
        require(conditioningPrompt.isNotBlank())
        require(criticalPrompt.isNotBlank())

        val validPfm = pfmEventTwo?.takeIf {
            it.optString("schema", "") ==
                "amelia-p3.11-process-field-memory-v1" &&
                it.optString("status", "") == "contribution_ready"
        }

        val contribution = validPfm
            ?.optString("interpretive_contribution", "")
            ?.trim()
            ?.takeIf { it.isNotBlank() }

        val marker = validPfm
            ?.optString("relay_marker", "")
            ?.trim()
            ?.takeIf {
                it.matches(Regex("^[A-Za-z0-9._:-]{1,96}$"))
            }

        val historyDepth = validPfm
            ?.optInt("history_depth", -1)
            ?.takeIf { it >= 0 }

        val expectedToken =
            if (
                contribution != null &&
                marker != null &&
                historyDepth != null
            ) {
                "[[PFM-EVIDENCE:$marker:DEPTH:$historyDepth]]"
            } else {
                null
            }

        val sealed = JSONObject()
            .put(
                "schema",
                "amelia-p3.12-relay-payload-v1"
            )
            .put("conditioning_prompt", conditioningPrompt)
            .put("critical_prompt", criticalPrompt)
            .put("event_one", eventOne)
            .put("event_two", eventTwo)
            .put(
                "process_field_memory",
                validPfm ?: JSONObject.NULL
            )

        val canonicalPayload = canonicalize(sealed)

        val renderPrompt = buildString {
            append(BASE_TEMPLATE.format(canonicalPayload))
            if (
                expectedToken != null &&
                contribution != null
            ) {
                append("\n")
                append(
                    PFM_CONTRACT.format(
                        contribution
                            .replace("\n", " ")
                            .replace("\r", " "),
                        expectedToken
                    )
                )
            }
        }

        return P312PromptPayload(
            renderPrompt = renderPrompt,
            traceDigest =
                sha256Hex("p3.12-relay|$renderPrompt"),
            payloadDigest =
                sha256Hex(canonicalPayload),
            rendererTemplateDigest =
                sha256Hex(
                    BASE_TEMPLATE +
                        PFM_CONTRACT +
                        P312_TEMPLATE_VERSION
                ),
            expectedEvidenceToken = expectedToken,
            processFieldContribution = contribution,
            processFieldHistoryDepth = historyDepth
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
                    builder.append(
                        character.code
                            .toString(16)
                            .padStart(4, '0')
                    )
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
            val keys =
                value.keys().asSequence().sorted().toList()
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
