package com.amelia.p39

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
import com.amelia.renderer.ChatMessage
import com.amelia.renderer.ChatPromptBuilder
import com.amelia.renderer.FaithfulnessState
import com.amelia.renderer.RenderCapsule
import com.amelia.renderer.RenderPromptBuilder
import com.amelia.renderer.RenderTransport
import com.amelia.renderer.RendererFaithfulness
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.security.MessageDigest

/**
 * P3.9 combines three deliberately separate surfaces:
 *
 * 1. a display-only user chat lane;
 * 2. the prior sealed Numogram fork -> renderer assay, now with a
 *    renderer-faithfulness gate and authoritative branch table; and
 * 3. a staged Python-module vault.
 *
 * Conversation and uploaded source never become Numogram input. The only
 * calls to NumogramBridge are in executeSealedTrace(), which has no chat or
 * module-vault parameters. Uploaded source is not imported or executed.
 */
class MainActivity : Activity() {

    companion object {
        private const val LOG_TAG = "AMELIA_P39"
        private const val REQUEST_OPEN_PYTHON = 3901
        private const val MAX_PICKED_MODULE_BYTES = 128 * 1024
        private const val MAX_CHAT_INPUT_CHARS = 1_200
        private const val PROBE_SEED = 3606
        private const val PROBE_DIMENSION = 3
        private const val PROBE_ORIGIN = 3
    }

    private lateinit var statusView: TextView
    private lateinit var chatLogView: TextView
    private lateinit var chatInput: EditText
    private lateinit var sendButton: Button
    private lateinit var traceButton: Button
    private lateinit var sealedTableView: TextView
    private lateinit var traceResultView: TextView
    private lateinit var moduleVaultView: TextView

