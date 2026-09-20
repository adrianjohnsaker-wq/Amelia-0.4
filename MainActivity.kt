package com.amelia.p37

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.bridge.NumogramBridge
import kotlin.math.abs
import org.json.JSONArray
import org.json.JSONObject

class MainActivity : Activity() {

    companion object {
        private const val LOG_TAG = "AMELIA_P37"
        private const val PROBE_SEED = 3606
        private const val PROBE_DIMENSION = 3
        private const val PROBE_ORIGIN = 3
        private val EXPECTED_BRANCHES = listOf(
            "FULL", "ABLATED_TRANSITION", "ABLATED_MAGNETISM", "ABLATED_BOTH", "NEUTRAL_RESET"
        )
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
                text = "AMELIA · P3.7"
                textSize = 25f
                gravity = Gravity.CENTER_HORIZONTAL
            }
        )

        root.addView(
            TextView(this).apply {
                text = "Chaquopy 16.1 · Python 3.8 · Torch 1.8.1 · matched FULL/ABLATED/NEUTRAL_RESET fork"
                textSize = 14f
                gravity = Gravity.CENTER_HORIZONTAL
                setPadding(0, dp(8), 0, dp(18))
            }
        )

        statusView = TextView(this).apply {
            text = "P3.7 fork probe starting…"
            textSize = 20f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(8), dp(18), dp(8), dp(18))
        }

        detailView = TextView(this).apply {
            text = "Waiting for Torch import, the sealed Numogram lifecycle, and the fork."
            textSize = 13f
            setPadding(dp(8), dp(12), dp(8), dp(12))
        }

        root.addView(statusView)
        root.addView(detailView)

        root.addView(
            TextView(this).apply {
                text =
                    "\nP3.7 boundary:\n\n" +
                    "Kotlin\n" +
                    "  ↓\n" +
                    "NumogramBridge\n" +
                    "  ↓\n" +
                    "Python 3.8 · Numogram.py\n" +
                    "  ↓\n" +
                    "initialize (fresh OR reattach) → status → transition(Z3)\n" +
                    "  → run_fork(Z3): FULL, ABLATED_TRANSITION, ABLATED_MAGNETISM,\n" +
                    "    ABLATED_BOTH, NEUTRAL_RESET, sealed from one captured\n" +
                    "    pre-state, none of them mutating the live system\n" +
                    "  → verify_last_fork → status\n" +
                    "  ↓\n" +
                    "Kotlin\n\n" +
                    "Fixed probe: seed 3606 · dimension 3 · origin Z3 · context {}\n\n" +
                    "One real transition is committed from Z3 first, so the fork " +
                    "runs against a state that actually has something learned in " +
                    "it -- forking a cold, never-committed system would trivially " +
                    "show every ABLATED_* condition equal to FULL, which confirms " +
                    "nothing. The fork itself always runs from Z3 again, regardless " +
                    "of where that committed transition landed, so a repeat launch " +
                    "stays comparable to earlier ones rather than forking from a " +
                    "different, accumulating starting zone each time.\n\n" +
                    "No language model. No network. Persistence disabled."
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
                    .put("schema", "amelia-p3.7-probe-result-v1")
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
        val postTransition = JSONObject(bridge.status())
        val forked = JSONObject(bridge.runFork(PROBE_ORIGIN, "{}"))
        val verified = JSONObject(bridge.verifyLastFork())
        val finalStatus = JSONObject(bridge.status())

        return JSONObject()
            .put("schema", "amelia-p3.7-probe-result-v1")
            .put("status", "completed")
            .put("runtime", runtime)
            .put("before", before)
            .put("initialized", initialized)
            .put("ready", ready)
            .put("transitioned", transitioned)
            .put("post_transition", postTransition)
            .put("forked", forked)
            .put("verified", verified)
            .put("final", finalStatus)
            .toString()
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
                    forkHeld &&
                    verifyHeld &&
                    finalHeld

            val initKind = if (initStatus == "already_initialized") {
                "reattached to existing system (digest-matched)"
            } else {
                "fresh initialization"
            }
            val transitionLine = "Z" + event.optInt("from") + " → Z" + event.optInt("to")

            if (passed) {
                statusView.text = "P3.7 PASSED ✓"
                detailView.text =
                    "Torch imported, one transition committed, and the five-condition " +
                        "fork ran and replay-verified without touching live state.\n\n" +
                        "Torch: " + torchVersion + "\n" +
                        "Before initialization: " + before.optString("status") + "\n" +
                        "Initialization: " + initKind + "\n" +
                        "Step baseline going in: " + baselineStep + "\n" +
                        "Committed transition: " + transitionLine + "\n\n" +
                        "Fork branches (all from Z3):\n" + branchLines.toString() + "\n" +
                        "live_state_unchanged: " + liveStateUnchanged + "\n" +
                        "generator_state_unchanged: " + generatorStateUnchanged + "\n" +
                        "ablated_both_matches_neutral_reset: " + ablatedMatchesNeutral + "\n" +
                        "verify_last_fork: " + verified.optString("status") + "\n\n" +
                        "Step after: " + finalSystem.optInt("evolution_step") + "\n" +
                        "History: " + finalSystem.optInt("transition_history") + "\n" +
                        "Persistence: " + finalSystem.optBoolean("persistence_enabled")
            } else {
                statusView.text = "P3.7 FAIL-CLOSED"
                detailView.text =
                    "A Torch/Numogram response was received, but it did not satisfy " +
                        "the sealed P3.7 contract.\n\n" +
                        "Torch ready: " + torchReady + "\n" +
                        "Initialization: " + initializationHeld + " (" + initStatus + ")\n" +
                        "Ready state: " + readyHeld + "\n" +
                        "Transition: " + transitionHeld + "\n" +
                        "Fork: " + forkHeld + " (branches well-formed: " + branchesWellFormed + ")\n" +
                        "  live_state_unchanged: " + liveStateUnchanged + "\n" +
                        "  generator_state_unchanged: " + generatorStateUnchanged + "\n" +
                        "  ablated_both_matches_neutral_reset: " + ablatedMatchesNeutral + "\n" +
                        "Verify: " + verifyHeld + "\n" +
                        "Final state: " + finalHeld + "\n\n" +
                        "Raw response:\n" + raw
            }
        } catch (t: Throwable) {
            statusView.text = "P3.7 FAIL-CLOSED"
            detailView.text =
                "The returned Torch/Numogram value was not valid P3.7 probe JSON.\n\n" +
                    "Error: " + (t.message ?: "Unknown parsing error") + "\n\n" +
                    "Raw response:\n" + raw
        }
    }

    private fun dp(value: Int): Int {
        return (value * resources.displayMetrics.density).toInt()
    }
}
