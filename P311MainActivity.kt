package com.amelia.p311

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import android.util.Log
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.bridge.NumogramBridge
import com.amelia.modules.ModuleRecord
import com.amelia.modules.ModuleRejectedException
import com.amelia.modules.PythonModuleVault
import com.amelia.orchestration.EventModulePlanner
import com.amelia.renderer.P311ChatMessage
import com.amelia.renderer.P311MediatedChatPromptBuilder
import com.amelia.renderer.RenderCapsule
import com.amelia.renderer.RenderTransport
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.security.MessageDigest

/**
 * Amelia Android P3.11
 *
 * Constitutive chat path:
 * user event -> deterministic Numogram input field -> committed transition ->
 * event/module synthesis -> selected audited module contributions -> sealed
 * language relay.
 *
 * The relay interprets an event already produced by the substrate. It does
 * not select or revise the Numogram transition, and its output is never fed
 * back into NumogramBridge.
 */
class MainActivity : Activity() {

    companion object {
        private const val LOG_TAG = "AMELIA_P311"
        private const val REQUEST_OPEN_PYTHON = 3111
        private const val MAX_PICKED_MODULE_BYTES = 128 * 1024
        private const val MAX_CHAT_INPUT_CHARS = 2_400
        private const val NUMOGRAM_SEED = 3606
        private const val NUMOGRAM_DIMENSION = 3
        private const val INITIAL_ZONE = 3
    }

    private lateinit var statusView: TextView
    private lateinit var processView: TextView
    private lateinit var chatLogView: TextView
    private lateinit var chatInput: EditText
    private lateinit var sendButton: Button
    private lateinit var moduleVaultView: TextView