    private val chatHistory = mutableListOf<ChatMessage>()
    private var providerCallInFlight = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(22), dp(18), dp(28))
        }

        root.addView(
            TextView(this).apply {
                text = "AMELIA · P3.9"
                textSize = 25f
                gravity = Gravity.CENTER_HORIZONTAL
            }
        )
        root.addView(
            TextView(this).apply {
                text = "Chat · sealed trace renderer · staged Python module vault"
                textSize = 14f
                gravity = Gravity.CENTER_HORIZONTAL
                setPadding(0, dp(8), 0, dp(16))
            }
        )

        statusView = TextView(this).apply {
            text = "Ready. Chat is display-only; uploaded Python is staged, not run."
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
            maxLines = 5
            setPadding(dp(8), dp(8), dp(8), dp(8))
        }
        root.addView(chatInput)

        sendButton = actionButton("SEND CHAT") { sendChat() }
        root.addView(sendButton)

        root.addView(sectionHeading("SEALED TRACE RENDERER"))
        root.addView(
            TextView(this).apply {
                text =
                    "Runs the fixed P3.7 fork, seals one provider call, then displays " +
                        "the archived branch table alongside only faithful or explicitly " +
                        "labelled prose. No renderer output is routed to Numogram."
                textSize = 13f
                setPadding(dp(4), dp(4), dp(4), dp(8))
            }
        )
        traceButton = actionButton("RUN SEALED TRACE") { runSealedTrace() }
        root.addView(traceButton)

        sealedTableView = TextView(this).apply {
            text = "No sealed branch table yet."
            textSize = 13f
            setPadding(dp(4), dp(10), dp(4), dp(8))
        }
        traceResultView = TextView(this).apply {
            text = ""
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(sealedTableView)
        root.addView(traceResultView)

        root.addView(sectionHeading("PYTHON MODULE VAULT"))
        root.addView(
            TextView(this).apply {
                text =
                    "Pick a UTF-8 .py file. P3.9 hashes it, applies a conservative " +
                        "source-policy audit, and copies it to app-private storage. It is " +
                        "not placed on Python's import path and is never executed here."
                textSize = 13f
                setPadding(dp(4), dp(4), dp(4), dp(8))
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

        root.addView(
            TextView(this).apply {
                text =
                    "P3.9 boundaries:\n\n" +
                        "Chat text → sealed display capsule → provider → screen\n" +
                        "(never NumogramBridge)\n\n" +
                        "Fixed trace → NumogramBridge → sealed branch table → " +
                        "faithfulness gate → screen\n" +
                        "(renderer never feeds back)\n\n" +
                        "Picked .py → hash + source audit → app-private vault\n" +
                        "(never sys.path, import, or execution)\n\n" +
                        "The direct provider credential is attested before each call. " +
                        "A missing or mismatched key causes no network call."
                textSize = 13f
                setPadding(dp(4), dp(10), dp(4), 0)
            }
        )

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
            statusView.text = "A sealed provider call is already in progress."
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

        val userMessage = ChatMessage("user", userText)
        chatHistory += userMessage
        trimChatHistory()
        chatInput.setText("")
        renderChatHistory()
        setProviderCallInFlight(true)
        statusView.text = "Chat capsule sealed. Making one display-only provider call…"

        val snapshot = chatHistory.toList()
        Thread {
            val result = try {
                executeChat(snapshot)
            } catch (error: Throwable) {
                JSONObject()
                    .put("schema", "amelia-p3.9-chat-result-v1")
                    .put("status", "error")
                    .put("error_type", error::class.java.simpleName)
                    .put("message", error.message ?: "Unknown chat error")
                    .toString()
            }
            Log.i(LOG_TAG, result)
            runOnUiThread {
                renderChatResult(result)
                setProviderCallInFlight(false)
            }
        }.start()
    }

    /** This function has no NumogramBridge reference: chat cannot become a
     * substrate command path by an accidental parameter or helper call. */
    private fun executeChat(messages: List<ChatMessage>): String {
        val credential = credentialAttestation()
        val result = JSONObject()
            .put("schema", "amelia-p3.9-chat-result-v1")
            .put("credential", credential)

        if (!credential.optBoolean("usable", false)) {
            result.put("status", credential.optString("state", "unusable"))
            return result.toString()
        }

        val prompt = ChatPromptBuilder.build(messages)
        val capsule = RenderCapsule.seal(
            traceDigest = prompt.traceDigest,
            payloadDigest = prompt.payloadDigest,
            rendererTemplateDigest = prompt.rendererTemplateDigest,
            maxAttempts = 1
        )
        val transport = RenderTransport.execute(
            capsule,
            prompt.renderPrompt,
            BuildConfig.ANTHROPIC_API_KEY
        )
        val sealed = transport.sealed

        result.put("capsule_digest", capsule.capsuleDigest)
        result.put("attempt_count", transport.attempts.size)
        result.put("transport_archive", transport.archiveJson())
        if (sealed == null) {
            result.put("status", "transport_failed")
        } else {
            result.put("response_class", sealed.responseClass.name)
            result.put("http_status", sealed.httpStatus)
            result.put("rendered_text", sealed.parsedDisplayText)
            result.put(
                "status",
                if (sealed.responseClass.name == "SUCCESS_TEXT") "success" else "terminal_response"
            )
        }
        return result.toString()
    }

    private fun renderChatResult(raw: String) {
        try {
            val result = JSONObject(raw)
            when (result.optString("status", "")) {
                "success" -> {
                    val response = result.optString("rendered_text", "").trim()
                    if (response.isBlank()) {
                        statusView.text = "Chat response was empty; it was not added to the transcript."
                    } else {
                        chatHistory += ChatMessage("assistant", response.take(MAX_CHAT_INPUT_CHARS))
                        trimChatHistory()
                        renderChatHistory()
                        statusView.text =
                            "Chat response displayed from one sealed, display-only call. " +
                                "It did not invoke Numogram or an uploaded module."
                    }
                }
                "missing" -> {
                    statusView.text = "No API key is packaged, so no chat network call was attempted."
                }
                "mismatch", "noncanonical" -> {
                    statusView.text =
                        "Credential attestation did not pass, so no chat network call was attempted."
                }
                "terminal_response", "transport_failed" -> {
                    statusView.text =
                        "Chat did not return display text. " +
                            "The one-call terminal archive is shown below."
                    traceResultView.text = terminalDiagnostic(
                        result.optJSONObject("transport_archive")
                            ?.optJSONObject("terminal_attempt")
                    )
                }
                else -> {
                    statusView.text =
                        "Chat failed closed: " + result.optString("message", raw.take(300))
                }
            }
        } catch (error: Throwable) {
            statusView.text = "Chat result could not be parsed: ${error.message}"
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

    private fun runSealedTrace() {
        if (providerCallInFlight) {
            statusView.text = "A sealed provider call is already in progress."
            return
        }
        setProviderCallInFlight(true)
        statusView.text = "Computing fixed Numogram trace, then sealing one renderer call…"
        traceResultView.text = ""

        Thread {
            val raw = try {
                executeSealedTrace()
            } catch (error: Throwable) {
                JSONObject()
                    .put("schema", "amelia-p3.9-trace-result-v1")
                    .put("status", "error")
                    .put("error_type", error::class.java.simpleName)
                    .put("message", error.message ?: "Unknown trace error")
                    .toString()
            }
            Log.i(LOG_TAG, raw)
            runOnUiThread {
                renderTraceResult(raw)
                setProviderCallInFlight(false)
            }
        }.start()
    }

    private fun executeSealedTrace(): String {
        val bridge = NumogramBridge(applicationContext)
        val runtime = JSONObject(bridge.runtimeInfo())
        val before = JSONObject(bridge.status())
        val initialized = JSONObject(bridge.initialize(PROBE_SEED, PROBE_DIMENSION))
        val ready = JSONObject(bridge.status())
        val transitioned = JSONObject(bridge.transition(PROBE_ORIGIN, "{}"))
        val forked = JSONObject(bridge.runFork(PROBE_ORIGIN, "{}"))
        val verified = JSONObject(bridge.verifyLastFork())
        val postForkStatus = JSONObject(bridge.status())
        val credential = credentialAttestation()

        val result = JSONObject()
            .put("schema", "amelia-p3.9-trace-result-v1")
            .put("runtime", runtime)
            .put("before", before)
            .put("initialized", initialized)
            .put("ready", ready)
            .put("transitioned", transitioned)
            .put("forked", forked)
            .put("verified", verified)
            .put("post_fork_status", postForkStatus)
            .put("credential", credential)

        if (!credential.optBoolean("usable", false)) {
            result.put("status", credential.optString("state", "unusable"))
            result.put("final", JSONObject(bridge.status()))
            return result.toString()
        }

        val prompt = RenderPromptBuilder.buildFromForkResult(forked)
        val capsule = RenderCapsule.seal(
            traceDigest = prompt.traceDigest,
            payloadDigest = prompt.payloadDigest,
            rendererTemplateDigest = prompt.rendererTemplateDigest,
            maxAttempts = 1
        )
        val transport = RenderTransport.execute(
            capsule,
            prompt.renderPrompt,
            BuildConfig.ANTHROPIC_API_KEY
        )
        // This is deliberately the first Numogram call after the renderer.
        // It is the ground-truth no-feedback check, not a self-report from
        // the transport object.
        val postRenderStatus = JSONObject(bridge.status())
        val sealed = transport.sealed

        result.put("capsule_digest", capsule.capsuleDigest)
        result.put("model", capsule.model)
        result.put("attempt_count", transport.attempts.size)
        result.put("transport_archive", transport.archiveJson())
        result.put("post_render_status", postRenderStatus)
        result.put("final", postRenderStatus)
        if (sealed == null) {
            result.put("status", "transport_failed")
        } else {
            result.put("response_class", sealed.responseClass.name)
            result.put("http_status", sealed.httpStatus)
            result.put("rendered_text", sealed.parsedDisplayText)
            result.put(
                "status",
                if (sealed.responseClass.name == "PROVIDER_REJECTED") {
                    "provider_rejected"
                } else {
                    "completed"
                }
            )
        }
        return result.toString()
    }

    private fun renderTraceResult(raw: String) {
        try {
            val result = JSONObject(raw)
            val forked = result.optJSONObject("forked")
                ?: throw IllegalStateException("Missing sealed fork result")
            sealedTableView.text = RendererFaithfulness.branchTable(forked)

            val coreHeld = traceCoreHeld(result)
            val status = result.optString("status", "")
            if (status == "missing") {
                statusView.text = "P3.9 TRACE READY — no API key is configured."
                traceResultView.text =
                    "The sealed branch table above was computed locally. No provider call was attempted."
                return
            }
            if (status == "mismatch" || status == "noncanonical") {
                statusView.text = "P3.9 TRACE STOPPED — credential attestation did not pass."
                traceResultView.text =
                    "The branch table is local. The renderer was not called.\n\n" +
                        credentialText(result.optJSONObject("credential"))
                return
            }

            val noFeedbackHeld = noFeedbackHeld(result)
            when (status) {
                "provider_rejected", "transport_failed" -> {
                    statusView.text = "P3.9 TRACE FAIL-CLOSED"
                    traceResultView.text =
                        "Core trace held: $coreHeld\n" +
                            "no_feedback_held: $noFeedbackHeld\n\n" +
                            terminalDiagnostic(
                                result.optJSONObject("transport_archive")
                                    ?.optJSONObject("terminal_attempt")
                            )
                }
                "completed" -> {
                    val responseClass = result.optString("response_class", "")
                    val rendererText = result.optString("rendered_text", "")
                    if (responseClass != "SUCCESS_TEXT") {
                        statusView.text = "P3.9 TRACE COMPLETE — $responseClass"
                        traceResultView.text =
                            "The transport completed without display text.\n" +
                                "Core trace held: $coreHeld\n" +
                                "no_feedback_held: $noFeedbackHeld"
                        return
                    }

                    val verdict = RendererFaithfulness.verify(forked, rendererText)
                    when (verdict.state) {
                        FaithfulnessState.VERIFIED -> {
                            statusView.text = if (coreHeld && noFeedbackHeld) {
                                "P3.9 TRACE VERIFIED ✓"
                            } else {
                                "P3.9 TRACE FAIL-CLOSED"
                            }
                            traceResultView.text =
                                "Renderer faithfulness: ${verdict.summary()}\n" +
                                    "Core trace held: $coreHeld\n" +
                                    "no_feedback_held: $noFeedbackHeld\n" +
                                    "Capsule: ${result.optString("capsule_digest", "").take(16)}…\n\n" +
                                    "Rendered prose:\n\n${verdict.narrative}"
                        }
                        FaithfulnessState.CONTRADICTION_DETECTED -> {
                            statusView.text = "P3.9 RENDER REJECTED"
                            traceResultView.text =
                                "Renderer faithfulness: ${verdict.summary()}\n" +
                                    "Core trace held: $coreHeld\n" +
                                    "no_feedback_held: $noFeedbackHeld\n\n" +
                                    "Reasons:\n${verdict.reasons.joinToString("\n") { "• $it" }}\n\n" +
                                    "The provider prose is not displayed as a trace rendering and " +
                                    "will not be retried. The sealed table remains authoritative."
                        }
                        FaithfulnessState.UNVERIFIABLE -> {
                            statusView.text = "P3.9 RENDER LABELLED"
                            traceResultView.text =
                                "Renderer faithfulness: ${verdict.summary()}\n" +
                                    "Core trace held: $coreHeld\n" +
                                    "no_feedback_held: $noFeedbackHeld\n\n" +
                                    "Reasons:\n${verdict.reasons.joinToString("\n") { "• $it" }}\n\n" +
                                    "Provider prose (unverified, display-only):\n\n" +
                                    verdict.narrative.take(4_000)
                        }
                    }
                }
                else -> {
                    statusView.text = "P3.9 TRACE FAIL-CLOSED"
                    traceResultView.text = result.optString("message", raw.take(2_000))
                }
            }
        } catch (error: Throwable) {
            statusView.text = "P3.9 TRACE FAIL-CLOSED"
            traceResultView.text =
                "Trace result could not be parsed: ${error.message}\n\n${raw.take(2_000)}"
        }
    }

    private fun traceCoreHeld(result: JSONObject): Boolean {
        val runtime = result.optJSONObject("runtime") ?: return false
        val initialized = result.optJSONObject("initialized") ?: return false
        val transitioned = result.optJSONObject("transitioned") ?: return false
        val forked = result.optJSONObject("forked") ?: return false
        val verified = result.optJSONObject("verified") ?: return false
        val initStatus = initialized.optString("status", "")
        val initHeld = initStatus == "initialized" ||
            (initStatus == "already_initialized" && initialized.optBoolean("state_unchanged", false))

        return runtime.optString("status", "") == "torch_ready" &&
            runtime.optString("torch_version", "").startsWith("1.8.1") &&
            initHeld &&
            transitioned.optString("status", "") == "transitioned" &&
            forked.optString("status", "") == "forked" &&
            verified.optString("status", "") == "verified" &&
            verified.optJSONArray("mismatched_branches")?.length() == 0
    }

    private fun noFeedbackHeld(result: JSONObject): Boolean {
        val before = result.optJSONObject("post_fork_status")
            ?.optJSONObject("system") ?: return false
        val after = result.optJSONObject("post_render_status")
            ?.optJSONObject("system") ?: return false
        return before.optInt("evolution_step", -1) == after.optInt("evolution_step", -2) &&
            before.optInt("transition_history", -1) == after.optInt("transition_history", -2)
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

    @Deprecated("Android's Activity Result API would require an AndroidX dependency not used by this isolated build.")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_OPEN_PYTHON || resultCode != RESULT_OK) return
        val uri = data?.data ?: run {
            statusView.text = "No module document was returned by the picker."
            return
        }
        statusView.text = "Auditing and staging selected Python source…"
        Thread {
            val outcome = try {
                val displayName = documentDisplayName(uri)
                val bytes = readBoundedDocument(uri, MAX_PICKED_MODULE_BYTES)
                val record = PythonModuleVault.ingest(applicationContext, displayName, bytes)
                "staged" to record
            } catch (error: ModuleRejectedException) {
                "rejected" to error
            } catch (error: Throwable) {
                "error" to error
            }
            runOnUiThread {
                when (outcome.first) {
                    "staged" -> {
                        val record = outcome.second as ModuleRecord
                        statusView.text =
                            "Module staged: ${record.fileName} (${record.digest.take(16)}…). " +
                                "It was not imported or executed."
                    }
                    "rejected" -> {
                        val error = outcome.second as ModuleRejectedException
                        statusView.text = "Module rejected by the P3.9 source policy."
                        moduleVaultView.text =
                            "Rejected source was not stored.\n\n" +
                                error.findings.joinToString("\n") { "• $it" }
                    }
                    else -> {
                        val error = outcome.second as Throwable
                        statusView.text = "Module upload failed: ${error.message ?: "unknown error"}"
                    }
                }
                refreshModuleVault()
            }
        }.start()
    }

    private fun documentDisplayName(uri: Uri): String {
        contentResolver.query(
            uri,
            arrayOf(OpenableColumns.DISPLAY_NAME),
            null,
            null,
            null
        )?.use { cursor ->
            val nameColumn = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
            if (nameColumn >= 0 && cursor.moveToFirst()) {
                val value = cursor.getString(nameColumn)
                if (!value.isNullOrBlank()) return value
            }
        }
        return "uploaded_module.py"
    }

    private fun readBoundedDocument(uri: Uri, maximumBytes: Int): ByteArray {
        val stream = contentResolver.openInputStream(uri)
            ?: throw IllegalStateException("Unable to open the selected document.")
        return stream.use { input ->
            val output = ByteArrayOutputStream()
            val buffer = ByteArray(8_192)
            while (true) {
                val count = input.read(buffer)
                if (count < 0) break
                if (output.size() + count > maximumBytes) {
                    throw IllegalArgumentException("Selected module exceeds $maximumBytes bytes.")
                }
                output.write(buffer, 0, count)
            }
            output.toByteArray()
        }
    }

    private fun refreshModuleVault() {
        Thread {
            val records = try {
                PythonModuleVault.list(applicationContext)
            } catch (error: Throwable) {
                emptyList<ModuleRecord>()
            }
            runOnUiThread {
                moduleVaultView.text = moduleVaultText(records)
            }
        }.start()
    }

    private fun moduleVaultText(records: List<ModuleRecord>): String {
        if (records.isEmpty()) {
            return "No staged modules. Pick a .py file to copy it into the app-private vault."
        }
        return buildString {
            append("Staged modules (none are active):\n")
            records.forEach { record ->
                append("• ")
                append(record.fileName)
                append(" · ")
                append(record.byteCount)
                append(" bytes · ")
                append(record.digest.take(16))
                append("…\n  ")
                append(record.sourceStatus)
                append('\n')
            }
        }
    }

    private fun setProviderCallInFlight(inFlight: Boolean) {
        providerCallInFlight = inFlight
        sendButton.isEnabled = !inFlight
        traceButton.isEnabled = !inFlight
    }

    private fun credentialAttestation(): JSONObject {
        val apiKey = BuildConfig.ANTHROPIC_API_KEY
        if (apiKey.isBlank()) {
            return JSONObject()
                .put("state", "missing")
                .put("usable", false)
        }

        val apkFingerprint = sha256Hex(apiKey)
        val runnerFingerprint = BuildConfig.CREDENTIAL_FINGERPRINT
        val canonical = apiKey.startsWith("sk-ant-") && apiKey.none { it.isWhitespace() }
        val fingerprintMatches = runnerFingerprint == apkFingerprint
        val shapeMatches = BuildConfig.CREDENTIAL_SHAPE == "canonical" && canonical
        val state = when {
            !fingerprintMatches -> "mismatch"
            !shapeMatches -> "noncanonical"
            else -> "usable"
        }
        return JSONObject()
            .put("state", state)
            .put("usable", state == "usable")
            .put("fingerprint_matches", fingerprintMatches)
            .put("shape_matches", shapeMatches)
            .put("apk_fingerprint_prefix", apkFingerprint.take(16))
            .put("build_revision", BuildConfig.BUILD_REVISION)
    }

    private fun credentialText(credential: JSONObject?): String {
        if (credential == null) return "Credential attestation missing."
        return "Credential state: ${credential.optString("state", "unknown")}\n" +
            "Runner/APK fingerprint match: ${credential.optBoolean("fingerprint_matches", false)}\n" +
            "Canonical key shape: ${credential.optBoolean("shape_matches", false)}"
    }

    private fun terminalDiagnostic(terminal: JSONObject?): String {
        if (terminal == null) return "Transport archive is missing."
        val status = terminal.optInt("http_status", -1)
        val statusText = if (status >= 0) status.toString() else "not received"
        val preview = terminal.optString("raw_response_preview", "").take(1_500)
        return buildString {
            append("Terminal transport archive (display-only):\n\n")
            append("Attempt: ${terminal.optInt("attempt_number", -1)}\n")
            append("HTTP status: $statusText\n")
            append("Response class: ${terminal.optString("response_class", "")}\n")
            append("Error type: ${terminal.optString("error_type", "")}\n")
            append("Error message: ${terminal.optString("error_message", "")}\n")
            append("Raw response recorded: ${terminal.optBoolean("raw_response_recorded", false)}\n")
            append("Raw SHA-256: ${terminal.optString("raw_response_digest", "")}\n\n")
            append("Provider response preview:\n")
            append(if (preview.isBlank()) "(no response body received)" else preview)
        }
    }

    private fun sha256Hex(value: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(value.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density).toInt()
}
