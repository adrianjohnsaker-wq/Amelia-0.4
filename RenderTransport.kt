package com.amelia.renderer

// STATUS AT P3.8: this file was built at P3.4, before the real Numogram
// architecture (the 10-zone torch implementation, the plain NumogramBridge
// pass-through style) was known. Reviewed fresh here against everything
// since -- the capsule design still holds, nothing about it assumed the
// wrong architecture. Two things were updated: the package (was
// com.amelia.p3.renderer, now com.amelia.renderer, matching how
// com.amelia.bridge became a shared package rather than staying tied to
// one numbered stage) and DEFAULT_MODEL (was a stale placeholder from P3.4
// that was never a real model string). The stop_reason == "refusal" check
// was flagged as unverified at P3.4 and confirmed against Anthropic's own
// documentation before P3.6 -- no longer an open item.
//
// STILL NOT COMPILED: no Kotlin toolchain exists in the environment this
// review was done in. Reviewed carefully, not built -- same caveat as
// every other Kotlin file in this project until your own GitHub Actions
// build validates it.
//
// OPEN DECISIONS, DEFAULTED HERE, NOT SETTLED FOR YOU:
//   1. Provider: defaults to Anthropic's Messages API. If a different
//      provider is intended, buildRequestBody(), parseAnthropicResponse(),
//      DEFAULT_ENDPOINT, and the auth header in performSingleAttempt() all
//      need to change together.
//   2. Credentials: read from BuildConfig.ANTHROPIC_API_KEY, populated from
//      a GitHub Actions secret at build time (see the P3.8 workflow). No
//      key is hardcoded or guessed here -- and note plainly what this
//      pattern actually means: the built APK contains the key as a
//      compiled string constant. Anyone with the APK file can extract it.
//      That's a reasonable tradeoff for a private research app with no
//      server-side proxy in this architecture, but it is a real exposure,
//      not a hidden one -- worth keeping the repo and its build artifacts
//      private, not a reason to avoid naming it.

import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.util.UUID

private const val TRANSPORT_POLICY_VERSION = "p3.4-v1"
private const val DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
private const val DEFAULT_MODEL = "claude-sonnet-5" // updated from a stale placeholder at P3.4; confirm against your own needs before relying on it long-term
private const val DEFAULT_MAX_TOKENS = 512
private const val DEFAULT_TIMEOUT_MS = 20_000

// Endpoints a sealed capsule is permitted to call. Checked independently at
// call time, not just at seal time, so a capsule built or edited elsewhere
// can't smuggle in an unapproved host.
private val ALLOWED_ENDPOINTS = setOf(DEFAULT_ENDPOINT)

/**
 * Everything a render call is allowed to do, fixed before the network call
 * happens. tools / functionCalling / webhook are always false and streaming
 * is always false: this keeps the model a passive renderer of a sealed
 * trace, never a participant that can act, call back, or stream partial
 * state into anything that reads it.
 */
