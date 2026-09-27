package com.amelia.p313

import android.app.Activity
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.assay.P312AssayBridge
import com.amelia.renderer.P312PromptBuilder
import com.amelia.renderer.P313RendererFaithfulness
import com.amelia.renderer.RenderCapsule
import com.amelia.renderer.RenderTransport
import org.json.JSONObject
import java.security.MessageDigest

/**
 * Amelia P3.13 — renderer-faithfulness validation.
 *
 * P3.12 is deliberately preserved as the upstream causal assay. P3.13 adds:
 *   1. PRE_RENDER archival of the exact Event-2 relay prompt/payload.
 *   2. POST_RENDER archival of the returned provider text.
 *   3. A deterministic closed-set contradiction audit.
 *   4. A deliberate-false-text positive control.
 *   5. Verification of the P3.13 SHA-256 archive chain.
 *
 * This Activity belongs to applicationId com.amelia.p313, so the APK installs
 * beside the frozen P3.12 package com.amelia.p312 rather than replacing it.
 */
class MainActivity : Activity() {

    companion object {
        private const val NUMOGRAM_SEED = 3606
        private const val NUMOGRAM_DIMENSION = 3

        private const val CONDITION_A = "A_ABSENT"
        private const val CONDITION_B = "B_RETAINED"
        private const val CONDITION_C = "C_RESET"
    }

