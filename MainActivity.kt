package com.amelia.p361

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.bridge.NumogramBridge
import kotlin.math.abs
import org.json.JSONObject

class MainActivity : Activity() {

    companion object {
        private const val LOG_TAG = "AMELIA_P361"
        private const val PROBE_SEED = 3606
        private const val PROBE_DIMENSION = 3
        private const val PROBE_ORIGIN = 3
    }

    private lateinit var statusView: TextView
    private lateinit var detailView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(24), dp(20), dp(24))
        }

        root.addView(
            TextView(this).apply {
                text = "AMELIA · P3.6.1"
                textSize = 25f
                gravity = Gravity.CENTER_HORIZONTAL
            }
        )

        root.addView(
            TextView(this).apply {
                text = "Chaquopy 16.1 · Python 3.8 · Torch 1.8.1 · digest-matched reattachment"
                textSize = 14f
                gravity = Gravity.CENTER_HORIZONTAL
                setPadding(0, dp(8), 0, dp(18))
            }
        )

        statusView = TextView(this).apply {
            text = "P3.6.1 tensor probe starting…"
            textSize = 20f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(8), dp(18), dp(8), dp(18))
        }

        detailView = TextView(this).apply {
            text = "Waiting for Torch import and the sealed Numogram lifecycle."
            textSize = 14f
            setPadding(dp(8), dp(12), dp(8), dp(12))
        }

        root.addView(statusView)
        root.addView(detailView)

        root.addView(
            TextView(this).apply {
                text =
                    "\nP3.6.1 boundary:\n\n" +
                    "Kotlin\n" +
                    "  ↓\n" +
                    "NumogramBridge\n" +
                    "  ↓\n" +
                    "Python 3.8 · Numogram.py\n" +
                    "  ↓\n" +
                    "Torch 1.8.1 tensor field\n" +
                    "  ↓\n" +
                    "initialize (fresh OR digest-matched reattach) → status → transition → status\n" +
                    "  ↓\n" +
                    "Kotlin\n\n" +
                    "Fixed probe: seed 3606 · dimension 3 · origin Z3 · context {}\n\n" +
                    "No language model. No network. Persistence disabled.\n\n" +
                    "A repeat launch reattaches to the already-running system (same " +
                    "seed/dimension) rather than silently discarding its history, and " +
                    "this screen checks that exactly one transition happened this run " +
                    "-- not that the step count is 1 -- so it stays correct whether " +
                    "this is the first launch or the fifth."
                textSize = 14f
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
                    .put("schema", "amelia-p3.6.1-probe-result-v1")
                    .put("status", "error")
                    .put("error_type", t::class.java.simpleName)
                    .put("message", t.message ?: "Unknown Android, Chaquopy, or Torch error")
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
        val finalStatus = JSONObject(bridge.status())

        return JSONObject()
            .put("schema", "amelia-p3.6.1-probe-result-v1")
            .put("status", "completed")
            .put("runtime", runtime)
            .put("before", before)
            .put("initialized", initialized)
            .put("ready", ready)
            .put("transitioned", transitioned)
            .put("final", finalStatus)
            .toString()
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
            val finalStatus = result.optJSONObject("final")
                ?: throw IllegalStateException("Missing final status")

            val initializedSystem = initialized.optJSONObject("system")
                ?: throw IllegalStateException("Missing initialized system")
            val readySystem = ready.optJSONObject("system")
                ?: throw IllegalStateException("Missing ready system")
            val event = transitioned.optJSONObject("event")
                ?: throw IllegalStateException("Missing transition event")
            val finalSystem = finalStatus.optJSONObject("system")
                ?: throw IllegalStateException("Missing final system")
            val probabilities = event.optJSONArray("probabilities")
                ?: throw IllegalStateException("Missing probability vector")

            var probabilityMass = 0.0
            var finiteProbabilities = true
            for (index in 0 until probabilities.length()) {
                val value = probabilities.optDouble(index, Double.NaN)
                if (value.isNaN() || value.isInfinite()) {
                    finiteProbabilities = false
                } else {
                    probabilityMass += value
                }
            }

            val torchVersion = runtime.optString("torch_version", "")
            val torchReady =
                runtime.optString("status", "") == "torch_ready" &&
                    torchVersion.startsWith("1.8.1") &&
                    runtime.optInt("zone_count", -1) == 10 &&
                    !runtime.optBoolean("persistence_default", true)

            // A second (or fifth) launch reattaches rather than resets, so
            // "initialized" alone is no longer the only valid outcome --
            // "already_initialized" is equally valid PROVIDED the digest
            // match actually held, which is what state_unchanged plus the
            // digest comparison below confirms rather than assumes.
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

            // Baseline is whatever evolution_step/history already existed
            // going into this run -- 0 on a genuine cold start, whatever a
            // prior launch left behind on a reattachment. Everything below
            // checks the delta this run produced, not an absolute value.
            val baselineStep = readySystem.optInt("evolution_step", -1)
            val baselineHistory = readySystem.optInt("transition_history", -1)

            val readyHeld =
                ready.optString("status", "") == "ready" &&
                    baselineStep >= 0 &&
                    baselineHistory >= 0

            val transitionHeld =
                transitioned.optString("status", "") == "transitioned" &&
                    event.optInt("step", -1) == baselineStep + 1 &&
                    event.optInt("from", -1) == PROBE_ORIGIN &&
                    event.optInt("to", -1) in 0 until 10 &&
                    !event.optBoolean("fallback", true) &&
                    probabilities.length() == 10 &&
                    finiteProbabilities &&
                    abs(probabilityMass - 1.0) <= 0.00001

            val finalHeld =
                finalStatus.optString("status", "") == "ready" &&
                    finalSystem.optInt("evolution_step", -1) == baselineStep + 1 &&
                    finalSystem.optInt("transition_history", -1) == baselineHistory + 1 &&
                    !finalSystem.optBoolean("persistence_enabled", true)

            val passed =
                result.optString("status", "") == "completed" &&
                    torchReady &&
                    initializationHeld &&
                    readyHeld &&
                    transitionHeld &&
                    finalHeld

            val transitionLine =
                "Z" + event.optInt("from") + " → Z" + event.optInt("to")
            val initKind = if (initStatus == "already_initialized") {
                "reattached to existing system (digest-matched)"
            } else {
                "fresh initialization"
            }

            if (passed) {
                statusView.text = "P3.6.1 PASSED ✓"
                detailView.text =
                    "Torch imported and the live tensor Numogram lifecycle completed.\n\n" +
                        "Torch: " + torchVersion + "\n" +
                        "Before initialization: " + before.optString("status") + "\n" +
                        "Initialization: " + initKind + "\n" +
                        "Seed: " + initializedSystem.optInt("seed") + "\n" +
                        "Dimension: " + initializedSystem.optInt("dimension") + "\n" +
                        "Step baseline going in: " + baselineStep + "\n" +
                        "Transition: " + transitionLine + "\n" +
                        "Step after: " + event.optInt("step") + "\n" +
                        "Probability mass: " + probabilityMass + "\n" +
                        "Fallback: " + event.optBoolean("fallback") + "\n" +
                        "History: " + finalSystem.optInt("transition_history") + "\n" +
                        "Persistence: " + finalSystem.optBoolean("persistence_enabled")
            } else {
                statusView.text = "P3.6.1 FAIL-CLOSED"
                detailView.text =
                    "A Torch/Numogram response was received, but it did not satisfy " +
                        "the sealed P3.6.1 contract.\n\n" +
                        "Torch ready: " + torchReady + "\n" +
                        "Initialization: " + initializationHeld + " (" + initStatus + ")\n" +
                        "Ready state: " + readyHeld + "\n" +
                        "Transition: " + transitionHeld + "\n" +
                        "Final state: " + finalHeld + "\n\n" +
                        "Raw response:\n" + raw
            }
        } catch (t: Throwable) {
            statusView.text = "P3.6.1 FAIL-CLOSED"
            detailView.text =
                "The returned Torch/Numogram value was not valid P3.6.1 probe JSON.\n\n" +
                    "Error: " + (t.message ?: "Unknown parsing error") + "\n\n" +
                    "Raw response:\n" + raw
        }
    }

    private fun dp(value: Int): Int {
        return (value * resources.displayMetrics.density).toInt()
    }
}