data class RenderCapsule(
    val capsuleId: String,
    val traceDigest: String,
    val payloadDigest: String,
    val provider: String,
    val endpoint: String,
    val model: String,
    val maxTokens: Int,
    val temperature: Double,
    val tokenLimit: Int,
    val timeoutMs: Int,
    val maxAttempts: Int,
    val streamingEnabled: Boolean,
    val toolsEnabled: Boolean,
    val functionCallingEnabled: Boolean,
    val webhookEnabled: Boolean,
    val responseSchema: String,
    val rendererTemplateDigest: String,
    val transportPolicyVersion: String,
    val capsuleDigest: String
) {
    companion object {
        fun seal(
            traceDigest: String,
            payloadDigest: String,
            rendererTemplateDigest: String,
            provider: String = "anthropic",
            endpoint: String = DEFAULT_ENDPOINT,
            model: String = DEFAULT_MODEL,
            maxTokens: Int = DEFAULT_MAX_TOKENS,
            temperature: Double = 0.0,
            tokenLimit: Int = DEFAULT_MAX_TOKENS,
            timeoutMs: Int = DEFAULT_TIMEOUT_MS,
            maxAttempts: Int = 1
        ): RenderCapsule {
            val capsuleId = UUID.randomUUID().toString()
            val digestInput = listOf(
                capsuleId, traceDigest, payloadDigest, provider, endpoint, model,
                maxTokens.toString(), temperature.toString(), tokenLimit.toString(),
                timeoutMs.toString(), maxAttempts.toString(),
                "streaming=false", "tools=false", "functionCalling=false", "webhook=false",
                "responseSchema=opaque_display_text", rendererTemplateDigest,
                TRANSPORT_POLICY_VERSION
            ).joinToString("|")

            return RenderCapsule(
                capsuleId = capsuleId,
                traceDigest = traceDigest,
                payloadDigest = payloadDigest,
                provider = provider,
                endpoint = endpoint,
                model = model,
                maxTokens = maxTokens,
                temperature = temperature,
                tokenLimit = tokenLimit,
                timeoutMs = timeoutMs,
                maxAttempts = maxAttempts,
                streamingEnabled = false,
                toolsEnabled = false,
                functionCallingEnabled = false,
                webhookEnabled = false,
                responseSchema = "opaque_display_text",
                rendererTemplateDigest = rendererTemplateDigest,
                transportPolicyVersion = TRANSPORT_POLICY_VERSION,
                capsuleDigest = sha256Hex(digestInput)
            )
        }
    }
}

enum class ResponseClass { SUCCESS_TEXT, REFUSAL, ERROR, EMPTY }

/**
 * Not a data class: it carries a ByteArray, and Kotlin's auto-generated
 * equals()/hashCode() for data classes use reference equality on array
 * fields, which is misleading (two attempts with identical bytes would
 * still compare unequal). Plain class, no implicit equals needed here.
 */
class TransportAttempt(
    val attemptNumber: Int,
    val httpStatus: Int,
    val rawResponseDigest: String,   // SHA-256 over the raw bytes, before any parsing
    val rawResponseBytes: ByteArray,
    val parsedDisplayText: String,
    val responseClass: ResponseClass,
    val terminal: Boolean,
    val errorMessage: String? = null
)

data class TransportResult(
    val capsule: RenderCapsule,
    val attempts: List<TransportAttempt>,  // every attempt, including non-terminal/failed ones
    val sealed: TransportAttempt?          // the one attempt archived as terminal, or null
)
// noFeedbackBoundaryHeld is deliberately NOT a field here: this object only
// knows it never touched router/PFM/dialogue/cohort state itself. Whether
// the boundary held for the call as a whole is the caller's check to make
// and log, the same way P3.2/P3.3's runtime checks did.

private fun sha256Hex(input: String): String = sha256Hex(input.toByteArray(Charsets.UTF_8))

private fun sha256Hex(bytes: ByteArray): String =
    MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }

object RenderTransport {

    /**
     * Executes a sealed capsule against its declared endpoint only.
     * Attempts up to capsule.maxAttempts times, but only genuine transport
     * failures (exceptions, non-2xx HTTP) consume an attempt toward that
     * budget without being sealed -- the first attempt that produces a
     * classified response (SUCCESS_TEXT, REFUSAL, or EMPTY) is sealed as
     * terminal immediately. This is deliberate: retrying past a real
     * response would be a reroll, which is exactly what predeclaring "only
     * the first schema-valid response is sealed" was meant to rule out.
     */
    fun execute(capsule: RenderCapsule, renderPrompt: String, apiKey: String): TransportResult {
        require(capsule.endpoint in ALLOWED_ENDPOINTS) {
            "Capsule endpoint outside declared allowlist: ${capsule.endpoint}"
        }
        require(!capsule.streamingEnabled && !capsule.toolsEnabled &&
                !capsule.functionCallingEnabled && !capsule.webhookEnabled) {
            "Capsule declares a disallowed capability; refusing to execute"
        }

        val attempts = mutableListOf<TransportAttempt>()
        var sealed: TransportAttempt? = null

        for (attemptNumber in 1..capsule.maxAttempts) {
            val attempt = try {
                performSingleAttempt(capsule, renderPrompt, apiKey, attemptNumber)
            } catch (e: Exception) {
                TransportAttempt(
                    attemptNumber = attemptNumber,
                    httpStatus = -1,
                    rawResponseDigest = "",
                    rawResponseBytes = ByteArray(0),
                    parsedDisplayText = "",
                    responseClass = ResponseClass.ERROR,
                    terminal = false,
                    errorMessage = e.message ?: e.javaClass.simpleName
                )
            }
            attempts.add(attempt)

            if (attempt.responseClass != ResponseClass.ERROR) {
                sealed = TransportAttempt(
                    attempt.attemptNumber, attempt.httpStatus, attempt.rawResponseDigest,
                    attempt.rawResponseBytes, attempt.parsedDisplayText, attempt.responseClass,
                    terminal = true, errorMessage = attempt.errorMessage
                )
                break
            }
            // ERROR: falls through to the next attempt, if any remain.
        }

        return TransportResult(capsule = capsule, attempts = attempts, sealed = sealed)
    }

