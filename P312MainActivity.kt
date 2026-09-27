package com.amelia.p312

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
import com.amelia.renderer.RenderCapsule
import com.amelia.renderer.RenderTransport
import org.json.JSONObject
import java.security.MessageDigest

/**
 * P3.12 matched causal incorporation assay.
 *
 * Primary endpoint:
 *   identical Numogram event 1 and event 2 across A/B/C,
 *   A has no PFM,
 *   B event 2 has retained PFM history depth 2,
 *   C event 2 has reset PFM history depth 1.
 *
 * Language responses are downstream descriptive evidence. Provider generation
 * is not treated as deterministic causal evidence by itself.
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
    private lateinit var responsesView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(22), dp(18), dp(28))
        }

        root.addView(TextView(this).apply {
            text = "AMELIA · P3.12"
            textSize = 25f
            gravity = Gravity.CENTER_HORIZONTAL
        })

        root.addView(TextView(this).apply {
            text =
                "Matched causal incorporation assay · " +
                    "PFM absent / retained / reset"
            textSize = 14f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(8), 0, dp(16))
        })

        statusView = TextView(this).apply {
            text =
                "Ready. One assay runs three fresh Numogram instances " +
                    "with the same seed and prompt sequence."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(statusView)

        root.addView(sectionHeading("CONDITIONING PROMPT · EVENT 1"))
        promptOneView = EditText(this).apply {
            setText(
                "What is the significance of 333 in the Numogram?"
            )
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
            text = "RUN MATCHED A / B / C ASSAY"
            setOnClickListener { runMatchedAssay() }
        }
        root.addView(runButton)

        root.addView(sectionHeading("PRIMARY CAUSAL ENDPOINT"))
        endpointView = TextView(this).apply {
            text = "No assay run yet."
            textSize = 13f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(endpointView)

        root.addView(sectionHeading("SECOND-EVENT LANGUAGE REALIZATIONS"))
        responsesView = TextView(this).apply {
            text =
                "A, B and C responses will appear here after the " +
                    "matched transition check passes."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(12))
        }
        root.addView(responsesView)

        root.addView(TextView(this).apply {
            text =
                "A — PFM absent: Numogram → language\n" +
                    "B — PFM retained: event 1 deforms PFM; event 2 inherits it\n" +
                    "C — PFM reset: same PFM source, zeroed before each event\n\n" +
                    "The language provider is called only for event 2. " +
                    "The primary causal endpoint is determined before rendering. " +
                    "Natural-language differences are retained as downstream " +
                    "descriptive evidence rather than treated as deterministic " +
                    "proof by themselves."
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
            "Running fresh-state A/B/C Numogram sequences…"
        endpointView.text = "Assay in progress."
        responsesView.text = "Waiting for matched transition check…"

        Thread {
            val raw = try {
                executeAssay(promptOne, promptTwo)
            } catch (error: Throwable) {
                JSONObject()
                    .put(
                        "schema",
                        "amelia-p3.12-android-result-v1"
                    )
                    .put("status", "error")
                    .put(
                        "error_type",
                        error::class.java.simpleName
                    )
                    .put(
                        "message",
                        error.message ?: "Unknown P3.12 error"
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
        val assay =
            JSONObject(
                bridge.runAssay(
                    promptOne,
                    promptTwo,
                    NUMOGRAM_SEED,
                    NUMOGRAM_DIMENSION
                )
            )

        val endpoint =
            assay.getJSONObject("primary_endpoint")

        val primaryHeld =
            endpoint.optBoolean(
                "causal_memory_contrast_held",
                false
            )

        val result = JSONObject()
            .put(
                "schema",
                "amelia-p3.12-android-result-v1"
            )
            .put("assay", assay)
            .put("primary_endpoint_held", primaryHeld)

        if (!primaryHeld) {
            result.put(
                "status",
                "primary_endpoint_failed"
            )
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

        val branches = assay.getJSONObject("branches")
        val rendered = JSONObject()

        listOf(
            CONDITION_A,
            CONDITION_B,
            CONDITION_C
        ).forEach { condition ->
            val branch = branches.getJSONObject(condition)
            val response = renderCriticalEvent(
                bridge = bridge,
                condition = condition,
                promptOne = promptOne,
                promptTwo = promptTwo,
                branch = branch
            )
            rendered.put(condition, response)
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
            "status",
            if (
                allIsolationHeld &&
                bEvidenceHeld &&
                cEvidenceHeld
            ) {
                "success"
            } else {
                "downstream_validation_failed"
            }
        )

        return result.toString()
    }

    private fun renderCriticalEvent(
        bridge: P312AssayBridge,
        condition: String,
        promptOne: String,
        promptTwo: String,
        branch: JSONObject
    ): JSONObject {
        val pfmEventTwo =
            branch.optJSONObject("pfm_event_two")

        val prompt = P312PromptBuilder.build(
            conditioningPrompt = promptOne,
            criticalPrompt = promptTwo,
            eventOne = branch.getJSONObject("event_one"),
            eventTwo = branch.getJSONObject("event_two"),
            pfmEventTwo = pfmEventTwo
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

        val expectedToken =
            prompt.expectedEvidenceToken

        val evidenceExpected =
            expectedToken != null

        val evidenceHeld =
            if (expectedToken == null) {
                true
            } else {
                rawText.contains(expectedToken)
            }

        val displayText =
            stripEvidenceToken(rawText, expectedToken)

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
    }

    private fun renderAssay(raw: String) {
        try {
            val result = JSONObject(raw)
            val assay = result.optJSONObject("assay")
            val endpoint =
                assay?.optJSONObject("primary_endpoint")

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
                        "P3.12 PASS: matched transitions held; " +
                            "retained PFM separated B from absent/reset " +
                            "controls; relay evidence and Numogram " +
                            "isolation both held."
                    renderResponses(
                        result.getJSONObject(
                            "rendered_branches"
                        )
                    )
                }

                "primary_endpoint_failed" -> {
                    statusView.text =
                        "P3.12 FAIL-CLOSED: the matched causal " +
                            "endpoint did not hold. No provider calls " +
                            "were made."
                    responsesView.text =
                        "Language rendering was correctly withheld."
                }

                "missing" -> {
                    statusView.text =
                        "Primary P3.12 endpoint passed locally, but " +
                            "no API key is packaged. Language branches " +
                            "were not rendered."
                    responsesView.text =
                        "Local causal assay complete; provider stage absent."
                }

                "mismatch", "noncanonical" -> {
                    statusView.text =
                        "Primary P3.12 endpoint passed locally, but " +
                            "credential attestation blocked rendering."
                    responsesView.text =
                        "Local causal assay complete; provider stage blocked."
                }

                "downstream_validation_failed" -> {
                    statusView.text =
                        "Primary P3.12 causal endpoint passed, but " +
                            "relay-evidence or post-render Numogram " +
                            "isolation failed."
                    result.optJSONObject("rendered_branches")
                        ?.let { renderResponses(it) }
                }

                else -> {
                    statusView.text =
                        "P3.12 error: " +
                            result.optString(
                                "message",
                                raw.take(500)
                            )
                }
            }
        } catch (error: Throwable) {
            statusView.text =
                "Unable to parse P3.12 result: ${error.message}"
        }
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
                "amelia-p3.12-credential-attestation-v1"
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
