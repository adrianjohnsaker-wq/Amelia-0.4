package com.amelia.renderer

import org.json.JSONArray
import org.json.JSONObject
import java.security.MessageDigest

private const val P311_TEMPLATE_VERSION =
    "p3.11-process-field-memory-relay-v1"
private const val P311_MAX_MESSAGES = 12
private const val P311_MAX_MESSAGE_CHARS = 2_400

data class P311ChatMessage(
    val role: String,
    val content: String
)

data class P311PromptPayload(
    val renderPrompt: String,
    val traceDigest: String,
    val payloadDigest: String,
    val rendererTemplateDigest: String,
    val expectedEvidenceToken: String?,
    val processFieldContribution: String?
)

/**
 * P3.11 extends the P3.10 relay contract with one explicit module-evidence
 * channel for ProcessFieldMemory.
 *
 * The module executes after the Numogram transition and before rendering.
 * When a valid ProcessFieldMemory contribution is present, the renderer is
 * required to use the contribution substantively and append a deterministic
 * evidence token. The activity verifies and strips that token before showing
 * the answer. The token proves that the module payload reached the renderer;
 * it is not, by itself, a semantic-equivalence proof.
 */
object P311MediatedChatPromptBuilder {

    private val BASE_TEMPLATE = """
        You are Amelia's linguistic relay.

        A process event has already been produced before this call. The sealed
        event below is authoritative. The Numogram transition, event class,
        selected module families, selected modules, and module outputs are not
        choices for you to make: they are the completed non-linguistic event
        which you must render into a coherent answer.

        Use the conversation history to understand the user's question. Use the
        sealed process event as the constitutive basis of the answer. Integrate
        executed module outputs when present, but do not invent outputs for
        modules which did not execute.

        Do not claim that you changed, selected, reran, overrode, or inspected
        the Numogram beyond the supplied payload. Do not invent hidden tools,
        network access, consciousness, sentience, or actions not represented in
        the payload.

        Do not expose hashes, JSON, implementation details, or internal module
        mechanics unless the user explicitly asks for them. Render the result
        naturally as Amelia's answer.

        Give a complete answer rather than prematurely truncating it. Plain text
        only. Do not use a Markdown code fence.

        Sealed P3.11 event:
    """.trimIndent()

    private val PFM_CONTRACT_TEMPLATE = """

        P3.11 PROCESS-FIELD MEMORY INCORPORATION CONTRACT

        ProcessFieldMemory executed successfully after the Numogram transition.
        Its interpretive contribution is quoted below:

        "%s"

        Incorporate that contribution materially into the substance of the
        answer. Do not merely mention that a module ran. The answer should make
        intelligible how retained process history conditions the present event.

        After the substantive answer, append the following evidence token on a
        separate final line, exactly as written:
        %s
    """.trimIndent()

    fun build(
        messages: List<P311ChatMessage>,
        transition: JSONObject,
        eventPlan: JSONObject,
        moduleResults: JSONObject
    ): P311PromptPayload {
        require(messages.isNotEmpty()) {
            "A P3.11 mediated event requires at least one message."
        }

        val messageArray = JSONArray()
        messages.takeLast(P311_MAX_MESSAGES).forEach { message ->
            require(message.role == "user" || message.role == "assistant") {
                "Unsupported chat role: ${message.role}"
            }
            val content = message.content.trim()
            require(content.isNotBlank()) {
                "Blank chat messages are not sealed."
            }
            require(content.length <= P311_MAX_MESSAGE_CHARS) {
                "A chat message exceeds the declared P3.11 length limit."
            }
            messageArray.put(
                JSONObject()
                    .put("role", message.role)
                    .put("content", content)
            )
        }

        val payload = JSONObject()
            .put("schema", "amelia-p3.11-mediated-payload-v1")
            .put("conversation", messageArray)
            .put("transition", transition)
            .put("event_plan", eventPlan)
            .put("module_results", moduleResults)
            .put("max_messages", P311_MAX_MESSAGES)
            .put("max_message_chars", P311_MAX_MESSAGE_CHARS)

        val canonicalPayload = canonicalize(payload)
        val pfm = processFieldMemoryPayload(moduleResults)

        val contribution = pfm
            ?.optString("interpretive_contribution", "")
            ?.trim()
            ?.takeIf { it.isNotBlank() }

        val marker = pfm
            ?.optString("relay_marker", "")
            ?.trim()
            ?.takeIf { it.matches(Regex("^[A-Za-z0-9._:-]{1,96}$")) }

        val expectedEvidenceToken = if (contribution != null && marker != null) {
            "[[PFM-EVIDENCE:$marker]]"
        } else {
            null
        }

        val contract = if (expectedEvidenceToken != null && contribution != null) {
            PFM_CONTRACT_TEMPLATE.format(
                contribution.replace("\n", " ").replace("\r", " "),
                expectedEvidenceToken
            )
        } else {
            ""
        }

        val renderPrompt = buildString {
            append(BASE_TEMPLATE)
            append("\n")
            append(canonicalPayload)
            if (contract.isNotBlank()) {
                append("\n")
                append(contract)
            }
        }

        val payloadDigest = sha256Hex(
            listOf(
                canonicalPayload,
                contribution ?: "no-pfm-contribution",
                expectedEvidenceToken ?: "no-pfm-evidence-token"
            ).joinToString("|")
        )

        return P311PromptPayload(
            renderPrompt = renderPrompt,
            traceDigest = sha256Hex("p3.11-event|$renderPrompt"),
            payloadDigest = payloadDigest,
            rendererTemplateDigest = sha256Hex(
                BASE_TEMPLATE + PFM_CONTRACT_TEMPLATE + P311_TEMPLATE_VERSION
            ),
            expectedEvidenceToken = expectedEvidenceToken,
            processFieldContribution = contribution
        )
    }

    private fun processFieldMemoryPayload(
        moduleResults: JSONObject
    ): JSONObject? {
        val results = moduleResults.optJSONArray("results") ?: return null

        for (index in 0 until results.length()) {
            val result = results.optJSONObject(index) ?: continue
            if (result.optString("file_name", "") != "ProcessFieldMemory.py") {
                continue
            }
            if (result.optString("status", "") != "executed") {
                continue
            }

            val rawOutput = result.optString("output", "")
            if (rawOutput.isBlank()) continue

            val parsed = try {
                JSONObject(rawOutput)
            } catch (_: Throwable) {
                continue
            }

            if (
                parsed.optString("schema", "") ==
                    "amelia-p3.11-process-field-memory-v1" &&
                parsed.optString("status", "") == "contribution_ready"
            ) {
                return parsed
            }
        }
        return null
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
                        character.code.toString(16).padStart(4, '0')
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

        is JSONArray -> buildString {
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