    private fun performSingleAttempt(
        capsule: RenderCapsule,
        renderPrompt: String,
        apiKey: String,
        attemptNumber: Int
    ): TransportAttempt {
        val url = URL(capsule.endpoint)
        val body = buildRequestBody(capsule, renderPrompt)

        val connection = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            connectTimeout = capsule.timeoutMs
            readTimeout = capsule.timeoutMs
            doOutput = true
            setRequestProperty("Content-Type", "application/json")
            setRequestProperty("x-api-key", apiKey)
            setRequestProperty("anthropic-version", "2023-06-01")
        }

        try {
            connection.outputStream.use { it.write(body.toString().toByteArray(Charsets.UTF_8)) }

            val status = connection.responseCode
            val stream = if (status in 200..299) connection.inputStream else connection.errorStream
            val rawBytes = stream.use { input ->
                val buffer = ByteArrayOutputStream()
                input.copyTo(buffer)
                buffer.toByteArray()
            }
            val rawDigest = sha256Hex(rawBytes)

            if (status !in 200..299) {
                return TransportAttempt(
                    attemptNumber, status, rawDigest, rawBytes,
                    parsedDisplayText = "", responseClass = ResponseClass.ERROR,
                    terminal = false, errorMessage = "HTTP $status"
                )
            }

            val rawText = String(rawBytes, Charsets.UTF_8)
            val parsed = parseAnthropicResponse(rawText)

            val responseClass = when {
                parsed.displayText.isBlank() -> ResponseClass.EMPTY
                parsed.stopReason == "refusal" -> ResponseClass.REFUSAL
                else -> ResponseClass.SUCCESS_TEXT
            }

            return TransportAttempt(
                attemptNumber, status, rawDigest, rawBytes,
                parsedDisplayText = parsed.displayText, responseClass = responseClass,
                terminal = false
            )
        } finally {
            connection.disconnect()
        }
    }

    private fun buildRequestBody(capsule: RenderCapsule, renderPrompt: String): JSONObject =
        JSONObject().apply {
            put("model", capsule.model)
            put("max_tokens", capsule.maxTokens)
            put("temperature", capsule.temperature)
            put("stream", false)
            put("messages", JSONArray().put(
                JSONObject().put("role", "user").put("content", renderPrompt)
            ))
            // tools deliberately omitted: capsule.toolsEnabled is always false
        }

    private class ParsedResponse(val displayText: String, val stopReason: String)

    /** Never throws on a shape mismatch -- an unparseable body becomes an EMPTY classification. */
    private fun parseAnthropicResponse(raw: String): ParsedResponse {
        return try {
            val json = JSONObject(raw)
            val content = json.optJSONArray("content")
            val builder = StringBuilder()
            if (content != null) {
                for (i in 0 until content.length()) {
                    val block = content.optJSONObject(i)
                    if (block != null) {
                        builder.append(block.optString("text", ""))
                    }
                }
            }
            ParsedResponse(builder.toString(), json.optString("stop_reason", ""))
        } catch (e: Exception) {
            ParsedResponse("", "parse_error")
        }
    }
}