    private val chatHistory = mutableListOf<P311ChatMessage>()
    private var providerCallInFlight = false
    private var currentZone = INITIAL_ZONE

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(22), dp(18), dp(28))
        }

        root.addView(TextView(this).apply {
            text = "AMELIA · P3.11"
            textSize = 25f
            gravity = Gravity.CENTER_HORIZONTAL
        })
        root.addView(TextView(this).apply {
            text = "Numogram-mediated chat · ProcessFieldMemory enactment · relay evidence"
            textSize = 14f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(8), 0, dp(16))
        })

        statusView = TextView(this).apply {
            text = "Ready. Each chat event is mediated by the Numogram before language rendering."
            textSize = 15f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(statusView)

        root.addView(sectionHeading("CHAT"))
        chatLogView = TextView(this).apply {
            text = "No chat messages yet."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(8))
        }
        root.addView(chatLogView)

        chatInput = EditText(this).apply {
            hint = "Write to Amelia"
            textSize = 16f
            minLines = 2
            maxLines = 6
            setPadding(dp(8), dp(8), dp(8), dp(8))
        }
        root.addView(chatInput)

        sendButton = actionButton("SEND THROUGH NUMOGRAM") { sendChat() }
        root.addView(sendButton)

        root.addView(sectionHeading("LAST PROCESS EVENT"))
        processView = TextView(this).apply {
            text = "No mediated event yet."
            textSize = 13f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(processView)

        root.addView(sectionHeading("PYTHON MODULE VAULT"))
        root.addView(TextView(this).apply {
            text =
                "P3.11 includes one bundled experimental module: ProcessFieldMemory.py. " +
                    "Stage it explicitly through the same P3.9 source audit used for any " +
                    "picked UTF-8 .py module. After the Numogram transition, the planner " +
                    "may select an audited module and invoke one declared entry point: " +
                    "amelia_event, process, run, or transform. The source audit reduces " +
                    "capabilities but is not described as a security sandbox."
            textSize = 13f
            setPadding(dp(4), dp(4), dp(4), dp(8))
        })
        root.addView(
            actionButton("STAGE PROCESS FIELD MEMORY") {
                stageBundledProcessFieldMemory()
            }
        )
        root.addView(actionButton("PICK PYTHON MODULE") { pickPythonModule() })
        root.addView(actionButton("REFRESH MODULE VAULT") { refreshModuleVault() })

        moduleVaultView = TextView(this).apply {
            text = "Loading staged modules…"
            textSize = 13f
            setPadding(dp(4), dp(10), dp(4), dp(12))
        }
        root.addView(moduleVaultView)

        root.addView(TextView(this).apply {
            text =
                "P3.11 process boundary:\n\n" +
                    "user event → digit-fold zone field → Numogram.transition → " +
                    "EventModulePlanner → ProcessFieldMemory contribution (when staged) → " +
                    "P311MediatedChatPromptBuilder → one sealed provider call → language\n\n" +
                    "When ProcessFieldMemory executes, P3.11 requires a deterministic relay " +
                    "evidence token. The app verifies and strips that token before display. " +
                    "A separate post-render status check confirms that rendering did not " +
                    "change Numogram evolution state."
            textSize = 13f
            setPadding(dp(4), dp(10), dp(4), 0)
        })

        scroll.addView(root)
        setContentView(scroll)
        refreshModuleVault()
    }

    private fun sectionHeading(text: String): TextView = TextView(this).apply {
        this.text = text
        textSize = 17f
        setPadding(dp(4), dp(18), dp(4), dp(4))
    }

    private fun actionButton(label: String, action: () -> Unit): Button = Button(this).apply {
        text = label
        setOnClickListener { action() }
    }

    private fun sendChat() {
        if (providerCallInFlight) {
            statusView.text = "A mediated event is already in progress."
            return
        }

        val userText = chatInput.text.toString().trim()
        if (userText.isBlank()) {
            statusView.text = "Write a chat message before sending."
            return
        }
        if (userText.length > MAX_CHAT_INPUT_CHARS) {
            statusView.text = "Chat messages are limited to $MAX_CHAT_INPUT_CHARS characters."
            return
        }

        chatHistory += P311ChatMessage("user", userText)
        trimChatHistory()
        chatInput.setText("")
        renderChatHistory()
        setProviderCallInFlight(true)
        statusView.text = "Processing event through the Numogram…"

        val snapshot = chatHistory.toList()
        Thread {
            val raw = try {
                executeMediatedChat(snapshot, userText)
            } catch (error: Throwable) {
                JSONObject()
                    .put("schema", "amelia-p3.11-chat-result-v1")
                    .put("status", "error")
                    .put("error_type", error::class.java.simpleName)
                    .put("message", error.message ?: "Unknown mediated chat error")
                    .toString()
            }

            Log.i(LOG_TAG, raw)
            runOnUiThread {
                renderChatResult(raw)
                setProviderCallInFlight(false)
            }
        }.start()
    }

    private fun executeMediatedChat(
        messages: List<P311ChatMessage>,
        userText: String
    ): String {
        val bridge = NumogramBridge(applicationContext)
        val runtime = JSONObject(bridge.runtimeInfo())
        val initialization = JSONObject(bridge.initialize(NUMOGRAM_SEED, NUMOGRAM_DIMENSION))
        val before = JSONObject(bridge.status())

        val origin = currentZone
        val context = EventModulePlanner.numogramContext(userText)

        // Numogram.py returns:
        // {"status":"transitioned","event":{...},"system":{...}}
        // Unwrap the actual transition event before planning/rendering.
        val transitionEnvelope =
            JSONObject(bridge.transition(origin, context.toString()))
        val transition = requireTransitionEvent(transitionEnvelope)
        currentZone = transition.getInt("to")
        val postTransition = JSONObject(bridge.status())

        val stagedModules = PythonModuleVault.list(applicationContext)
        val plan = EventModulePlanner.plan(
            userText = userText,
            transition = transition,
            availableModules = stagedModules
        )
        val moduleResults = EventModulePlanner.executeSelected(
            context = applicationContext,
            plan = plan,
            userText = userText,
            transition = transition
        )

        val credential = credentialAttestation()
        val result = JSONObject()
            .put("schema", "amelia-p3.11-chat-result-v1")
            .put("runtime", runtime)
            .put("initialization", initialization)
            .put("before", before)
            .put("input_field", context)
            .put("transition_envelope", transitionEnvelope)
            .put("transition", transition)
            .put("post_transition", postTransition)
            .put("event_plan", plan.toJson())
            .put("module_results", moduleResults)
            .put("credential", credential)

        if (!credential.optBoolean("usable", false)) {
            result.put("status", credential.optString("state", "unusable"))
            result.put("final", JSONObject(bridge.status()))
            return result.toString()
        }

        val prompt = P311MediatedChatPromptBuilder.build(
            messages = messages,
            transition = transition,
            eventPlan = plan.toJson(),
            moduleResults = moduleResults
        )

        // P3.10 deliberately raises the response ceiling from the earlier
        // 512-token renderer budget. One provider call is still sealed before
        // execution, but Amelia can now return a substantially fuller answer.
        val capsule = RenderCapsule.seal(
            traceDigest = prompt.traceDigest,
            payloadDigest = prompt.payloadDigest,
            rendererTemplateDigest = prompt.rendererTemplateDigest,
            maxTokens = 1600,
            tokenLimit = 1600,
            timeoutMs = 30_000,
            maxAttempts = 1
        )

        val transport = RenderTransport.execute(
            capsule,
            prompt.renderPrompt,
            BuildConfig.ANTHROPIC_API_KEY
        )

        // First Numogram read after the network call: a ground-truth
        // no-feedback check rather than a renderer self-report.
        val postRenderStatus = JSONObject(bridge.status())
        val noFeedbackHeld = sameEvolutionState(postTransition, postRenderStatus)
        val sealed = transport.sealed

        val expectedEvidenceToken = prompt.expectedEvidenceToken
        val evidenceExpected = expectedEvidenceToken != null
        val rawRenderedText = sealed?.parsedDisplayText ?: ""
        val moduleIncorporationHeld =
            expectedEvidenceToken?.let { rawRenderedText.contains(it) } ?: true
        val displayText = stripEvidenceToken(
            rawRenderedText,
            expectedEvidenceToken
        )

        result.put("capsule_digest", capsule.capsuleDigest)
        result.put("attempt_count", transport.attempts.size)
        result.put("transport_archive", transport.archiveJson())
        result.put("post_render_status", postRenderStatus)
        result.put("no_feedback_held", noFeedbackHeld)
        result.put("pfm_evidence_expected", evidenceExpected)
        result.put("pfm_relay_evidence_held", moduleIncorporationHeld)
        result.put(
            "pfm_interpretive_contribution",
            prompt.processFieldContribution ?: ""
        )
        result.put("final", postRenderStatus)

        if (sealed == null) {
            result.put("status", "transport_failed")
        } else {
            result.put("response_class", sealed.responseClass.name)
            result.put("http_status", sealed.httpStatus)
            result.put("rendered_text", displayText)
            result.put(
                "status",
                when {
                    sealed.responseClass.name != "SUCCESS_TEXT" ->
                        "terminal_response"
                    !noFeedbackHeld ->
                        "feedback_violation"
                    evidenceExpected && !moduleIncorporationHeld ->
                        "module_incorporation_failure"
                    else ->
                        "success"
                }
            )
        }
        return result.toString()
    }

    private fun renderChatResult(raw: String) {
        try {
            val result = JSONObject(raw)
            val transition = result.optJSONObject("transition")
            val plan = result.optJSONObject("event_plan")
            val modules = result.optJSONObject("module_results")

            if (transition != null && plan != null) {
                processView.text = buildString {
                    append("Transition: Z")
                    append(transition.optInt("from", -1))
                    append(" → Z")
                    append(transition.optInt("to", -1))
                    append("\nEvent: ")
                    append(plan.optString("event_type", "unspecified"))
                    append("\nModule families: ")
                    append(plan.optJSONArray("module_families")?.toString() ?: "[]")
                    append("\nSelected modules: ")
                    append(plan.optJSONArray("selected_modules")?.toString() ?: "[]")
                    append("\nModule results: ")
                    append(modules?.optJSONArray("results")?.length() ?: 0)

                    val pfm = extractProcessFieldMemoryPayload(modules)
                    if (pfm != null) {
                        append("\nPFM history depth: ")
                        append(pfm.optInt("history_depth", -1))
                        append("\nPFM dominant zone: Z")
                        append(pfm.optInt("dominant_zone", -1))
                        append("\nPFM contribution: ")
                        append(
                            pfm.optString(
                                "interpretive_contribution",
                                ""
                            ).take(280)
                        )
                        append("\nPFM relay evidence: ")
                        append(
                            result.optBoolean(
                                "pfm_relay_evidence_held",
                                false
                            )
                        )
                    } else {
                        append("\nPFM contribution: not staged/executed")
                    }

                    append("\nno_feedback_held: ")
                    append(result.optBoolean("no_feedback_held", false))
                }
            }

            when (result.optString("status", "")) {
                "success" -> {
                    val response = result.optString("rendered_text", "").trim()
                    if (response.isBlank()) {
                        statusView.text = "The language relay returned empty display text."
                    } else {
                        chatHistory += P311ChatMessage("assistant", response)
                        trimChatHistory()
                        renderChatHistory()
                        statusView.text =
                            "P3.11 event completed: transition committed, module synthesis completed, " +
                                "relay evidence verified when required, and language rendered without substrate feedback."
                    }
                }

                "missing" -> {
                    statusView.text =
                        "Numogram event completed locally. No API key is packaged, so no language relay call was made."
                }

                "mismatch", "noncanonical" -> {
                    statusView.text =
                        "Numogram event completed locally. Credential attestation blocked the language relay call."
                }

                "feedback_violation" -> {
                    statusView.text =
                        "P3.11 FAIL-CLOSED: post-render Numogram state differs from the sealed post-transition state."
                }

                "module_incorporation_failure" -> {
                    statusView.text =
                        "P3.11 FAIL-CLOSED: ProcessFieldMemory executed, but its relay evidence token was absent from the provider response."
                }

                "terminal_response" -> {
                    val responseClass =
                        result.optString("response_class", "UNKNOWN")
                    val httpStatus =
                        result.optInt("http_status", -1)

                    statusView.text =
                        "Numogram event completed. Language relay returned " +
                            "$responseClass (HTTP $httpStatus)."
                }

                "transport_failed" -> {
                    statusView.text =
                        "Numogram event completed. Language relay transport failed " +
                            "before a terminal provider response was received."
                }

                else -> {
                    statusView.text =
                        "Mediated chat failed closed: " + result.optString("message", raw.take(300))
                }
            }
        } catch (error: Throwable) {
            statusView.text = "Mediated result could not be parsed: ${error.message}"
        }
    }

    private fun renderChatHistory() {
        chatLogView.text = if (chatHistory.isEmpty()) {
            "No chat messages yet."
        } else {
            chatHistory.joinToString("\n\n") { message ->
                val label = if (message.role == "user") "You" else "Amelia"
                "$label:\n${message.content}"
            }
        }
    }

    private fun trimChatHistory() {
        while (chatHistory.size > 12) {
            chatHistory.removeAt(0)
        }
    }

    private fun requireTransitionEvent(envelope: JSONObject): JSONObject {
        val status = envelope.optString("status", "")
        if (status != "transitioned") {
            val errorType =
                envelope.optString("error_type", "NumogramTransitionError")
            val message =
                envelope.optString(
                    "message",
                    "Numogram transition did not complete."
                )
            throw IllegalStateException("$errorType: $message")
        }

        return envelope.optJSONObject("event")
            ?: throw IllegalStateException(
                "Numogram transition envelope is missing its event object."
            )
    }

    /**
     * Numogram.py get_status() returns:
     * {"status":"ready","init_digest":"...","system":{...}}
     *
     * Compare the actual nested substrate state. The earlier P3.10 activity
     * looked for these values on the outer envelope, causing a false
     * feedback violation on every successful request.
     */
    private fun sameEvolutionState(
        beforeRender: JSONObject,
        afterRender: JSONObject
    ): Boolean {
        val beforeSystem =
            beforeRender.optJSONObject("system") ?: return false
        val afterSystem =
            afterRender.optJSONObject("system") ?: return false

        val integerKeys = listOf(
            "seed",
            "dimension",
            "evolution_step",
            "transition_history"
        )

        return integerKeys.all { key ->
            beforeSystem.has(key) &&
                afterSystem.has(key) &&
                beforeSystem.optLong(key, Long.MIN_VALUE) ==
                    afterSystem.optLong(key, Long.MAX_VALUE)
        }
    }

    private fun stageBundledProcessFieldMemory() {
        try {
            val bytes = assets
                .open("p311/ProcessFieldMemory.py")
                .use { it.readBytes() }

            if (bytes.size > MAX_PICKED_MODULE_BYTES) {
                error("Bundled ProcessFieldMemory exceeds the 128 KiB vault limit.")
            }

            val record = PythonModuleVault.ingest(
                applicationContext,
                "ProcessFieldMemory.py",
                bytes
            )

            statusView.text =
                "ProcessFieldMemory.py staged through the vault audit. " +
                    "Its session-local field will begin with the next Numogram event."
            refreshModuleVault()
        } catch (rejected: ModuleRejectedException) {
            statusView.text =
                "Bundled ProcessFieldMemory was rejected: " +
                    rejected.findings.joinToString(" ")
        } catch (error: Throwable) {
            statusView.text =
                "Unable to stage ProcessFieldMemory: " +
                    (error.message ?: error::class.java.simpleName)
        }
    }

    private fun extractProcessFieldMemoryPayload(
        modules: JSONObject?
    ): JSONObject? {
        val results = modules?.optJSONArray("results") ?: return null

        for (index in 0 until results.length()) {
            val item = results.optJSONObject(index) ?: continue
            if (item.optString("file_name", "") != "ProcessFieldMemory.py") {
                continue
            }
            if (item.optString("status", "") != "executed") {
                continue
            }

            val output = item.optString("output", "")
            if (output.isBlank()) continue

            val parsed = try {
                JSONObject(output)
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

    private fun stripEvidenceToken(
        rawText: String,
        expectedToken: String?
    ): String {
        if (expectedToken.isNullOrBlank()) {
            return rawText.trim()
        }

        return rawText
            .replace(expectedToken, "")
            .trim()
    }

    private fun pickPythonModule() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "*/*"
            putExtra(
                Intent.EXTRA_MIME_TYPES,
                arrayOf("text/x-python", "text/plain", "application/octet-stream")
            )
        }
        startActivityForResult(intent, REQUEST_OPEN_PYTHON)
    }

    @Deprecated("Retained for API 24 compatibility in this minimal Activity.")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_OPEN_PYTHON || resultCode != RESULT_OK) return

        val uri = data?.data ?: return
        try {
            val displayName = selectedDisplayName(uri)
            val bytes = readPickedBytes(uri)
            val record = PythonModuleVault.ingest(applicationContext, displayName, bytes)
            statusView.text =
                "Module accepted: ${record.fileName}. It is eligible for P3.11 event planning."
            refreshModuleVault()
        } catch (rejected: ModuleRejectedException) {
            statusView.text = "Module rejected: ${rejected.findings.joinToString(" ")}"
        } catch (error: Throwable) {
            statusView.text =
                "Module import failed: ${error.message ?: error::class.java.simpleName}"
        }
    }

    private fun selectedDisplayName(uri: Uri): String {
        contentResolver.query(
            uri,
            arrayOf(OpenableColumns.DISPLAY_NAME),
            null,
            null,
            null
        )?.use { cursor ->
            if (cursor.moveToFirst()) {
                val index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (index >= 0) return cursor.getString(index)
            }
        }
        return uri.lastPathSegment ?: "uploaded_module.py"
    }

    private fun readPickedBytes(uri: Uri): ByteArray {
        val stream =
            contentResolver.openInputStream(uri)
                ?: error("Unable to open selected file.")

        stream.use { input ->
            val output = ByteArrayOutputStream()
            val buffer = ByteArray(8 * 1024)
            var total = 0

            while (true) {
                val count = input.read(buffer)
                if (count < 0) break
                total += count
                if (total > MAX_PICKED_MODULE_BYTES) {
                    error("Selected module exceeds the 128 KiB limit.")
                }
                output.write(buffer, 0, count)
            }
            return output.toByteArray()
        }
    }

    private fun refreshModuleVault() {
        val records = try {
            PythonModuleVault.list(applicationContext)
        } catch (error: Throwable) {
            moduleVaultView.text = "Unable to read module vault: ${error.message}"
            return
        }

        moduleVaultView.text = if (records.isEmpty()) {
            "No audited Python modules are staged. Tap STAGE PROCESS FIELD MEMORY to begin the P3.11 module assay."
        } else {
            records.joinToString("\n\n") { moduleRecordText(it) }
        }
    }

    private fun moduleRecordText(record: ModuleRecord): String = buildString {
        append(record.fileName)
        append("\n  sha256: ")
        append(record.digest.take(20))
        append("…\n  bytes: ")
        append(record.byteCount)
        append("\n  source status: ")
        append(record.sourceStatus)
        append("\n  P3.11: eligible for deterministic event-planner selection")
    }

    private fun setProviderCallInFlight(inFlight: Boolean) {
        providerCallInFlight = inFlight
        sendButton.isEnabled = !inFlight
    }

    private fun credentialAttestation(): JSONObject {
        val key = BuildConfig.ANTHROPIC_API_KEY
        val actualFingerprint = if (key.isBlank()) "missing" else sha256Hex(key)
        val expectedFingerprint = BuildConfig.CREDENTIAL_FINGERPRINT
        val expectedShape = BuildConfig.CREDENTIAL_SHAPE

        val keyShape = when {
            key.isBlank() -> "missing"
            key.startsWith("sk-ant-") && key.none { it.isWhitespace() } -> "canonical"
            else -> "noncanonical"
        }

        val state = when {
            key.isBlank() -> "missing"
            expectedShape != "canonical" || keyShape != "canonical" -> "noncanonical"
            expectedFingerprint == "missing" || expectedFingerprint != actualFingerprint -> "mismatch"
            else -> "usable"
        }

        return JSONObject()
            .put("schema", "amelia-p3.11-credential-attestation-v1")
            .put("state", state)
            .put("usable", state == "usable")
            .put("fingerprint", actualFingerprint)
            .put("build_fingerprint", expectedFingerprint)
            .put("shape", keyShape)
            .put("build_shape", expectedShape)
            .put("revision", BuildConfig.BUILD_REVISION)
    }

    private fun sha256Hex(input: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(input.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density).toInt()
}
