package com.amelia.renderer

import org.json.JSONArray
import org.json.JSONObject
import java.security.MessageDigest

private const val MEDIATED_TEMPLATE_VERSION =
    "p3.10-numogram-mediated-language-v1"
private const val MAX_MESSAGES = 12
private const val MAX_MESSAGE_CHARS = 2_400

data class MediatedChatMessage(
    val role: String,
    val content: String
)

data class MediatedChatPromptPayload(
    val renderPrompt: String,
    val traceDigest: String,
    val payloadDigest: String,
    val rendererTemplateDigest: String
)

/**
 * P3.10 relay contract:
 *
 * The language model receives a process event which has already occurred.
 * It may synthesize that event into useful language, but it does not choose
 * the transition, select modules, rewrite module outputs, or feed anything
 * back into the Numogram.
 */
object MediatedChatPromptBuilder {

    private val TEMPLATE = """
        You are Amelia's linguistic relay.

        A process event has already been produced before this call. The sealed event below is authoritative. The Numogram transition, event class,
        selected module families, selected modules, and any module outputs are
        not suggestions for you to choose among: they are the completed
        non-linguistic event you must render into a coherent answer.

        Use the conversation history to understand the user's question. Use the
        sealed process event as the constitutive basis of the answer. Integrate
        module outputs when present, but do not invent outputs for modules which
        did not execute.

        Do not claim that you changed, selected, reran, overrode, or inspected
        the Numogram beyond the supplied payload. Do not invent hidden tools,
        network access, consciousness, sentience, or actions not represented in
        the payload.

        Do not expose implementation details, branch names, hashes, JSON, or
        internal module mechanics unless the user explicitly asks for them.
        Instead, express the synthesis naturally as Amelia's answer.

        Give a complete answer rather than prematurely truncating it. Plain text
        only. No Markdown code fence.

        Sealed P3.10 event:
        %s
    """.trimIndent()

    fun build(
        messages: List<MediatedChatMessage>,
        transition: JSONObject,
        eventPlan: JSONObject,
        moduleResults: JSONObject
    ): MediatedChatPromptPayload {
        require(messages.isNotEmpty()) {
            "A mediated chat event requires at least one message."
        }

        val messageArray = JSONArray()
        messages.takeLast(MAX_MESSAGES).forEach { message ->
            require(message.role == "user" || message.role == "assistant") {
                "Unsupported chat role: ${message.role}"
            }
            val content = message.content.trim()
            require(content.isNotBlank()) {
                "Blank chat messages are not sealed."
            }
            require(content.length <= MAX_MESSAGE_CHARS) {
                "A chat message exceeds the declared P3.10 length limit."
            }

            messageArray.put(
                JSONObject()
                    .put("role", message.role)
                    .put("content", content)
            )
        }

        val payload = JSONObject()
            .put("schema", "amelia-p3.10-mediated-payload-v1")
            .put("conversation", messageArray)
            .put("transition", transition)
            .put("event_plan", eventPlan)
            .put("module_results", moduleResults)
            .put("max_messages", MAX_MESSAGES)
            .put("max_message_chars", MAX_MESSAGE_CHARS)

        val canonicalPayload = canonicalize(payload)
        val payloadDigest = sha256Hex(canonicalPayload)

        return MediatedChatPromptPayload(
            renderPrompt = TEMPLATE.format(canonicalPayload),
            traceDigest = sha256Hex("p3.10-event|$canonicalPayload"),
            payloadDigest = payloadDigest,
            rendererTemplateDigest =
                sha256Hex(TEMPLATE + MEDIATED_TEMPLATE_VERSION)
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
