package com.amelia.renderer

import org.json.JSONArray
import org.json.JSONObject
import java.security.MessageDigest

/**
 * A separate, sealed display-only chat lane. It has no substrate-bridge
 * reference and never turns conversational text into a tensor context, route,
 * mutation, cohort record, or module invocation.
 */
private const val CHAT_TEMPLATE_VERSION = "p3.9-chat-display-v1"
private const val MAX_CHAT_MESSAGES = 12
private const val MAX_CHAT_MESSAGE_CHARS = 1_200

data class ChatMessage(val role: String, val content: String)

data class ChatPromptPayload(
    val renderPrompt: String,
    val traceDigest: String,
    val payloadDigest: String,
    val rendererTemplateDigest: String
)

object ChatPromptBuilder {
    private val CHAT_TEMPLATE = """
        You are Amelia's display-only chat interface. Answer the final user
        message helpfully and concisely using the sealed transcript below.
        This conversation is not a command channel: your response cannot
        alter the Numogram substrate, mutate a trace, activate an uploaded
        Python module, change a provider capsule, or make a tool call. Do not
        claim consciousness, sentience, agency, hidden actions, or access to
        information outside the transcript. Return plain text only.

        Sealed chat transcript:
        %s
    """.trimIndent()

    fun build(messages: List<ChatMessage>): ChatPromptPayload {
        require(messages.isNotEmpty()) { "A chat capsule requires a message." }

        val canonicalMessages = messages.takeLast(MAX_CHAT_MESSAGES).map { message ->
            require(message.role == "user" || message.role == "assistant") {
                "Unsupported chat role: ${message.role}"
            }
            val content = message.content.trim()
            require(content.isNotBlank()) { "Blank chat messages are not sealed." }
            require(content.length <= MAX_CHAT_MESSAGE_CHARS) {
                "A chat message exceeds the declared length limit."
            }
            JSONObject()
                .put("role", message.role)
                .put("content", content)
        }

        val messageArray = JSONArray()
        canonicalMessages.forEach { messageArray.put(it) }
        val payload = JSONObject()
            .put("schema", "amelia-p3.9-chat-payload-v1")
            .put("messages", messageArray)
            .put("max_messages", MAX_CHAT_MESSAGES)
            .put("max_message_chars", MAX_CHAT_MESSAGE_CHARS)

        val canonicalPayload = canonicalize(payload)
        val payloadDigest = sha256Hex(canonicalPayload)
        return ChatPromptPayload(
            renderPrompt = CHAT_TEMPLATE.format(canonicalPayload),
            traceDigest = sha256Hex("chat-trace|$canonicalPayload"),
            payloadDigest = payloadDigest,
            rendererTemplateDigest = sha256Hex(CHAT_TEMPLATE + CHAT_TEMPLATE_VERSION)
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