    private lateinit var promptOneView: EditText
    private lateinit var promptTwoView: EditText
    private lateinit var runButton: Button
    private lateinit var statusView: TextView
    private lateinit var endpointView: TextView
    private lateinit var auditView: TextView
    private lateinit var responsesView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(22), dp(18), dp(28))
        }

        root.addView(TextView(this).apply {
            text = "AMELIA · P3.13"
            textSize = 25f
            gravity = Gravity.CENTER_HORIZONTAL
        })

        root.addView(TextView(this).apply {
            text =
                "Renderer-faithfulness validation · " +
                    "side-by-side package"
            textSize = 14f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(8), 0, dp(16))
        })

        statusView = TextView(this).apply {
            text =
                "Ready. P3.12 remains the frozen upstream causal assay. " +
                    "P3.13 seals each Event-2 relay payload before rendering " +
                    "and audits the returned prose afterwards."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(statusView)

        root.addView(sectionHeading("CONDITIONING PROMPT · EVENT 1"))
        promptOneView = EditText(this).apply {
            setText("What is the significance of 333 in the Numogram?")
            minLines = 2
            maxLines = 5
            textSize = 15f
        }
        root.addView(promptOneView)

        root.addView(sectionHeading("CRITICAL PROMPT · EVENT 2"))
        promptTwoView = EditText(this).apply {
            setText(
                "Is intelligence the transition between states " +
                    "or the memory of that transition?"
            )
            minLines = 2
            maxLines = 5
            textSize = 15f
        }
        root.addView(promptTwoView)

        runButton = Button(this).apply {
            text = "RUN P3.13 A / B / C FAITHFULNESS ASSAY"
            setOnClickListener { runMatchedAssay() }
        }
        root.addView(runButton)

        root.addView(sectionHeading("P3.12 PRIMARY CAUSAL ENDPOINT"))
        endpointView = TextView(this).apply {
            text = "No assay run yet."
            textSize = 13f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(endpointView)

        root.addView(sectionHeading("P3.13 RENDERER-FAITHFULNESS GATE"))
        auditView = TextView(this).apply {
            text = "No renderer audit run yet."
            textSize = 13f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(auditView)

        root.addView(sectionHeading("SECOND-EVENT LANGUAGE REALIZATIONS"))
        responsesView = TextView(this).apply {
            text =
                "A, B and C responses will appear here after the " +
                    "P3.12 matched causal endpoint passes."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(responsesView)

        root.addView(TextView(this).apply {
            text =
                "Installed package: com.amelia.p313\n" +
                    "Frozen P3.12 package: com.amelia.p312\n\n" +
                    "P3.13 does not modify the Numogram, PFM intervention, " +
                    "or P3.12 primary endpoint. It archives exactly what is " +
                    "sent to the renderer, then archives and audits what the " +
                    "renderer returns."
            textSize = 12f
            setPadding(dp(4), dp(14), dp(4), 0)
        })

        scroll.addView(root)
        setContentView(scroll)
    }

    private fun runMatchedAssay() {
        val promptOne = promptOneView.text.toString().trim()
        val promptTwo = promptTwoView.text.toString().trim()

        if (promptOne.isBlank() || promptTwo.isBlank()) {
            statusView.text = "Both assay prompts are required."
            return
        }

        runButton.isEnabled = false
        statusView.text =
            "Running frozen P3.12 causal assay, then P3.13 renderer audit…"
        endpointView.text = "Assay in progress."
        auditView.text = "Waiting for pre-render seals."
        responsesView.text = "Waiting for matched transition check…"

        Thread {
            val raw = try {
                executeAssay(promptOne, promptTwo)
            } catch (error: Throwable) {
                JSONObject()
                    .put("schema", "amelia-p3.13-android-result-v1")
                    .put("status", "error")
                    .put("error_type", error::class.java.simpleName)
                    .put(
                        "message",
                        error.message ?: "Unknown P3.13 error"
                    )
                    .toString()
            }

            runOnUiThread {
                renderAssay(raw)
                runButton.isEnabled = true
            }
        }.start()
    }

    private fun executeAssay(
        promptOne: String,
        promptTwo: String
    ): String {
        val bridge = P312AssayBridge(applicationContext)

        // Frozen P3.12 upstream assay.
        val assay =
            JSONObject(
                bridge.runAssay(
                    promptOne,
                    promptTwo,
                    NUMOGRAM_SEED,
                    NUMOGRAM_DIMENSION
                )
            )

        val endpoint = assay.getJSONObject("primary_endpoint")
        val primaryHeld =
            endpoint.optBoolean(
                "causal_memory_contrast_held",
                false
            )

        val result = JSONObject()
            .put("schema", "amelia-p3.13-android-result-v1")
            .put("assay", assay)
            .put("primary_endpoint_held", primaryHeld)

        // Fail closed before any provider call, exactly as P3.12.
        if (!primaryHeld) {
            result.put("status", "primary_endpoint_failed")
            return result.toString()
        }

        val credential = credentialAttestation()
        result.put("credential", credential)

        if (!credential.optBoolean("usable", false)) {
            result.put(
                "status",
                credential.optString("state", "unusable")
            )
            return result.toString()
        }

        val p313RunId = P313RendererFaithfulness.newRunId()
        result.put("p313_run_id", p313RunId)

        val branches = assay.getJSONObject("branches")
        val rendered = JSONObject()

        listOf(
            CONDITION_A,
            CONDITION_B,
            CONDITION_C
        ).forEach { condition ->
            val branch = branches.getJSONObject(condition)
            rendered.put(
                condition,
                renderCriticalEvent(
                    bridge = bridge,
                    runId = p313RunId,
                    condition = condition,
                    promptOne = promptOne,
                    promptTwo = promptTwo,
                    branch = branch
                )
            )
        }

        result.put("rendered_branches", rendered)

        val allIsolationHeld =
            listOf(
                CONDITION_A,
                CONDITION_B,
                CONDITION_C
            ).all { condition ->
                rendered
                    .getJSONObject(condition)
                    .optBoolean(
                        "numogram_state_unchanged",
                        false
                    )
            }

        val bEvidenceHeld =
            rendered
                .getJSONObject(CONDITION_B)
                .optBoolean("pfm_relay_evidence_held", false)

        val cEvidenceHeld =
            rendered
                .getJSONObject(CONDITION_C)
                .optBoolean("pfm_relay_evidence_held", false)

        val p312DownstreamHeld =
            allIsolationHeld &&
                bEvidenceHeld &&
                cEvidenceHeld

        val allRealAuditsClean =
            listOf(
                CONDITION_A,
                CONDITION_B,
                CONDITION_C
            ).all { condition ->
                rendered
                    .getJSONObject(condition)
                    .optInt(
                        "p313_contradiction_count",
                        -1
                    ) == 0
            }

        val positiveControl =
            P313RendererFaithfulness.positiveControl()

        val archiveChainValid =
            P313RendererFaithfulness.verifyArchiveChain(
                applicationContext,
                p313RunId
            )

        val p313Held =
            primaryHeld &&
                p312DownstreamHeld &&
                allRealAuditsClean &&
                positiveControl &&
                archiveChainValid

        result.put(
            "all_numogram_isolation_held",
            allIsolationHeld
        )
        result.put(
            "b_relay_evidence_held",
            bEvidenceHeld
        )
        result.put(
            "c_relay_evidence_held",
            cEvidenceHeld
        )
        result.put(
            "p312_downstream_held",
            p312DownstreamHeld
        )
        result.put(
            "p313_all_real_audits_clean",
            allRealAuditsClean
        )
        result.put(
            "p313_positive_control_held",
            positiveControl
        )
        result.put(
            "p313_archive_hash_chain_valid",
            archiveChainValid
        )
        result.put(
            "p313_renderer_faithfulness_held",
            p313Held
        )

        result.put(
            "status",
            when {
                !p312DownstreamHeld ->
                    "downstream_validation_failed"
                !p313Held ->
                    "renderer_faithfulness_failed"
                else ->
                    "success"
            }
        )

        return result.toString()
    }

    private fun renderCriticalEvent(
        bridge: P312AssayBridge,
        runId: String,
        condition: String,
        promptOne: String,
        promptTwo: String,
        branch: JSONObject
    ): JSONObject {
        val eventOne = branch.getJSONObject("event_one")
        val eventTwo = branch.getJSONObject("event_two")
        val pfmEventTwo = branch.optJSONObject("pfm_event_two")

        val prompt = P312PromptBuilder.build(
            conditioningPrompt = promptOne,
            criticalPrompt = promptTwo,
            eventOne = eventOne,
            eventTwo = eventTwo,
            pfmEventTwo = pfmEventTwo
        )

        val transitionPath = listOf(
            eventOne.getInt("from"),
            eventOne.getInt("to"),
            eventTwo.getInt("to")
        )

        val shortBranch = when (condition) {
            CONDITION_A -> "A"
            CONDITION_B -> "B"
            CONDITION_C -> "C"
            else -> error("Unknown P3.13 condition: $condition")
        }

        val pfmMode = when (condition) {
            CONDITION_A ->
                P313RendererFaithfulness.PfmMode.ABSENT
            CONDITION_B ->
                P313RendererFaithfulness.PfmMode.RETAINED
            CONDITION_C ->
                P313RendererFaithfulness.PfmMode.RESET
            else ->
                error("Unknown P3.13 condition: $condition")
        }

        val expectedToken = prompt.expectedEvidenceToken

        val p313Payload =
            P313RendererFaithfulness.BranchPayload(
                runId = runId,
                branch = shortBranch,
                event = 2,
                pfmMode = pfmMode,
                processFieldHistoryDepth =
                    prompt.processFieldHistoryDepth,
                processFieldContribution =
                    prompt.processFieldContribution != null,
                relayEvidenceExpected =
                    if (expectedToken == null) null else true,
                numogramUnchangedExpected = true,
                transitionPath = transitionPath,
                traceDigest = prompt.traceDigest,
                upstreamPayloadDigest = prompt.payloadDigest,
                rendererTemplateDigest =
                    prompt.rendererTemplateDigest,
                expectedEvidenceToken =
                    expectedToken ?: "",
                renderPrompt = prompt.renderPrompt
            )

        // P3.13 critical ordering: seal the exact relay payload before the call.
        val preRenderPayloadSha =
            P313RendererFaithfulness.archivePreRender(
                applicationContext,
                p313Payload
            )

        val capsule = RenderCapsule.seal(
            traceDigest = prompt.traceDigest,
            payloadDigest = prompt.payloadDigest,
            rendererTemplateDigest =
                prompt.rendererTemplateDigest,
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

        val sealed = transport.sealed
        val rawText = sealed?.parsedDisplayText ?: ""

        // P3.13 critical ordering: returned prose is archived/audited after call.
        val p313Audit =
            P313RendererFaithfulness.auditAndArchive(
                applicationContext,
                p313Payload,
                rawText
            )

        val evidenceExpected = expectedToken != null
        val evidenceHeld =
            if (expectedToken == null) {
                true
            } else {
                rawText.contains(expectedToken)
            }

        val displayText =
            stripEvidenceToken(rawText, expectedToken)

        // Existing P3.12 isolation check remains after rendering.
        val postRenderStatus =
            JSONObject(bridge.branchStatus(condition))

        val numogramStateUnchanged =
            postRenderStatus.optBoolean(
                "state_unchanged_from_seal",
                false
            )

        return JSONObject()
            .put("condition", condition)
            .put(
                "response_class",
                sealed?.responseClass?.name ?: "NO_RESPONSE"
            )
            .put(
                "http_status",
                sealed?.httpStatus ?: -1
            )
            .put(
                "rendered_text",
                displayText
            )
            .put(
                "rendered_text_sha256",
                sha256Hex(displayText)
            )
            .put(
                "raw_provider_text_sha256",
                p313Audit.proseSha256
            )
            .put(
                "pfm_evidence_expected",
                evidenceExpected
            )
            .put(
                "pfm_relay_evidence_held",
                evidenceHeld
            )
            .put(
                "pfm_history_depth",
                prompt.processFieldHistoryDepth
                    ?: JSONObject.NULL
            )
            .put(
                "pfm_interpretive_contribution",
                prompt.processFieldContribution ?: ""
            )
            .put(
                "numogram_state_unchanged",
                numogramStateUnchanged
            )
            .put(
                "post_render_branch_status",
                postRenderStatus
            )
            .put(
                "transport_archive",
                transport.archiveJson()
            )
            .put(
                "p313_pre_render_payload_archived",
                true
            )
            .put(
                "p313_payload_sha256",
                preRenderPayloadSha
            )
            .put(
                "p313_audit_status",
                p313Audit.status
            )
            .put(
                "p313_contradiction_count",
                p313Audit.contradictionCount
            )
            .put(
                "p313_archive_record_sha256",
                p313Audit.archiveRecordSha256
            )
            .put(
                "p313_archive_file",
                p313Audit.archiveFile
            )
    }

    private fun renderAssay(raw: String) {
        try {
            val result = JSONObject(raw)
            val assay = result.optJSONObject("assay")
            val endpoint = assay?.optJSONObject("primary_endpoint")

            if (endpoint != null) {
                endpointView.text = buildString {
                    append("Event 1 identical A/B/C: ")
                    append(
                        endpoint.optBoolean(
                            "event_one_identical_across_conditions",
                            false
                        )
                    )
                    append("\nEvent 2 identical A/B/C: ")
                    append(
                        endpoint.optBoolean(
                            "event_two_identical_across_conditions",
                            false
                        )
                    )
                    append("\nA PFM absent: ")
                    append(
                        endpoint.optBoolean(
                            "a_pfm_absent",
                            false
                        )
                    )
                    append("\nB event-2 history depth: ")
                    append(
                        endpoint.optInt(
                            "b_second_history_depth",
                            -1
                        )
                    )
                    append("\nC event-2 history depth: ")
                    append(
                        endpoint.optInt(
                            "c_second_history_depth",
                            -1
                        )
                    )
                    append("\nCAUSAL MEMORY CONTRAST: ")
                    append(
                        endpoint.optBoolean(
                            "causal_memory_contrast_held",
                            false
                        )
                    )
                }
            }

            when (result.optString("status", "")) {
                "success" -> {
                    statusView.text =
                        "P3.13 PASS: P3.12 remained intact; exact relay " +
                            "payloads were archived before rendering; returned " +
                            "prose was archived and passed the closed causal " +
                            "contradiction audit; positive control and archive " +
                            "hash-chain verification both held."
                    renderAudit(result)
                    renderResponses(
                        result.getJSONObject("rendered_branches")
                    )
                }

                "primary_endpoint_failed" -> {
                    statusView.text =
                        "P3.13 FAIL-CLOSED: the frozen P3.12 causal " +
                            "endpoint did not hold. No provider calls were made."
                    auditView.text =
                        "Renderer audit correctly withheld."
                    responsesView.text =
                        "Language rendering was correctly withheld."
                }

                "missing" -> {
                    statusView.text =
                        "P3.12 endpoint passed locally, but no API key is " +
                            "packaged. P3.13 provider stage was not run."
                    auditView.text =
                        "Renderer audit incomplete: provider stage absent."
                    responsesView.text =
                        "Local causal assay complete; provider stage absent."
                }

                "mismatch", "noncanonical" -> {
                    statusView.text =
                        "P3.12 endpoint passed locally, but credential " +
                            "attestation blocked P3.13 rendering."
                    auditView.text =
                        "Renderer audit incomplete: credential gate blocked."
                    responsesView.text =
                        "Local causal assay complete; provider stage blocked."
                }

                "downstream_validation_failed" -> {
                    statusView.text =
                        "P3.12 primary endpoint passed, but its downstream " +
                            "relay-evidence or Numogram-isolation gate failed."
                    renderAudit(result)
                    result.optJSONObject("rendered_branches")
                        ?.let { renderResponses(it) }
                }

                "renderer_faithfulness_failed" -> {
                    statusView.text =
                        "P3.12 remained intact, but the P3.13 renderer-" +
                            "faithfulness acceptance gate did not fully hold."
                    renderAudit(result)
                    result.optJSONObject("rendered_branches")
                        ?.let { renderResponses(it) }
                }

                else -> {
                    statusView.text =
                        "P3.13 error: " +
                            result.optString(
                                "message",
                                raw.take(500)
                            )
                }
            }
        } catch (error: Throwable) {
            statusView.text =
                "Unable to parse P3.13 result: ${error.message}"
        }
    }

    private fun renderAudit(result: JSONObject) {
        val rendered = result.optJSONObject("rendered_branches")

        auditView.text = buildString {
            append("Run ID: ")
            append(result.optString("p313_run_id", "n/a"))

            if (rendered != null) {
                appendBranchAudit(
                    this,
                    "A",
                    rendered.optJSONObject(CONDITION_A)
                )
                appendBranchAudit(
                    this,
                    "B",
                    rendered.optJSONObject(CONDITION_B)
                )
                appendBranchAudit(
                    this,
                    "C",
                    rendered.optJSONObject(CONDITION_C)
                )
            }

            append("\n\nAuditor positive control: ")
            append(
                result.optBoolean(
                    "p313_positive_control_held",
                    false
                )
            )
            append("\nArchive hash-chain valid: ")
            append(
                result.optBoolean(
                    "p313_archive_hash_chain_valid",
                    false
                )
            )
            append("\nP3.12 downstream preserved: ")
            append(
                result.optBoolean(
                    "p312_downstream_held",
                    false
                )
            )
            append("\nP3.13 RENDERER FAITHFULNESS: ")
            append(
                result.optBoolean(
                    "p313_renderer_faithfulness_held",
                    false
                )
            )
        }
    }

    private fun appendBranchAudit(
        builder: StringBuilder,
        label: String,
        branch: JSONObject?
    ) {
        if (branch == null) {
            builder.append("\n\n$label audit: unavailable")
            return
        }

        builder.append("\n\n")
        builder.append(label)
        builder.append(" pre-render payload archived: ")
        builder.append(
            branch.optBoolean(
                "p313_pre_render_payload_archived",
                false
            )
        )
        builder.append("\n")
        builder.append(label)
        builder.append(" prose audit: ")
        builder.append(
            branch.optString(
                "p313_audit_status",
                "UNKNOWN"
            )
        )
        builder.append("\n")
        builder.append(label)
        builder.append(" contradictions: ")
        builder.append(
            branch.optInt(
                "p313_contradiction_count",
                -1
            )
        )
    }

    private fun renderResponses(rendered: JSONObject) {
        responsesView.text = buildString {
            appendBranch(
                this,
                "A — PFM ABSENT",
                rendered.getJSONObject(CONDITION_A)
            )
            append("\n\n")
            appendBranch(
                this,
                "B — PFM RETAINED",
                rendered.getJSONObject(CONDITION_B)
            )
            append("\n\n")
            appendBranch(
                this,
                "C — PFM RESET",
                rendered.getJSONObject(CONDITION_C)
            )
        }
    }

    private fun appendBranch(
        builder: StringBuilder,
        label: String,
        branch: JSONObject
    ) {
        builder.append(label)
        builder.append("\nPFM depth: ")
        if (branch.isNull("pfm_history_depth")) {
            builder.append("absent")
        } else {
            builder.append(
                branch.optInt("pfm_history_depth", -1)
            )
        }

        builder.append("\nRelay evidence: ")
        builder.append(
            if (
                branch.optBoolean(
                    "pfm_evidence_expected",
                    false
                )
            ) {
                branch.optBoolean(
                    "pfm_relay_evidence_held",
                    false
                ).toString()
            } else {
                "n/a"
            }
        )

        builder.append("\nNumogram unchanged: ")
        builder.append(
            branch.optBoolean(
                "numogram_state_unchanged",
                false
            )
        )

        builder.append("\nP3.13 audit: ")
        builder.append(
            branch.optString(
                "p313_audit_status",
                "UNKNOWN"
            )
        )

        builder.append("\nP3.13 contradictions: ")
        builder.append(
            branch.optInt(
                "p313_contradiction_count",
                -1
            )
        )

        builder.append("\n\nAmelia:\n")
        builder.append(
            branch.optString(
                "rendered_text",
                "(no text)"
            )
        )
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

    private fun credentialAttestation(): JSONObject {
        val key = BuildConfig.ANTHROPIC_API_KEY
        val actualFingerprint =
            if (key.isBlank()) "missing" else sha256Hex(key)
        val expectedFingerprint =
            BuildConfig.CREDENTIAL_FINGERPRINT
        val expectedShape =
            BuildConfig.CREDENTIAL_SHAPE

        val keyShape = when {
            key.isBlank() -> "missing"
            key.startsWith("sk-ant-") &&
                key.none { it.isWhitespace() } -> "canonical"
            else -> "noncanonical"
        }

        val state = when {
            key.isBlank() -> "missing"
            expectedShape != "canonical" ||
                keyShape != "canonical" -> "noncanonical"
            expectedFingerprint == "missing" ||
                expectedFingerprint != actualFingerprint -> "mismatch"
            else -> "usable"
        }

        return JSONObject()
            .put(
                "schema",
                "amelia-p3.13-credential-attestation-v1"
            )
            .put("state", state)
            .put("usable", state == "usable")
            .put("fingerprint", actualFingerprint)
            .put(
                "build_fingerprint",
                expectedFingerprint
            )
            .put("shape", keyShape)
            .put(
                "build_shape",
                expectedShape
            )
            .put(
                "revision",
                BuildConfig.BUILD_REVISION
            )
    }

    private fun sha256Hex(input: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(input.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }

    private fun sectionHeading(text: String): TextView =
        TextView(this).apply {
            this.text = text
            textSize = 17f
            setPadding(dp(4), dp(18), dp(4), dp(4))
        }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density).toInt()
}
