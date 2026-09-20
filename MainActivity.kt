package com.amelia.p38

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.bridge.NumogramBridge
import com.amelia.renderer.RenderCapsule
import com.amelia.renderer.RenderPromptBuilder
import com.amelia.renderer.RenderTransport
import kotlin.math.abs
import org.json.JSONArray
import org.json.JSONObject

class MainActivity : Activity() {

    companion object {
        private const val LOG_TAG = "AMELIA_P38"
        private const val PROBE_SEED = 3606
        private const val PROBE_DIMENSION = 3
        private const val PROBE_ORIGIN = 3
        private val EXPECTED_BRANCHES = listOf(
            "FULL", "ABLATED_TRANSITION", "ABLATED_MAGNETISM", "ABLATED_BOTH", "NEUTRAL_RESET"
        )
    }

    private lateinit var statusView: TextView
    private lateinit var detailView: TextView
    private lateinit var renderView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(24), dp(20), dp(24))
        }

        root.addView(
            TextView(this).apply {
                text = "AMELIA · P3.8"
                textSize = 25f
                gravity = Gravity.CENTER_HORIZONTAL
            }
        )

        root.addView(
            TextView(this).apply {
                text = "Chaquopy 16.1 · Python 3.8 · Torch 1.8.1 · sealed fork → Claude API render"
                textSize = 14f
                gravity = Gravity.CENTER_HORIZONTAL
                setPadding(0, dp(8), 0, dp(18))
            }
        )

        statusView = TextView(this).apply {
            text = "P3.8 render probe starting…"
            textSize = 20f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(8), dp(18), dp(8), dp(18))
        }

        detailView = TextView(this).apply {
            text = "Waiting for the Numogram fork, then the sealed render call."
            textSize = 13f
            setPadding(dp(8), dp(12), dp(8), dp(12))
        }

        renderView = TextView(this).apply {
            text = ""
            textSize = 14f
            setPadding(dp(8), dp(12), dp(8), dp(12))
        }

        root.addView(statusView)
        root.addView(detailView)
        root.addView(renderView)

        root.addView(
            TextView(this).apply {
                text =
                    "\nP3.8 boundary:\n\n" +
                    "Kotlin\n" +
                    "  ↓\n" +
                    "NumogramBridge → Numogram.py (fork, as P3.7)\n" +
                    "  ↓\n" +
                    "RenderPromptBuilder: curates the fork result into a prompt,\n" +
                    "  digests the trace, the curated payload, and the template\n" +
                    "  ↓\n" +
                    "RenderCapsule.seal(): fixes provider, model, params,\n" +
                    "  streaming/tools/functionCalling/webhook all false\n" +
                    "  ↓\n" +
                    "RenderTransport.execute(): single sealed call to the\n" +
                    "  declared endpoint only; response classified and\n" +
                    "  digested before any of it is trusted\n" +
                    "  ↓\n" +
                    "Kotlin: displays the rendered text; never routes it\n" +
                    "  back into NumogramBridge -- checked below, not assumed\n\n" +
                    "Fixed probe: seed 3606 · dimension 3 · origin Z3 · context {}\n\n" +
                    "No key configured means no network call is attempted -- " +
                    "reported plainly rather than left to fail as an HTTP error."
                textSize = 13f
            }
        )

        scroll.addView(root)
        setContentView(scroll)
        runProbe()
    }

    private fun runProbe() {
        Thread {
            val raw = try {
                executeProbe()
            } catch (t: Throwable) {
                JSONObject()
                    .put("schema", "amelia-p3.8-probe-result-v1")
                    .put("status", "error")
                    .put("error_type", t::class.java.simpleName)
                    .put("message", t.message ?: "Unknown Android, Chaquopy, Torch, or network error")
                    .toString()
            }

            Log.i(LOG_TAG, raw)
            runOnUiThread {
                renderProbeResult(raw)
            }
        }.start()
    }

    private fun executeProbe(): String {
        val bridge = NumogramBridge(applicationContext)
        val runtime = JSONObject(bridge.runtimeInfo())
        val before = JSONObject(bridge.status())
        val initialized = JSONObject(bridge.initialize(PROBE_SEED, PROBE_DIMENSION))
        val ready = JSONObject(bridge.status())
        val transitioned = JSONObject(bridge.transition(PROBE_ORIGIN, "{}"))
        val forked = JSONObject(bridge.runFork(PROBE_ORIGIN, "{}"))
        val verified = JSONObject(bridge.verifyLastFork())
        val postForkStatus = JSONObject(bridge.status())

        val result = JSONObject()
            .put("schema", "amelia-p3.8-probe-result-v1")
            .put("runtime", runtime)
            .put("before", before)
            .put("initialized", initialized)
            .put("ready", ready)
            .put("transitioned", transitioned)
            .put("forked", forked)
            .put("verified", verified)
            .put("post_fork_status", postForkStatus)

        val apiKey = BuildConfig.ANTHROPIC_API_KEY
        if (apiKey.isBlank()) {
            result.put("status", "completed_no_render")
            result.put("render_status", "no_api_key_configured")
            val finalStatus = JSONObject(bridge.status())
            result.put("final", finalStatus)
            return result.toString()
        }

        val promptPayload = RenderPromptBuilder.buildFromForkResult(forked)
        val capsule = RenderCapsule.seal(
            traceDigest = promptPayload.traceDigest,
            payloadDigest = promptPayload.payloadDigest,
            rendererTemplateDigest = promptPayload.rendererTemplateDigest
        )
        val transportResult = RenderTransport.execute(capsule, promptPayload.renderPrompt, apiKey)

        // The boundary claim this stage exists to check: the render call
        // must not have touched the substrate. Compared against ACTUAL
        // status calls before and after, not assumed from the transport
        // object's own (necessarily self-reported) behaviour.
        val postRenderStatus = JSONObject(bridge.status())

        val sealed = transportResult.sealed
        result.put("status", "completed")
        result.put("capsule_digest", capsule.capsuleDigest)
        result.put("trace_digest", promptPayload.traceDigest)
        result.put("payload_digest", promptPayload.payloadDigest)
        result.put("renderer_template_digest", promptPayload.rendererTemplateDigest)
        result.put("model", capsule.model)
        result.put("attempt_count", transportResult.attempts.size)
        if (sealed != null) {
            result.put("render_status", "completed")
            result.put("response_class", sealed.responseClass.name)
            result.put("http_status", sealed.httpStatus)
            result.put("raw_response_digest", sealed.rawResponseDigest)
            result.put("rendered_text", sealed.parsedDisplayText)
        } else {
            result.put("render_status", "transport_failed")
            result.put("attempts_all_errored", true)
        }
        result.put("post_render_status", postRenderStatus)
        result.put("final", postRenderStatus)

        return result.toString()
    }

    private fun probabilitiesValid(probabilities: JSONArray): Boolean {
        if (probabilities.length() != 10) return false
        var mass = 0.0
        for (index in 0 until probabilities.length()) {
            val value = probabilities.optDouble(index, Double.NaN)
            if (value.isNaN() || value.isInfinite()) return false
            mass += value
        }
        return abs(mass - 1.0) <= 0.00001
    }

    private fun renderProbeResult(raw: String) {
        try {
            val result = JSONObject(raw)
            val runtime = result.optJSONObject("runtime")
                ?: throw IllegalStateException("Missing Torch runtime record")
            val before = result.optJSONObject("before")
                ?: throw IllegalStateException("Missing pre-initialization status")
            val initialized = result.optJSONObject("initialized")
                ?: throw IllegalStateException("Missing initialization result")
            val ready = result.optJSONObject("ready")
                ?: throw IllegalStateException("Missing ready status")
            val transitioned = result.optJSONObject("transitioned")
                ?: throw IllegalStateException("Missing transition result")
            val forked = result.optJSONObject("forked")
                ?: throw IllegalStateException("Missing fork result")
            val verified = result.optJSONObject("verified")
                ?: throw IllegalStateException("Missing verify result")

            val initializedSystem = initialized.optJSONObject("system")
                ?: throw IllegalStateException("Missing initialized system")
            val readySystem = ready.optJSONObject("system")
                ?: throw IllegalStateException("Missing ready system")
            val event = transitioned.optJSONObject("event")
                ?: throw IllegalStateException("Missing transition event")
            val transitionProbs = event.optJSONArray("probabilities")
                ?: throw IllegalStateException("Missing transition probability vector")
            val branches = forked.optJSONObject("branches")
                ?: throw IllegalStateException("Missing fork branches")
            val invariants = forked.optJSONObject("invariants")
                ?: throw IllegalStateException("Missing fork invariants")

            val torchVersion = runtime.optString("torch_version", "")
            val torchReady =
                runtime.optString("status", "") == "torch_ready" &&
                    torchVersion.startsWith("1.8.1") &&
                    runtime.optInt("zone_count", -1) == 10 &&
                    !runtime.optBoolean("persistence_default", true)

            val initStatus = initialized.optString("status", "")
            val digestMatchedReattachment =
                initStatus == "already_initialized" &&
                    initialized.optBoolean("state_unchanged", false) &&
                    initialized.optString("init_digest", "").isNotBlank() &&
                    initialized.optString("init_digest", "") ==
                        initialized.optString("attempted_init_digest", "")

            val initializationHeld =
                (initStatus == "initialized" || digestMatchedReattachment) &&
                    initializedSystem.optInt("seed", -1) == PROBE_SEED &&
                    initializedSystem.optInt("dimension", -1) == PROBE_DIMENSION &&
                    !initializedSystem.optBoolean("persistence_enabled", true)

            val baselineStep = readySystem.optInt("evolution_step", -1)
            val baselineHistory = readySystem.optInt("transition_history", -1)

            val readyHeld =
                ready.optString("status", "") == "ready" && baselineStep >= 0 && baselineHistory >= 0

            val transitionHeld =
                transitioned.optString("status", "") == "transitioned" &&
                    event.optInt("step", -1) == baselineStep + 1 &&
                    event.optInt("from", -1) == PROBE_ORIGIN &&
                    event.optInt("to", -1) in 0 until 10 &&
                    probabilitiesValid(transitionProbs)

            var branchesWellFormed = true
            val branchLines = StringBuilder()
            for (name in EXPECTED_BRANCHES) {
                val branch = branches.optJSONObject(name)
                if (branch == null) {
                    branchesWellFormed = false
                    branchLines.append("$name: missing\n")
                    continue
                }
                val branchProbs = branch.optJSONArray("probabilities")
                val wellFormed =
                    branch.optInt("from", -1) == PROBE_ORIGIN &&
                        branch.optInt("to", -1) in 0 until 10 &&
                        branchProbs != null && probabilitiesValid(branchProbs)
                if (!wellFormed) branchesWellFormed = false
                branchLines.append(
                    "$name: Z${branch.optInt("from")} → Z${branch.optInt("to")}" +
                        (if (branch.optBoolean("fallback", false)) " (fallback)" else "") + "\n"
                )
            }

            val liveStateUnchanged = invariants.optBoolean("live_state_unchanged", false)
            val generatorStateUnchanged = invariants.optBoolean("generator_state_unchanged", false)
            val ablatedMatchesNeutral = invariants.optBoolean("ablated_both_matches_neutral_reset", false)

            val forkHeld =
                forked.optString("status", "") == "forked" &&
                    forked.optString("capsule_digest", "").isNotBlank() &&
                    branchesWellFormed &&
                    liveStateUnchanged &&
                    generatorStateUnchanged &&
                    ablatedMatchesNeutral

            val mismatchedBranches = verified.optJSONArray("mismatched_branches")
            val verifyHeld =
                verified.optString("status", "") == "verified" &&
                    mismatchedBranches != null && mismatchedBranches.length() == 0 &&
                    verified.optString("capsule_digest", "") == forked.optString("capsule_digest", "")

            val overallStatus = result.optString("status", "")
            val renderStatus = result.optString("render_status", "")

            if (overallStatus == "completed_no_render") {
                statusView.text = "P3.8 NO RENDER (key not configured)"
                detailView.text =
                    "The Numogram fork completed and verified normally, but " +
                        "BuildConfig.ANTHROPIC_API_KEY is blank, so no network call " +
                        "was attempted. Fork held: " + forkHeld + " · Verify held: " + verifyHeld +
                        "\n\nAdd the ANTHROPIC_API_KEY repository secret and rebuild " +
                        "to exercise the render step."
                renderView.text = ""
                return
            }

            // post_render_status is the ground-truth check for the one-way
            // boundary: the Numogram must show exactly the same evolution_step
            // and transition_history after the render call as it did right
            // after the fork -- a render call that somehow looped back into
            // the substrate would show up here as an unexpected increment.
            val postForkStatus = result.optJSONObject("post_fork_status")
                ?: throw IllegalStateException("Missing post-fork status")
            val postRenderStatus = result.optJSONObject("post_render_status")
                ?: throw IllegalStateException("Missing post-render status")
            val postForkSystem = postForkStatus.optJSONObject("system")
                ?: throw IllegalStateException("Missing post-fork system")
            val postRenderSystem = postRenderStatus.optJSONObject("system")
                ?: throw IllegalStateException("Missing post-render system")

            val noFeedbackHeld =
                postRenderSystem.optInt("evolution_step", -1) == postForkSystem.optInt("evolution_step", -2) &&
                    postRenderSystem.optInt("transition_history", -1) == postForkSystem.optInt("transition_history", -2)

            val renderTransportSucceeded = renderStatus == "completed"
            val responseClass = result.optString("response_class", "")
            val renderedText = result.optString("rendered_text", "")

            val passed =
                overallStatus == "completed" &&
                    torchReady &&
                    initializationHeld &&
                    readyHeld &&
                    transitionHeld &&
                    forkHeld &&
                    verifyHeld &&
                    renderTransportSucceeded &&
                    noFeedbackHeld

            val initKind = if (initStatus == "already_initialized") {
                "reattached to existing system (digest-matched)"
            } else {
                "fresh initialization"
            }

            if (passed) {
                statusView.text = "P3.8 PASSED ✓"
                detailView.text =
                    "Torch imported, one transition committed, the five-condition " +
                        "fork ran and replay-verified, and the sealed render call " +
                        "completed without any trace of feeding back into the substrate.\n\n" +
                        "Torch: " + torchVersion + "\n" +
                        "Initialization: " + initKind + "\n" +
                        "Fork branches (all from Z3):\n" + branchLines.toString() +
                        "verify_last_fork: " + verified.optString("status") + "\n\n" +
                        "Model: " + result.optString("model", "") + "\n" +
                        "Response class: " + responseClass + "\n" +
                        "HTTP status: " + result.optInt("http_status", -1) + "\n" +
                        "Attempts: " + result.optInt("attempt_count", -1) + "\n" +
                        "Capsule digest: " + result.optString("capsule_digest", "").take(16) + "…\n" +
                        "no_feedback_held: " + noFeedbackHeld
                renderView.text =
                    if (responseClass == "SUCCESS_TEXT") {
                        "Rendered text:\n\n" + renderedText
                    } else {
                        "Renderer returned " + responseClass + " rather than text " +
                            "(this is still a mechanically correct, boundary-respecting " +
                            "result -- the transport and the sealed capsule worked; " +
                            "the model just didn't produce display text this time).\n\n" +
                            "Raw: " + renderedText.take(300)
                    }
            } else {
                statusView.text = "P3.8 FAIL-CLOSED"
                renderView.text = ""
                detailView.text =
                    "A response was received, but it did not satisfy the sealed " +
                        "P3.8 contract.\n\n" +
                        "Torch ready: " + torchReady + "\n" +
                        "Initialization: " + initializationHeld + " (" + initStatus + ")\n" +
                        "Ready state: " + readyHeld + "\n" +
                        "Transition: " + transitionHeld + "\n" +
                        "Fork: " + forkHeld + " (branches well-formed: " + branchesWellFormed + ")\n" +
                        "Verify: " + verifyHeld + "\n" +
                        "Render transport succeeded: " + renderTransportSucceeded + "\n" +
                        "no_feedback_held: " + noFeedbackHeld + "\n\n" +
                        "Raw response:\n" + raw
            }
        } catch (t: Throwable) {
            statusView.text = "P3.8 FAIL-CLOSED"
            renderView.text = ""
            detailView.text =
                "The returned value was not valid P3.8 probe JSON.\n\n" +
                    "Error: " + (t.message ?: "Unknown parsing error") + "\n\n" +
                    "Raw response:\n" + raw
        }
    }

    private fun dp(value: Int): Int {
        return (value * resources.displayMetrics.density).toInt()
    }
}
