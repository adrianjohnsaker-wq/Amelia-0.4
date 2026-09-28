package com.amelia.p314r

import android.app.Activity
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.exp1r.P314RExperimentBridge
import org.json.JSONObject
import java.io.File

/**
 * Amelia P3.14R — prospective replication of the 666 operator signal.
 *
 * Progress and checkpoint state are visible. Inferential statistics remain
 * hidden until every prespecified code and seed has completed.
 */
class MainActivity : Activity() {

    private lateinit var runButton: Button
    private lateinit var statusView: TextView
    private lateinit var protocolView: TextView
    private lateinit var progressView: TextView
    private lateinit var primaryView: TextView
    private lateinit var seedRegimeView: TextView
    private lateinit var evidenceView: TextView

    @Volatile
    private var running = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(22), dp(18), dp(30))
        }

        root.addView(TextView(this).apply {
            text = "AMELIA · P3.14R"
            textSize = 25f
            gravity = Gravity.CENTER_HORIZONTAL
        })

        root.addView(TextView(this).apply {
            text = "666 FRESH-SEED REPLICATION · SEED-REGIME TEST"
            textSize = 14f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(8), 0, dp(16))
        })

        statusView = TextView(this).apply {
            text =
                "Ready. This is a prospective replication using 40 new seeds. " +
                    "Partial statistics remain hidden until the full root-9 " +
                    "population is complete."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(statusView)

        root.addView(sectionHeading("LOCKED REPLICATION PROTOCOL"))
        protocolView = TextView(this).apply {
            text = "Loading protocol…"
            textSize = 12f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(protocolView)

        runButton = Button(this).apply {
            text = "START / RESUME SEALED 666 REPLICATION"
            setOnClickListener { startOrResume() }
        }
        root.addView(runButton)

        root.addView(sectionHeading("EXECUTION PROGRESS"))
        progressView = TextView(this).apply {
            text = "Checking checkpoint…"
            textSize = 14f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(progressView)

        root.addView(sectionHeading("PRIMARY REPLICATION ENDPOINT"))
        primaryView = TextView(this).apply {
            text = "Inferential result withheld until completion."
            textSize = 13f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(primaryView)

        root.addView(sectionHeading("SECONDARY SEED-REGIME ENDPOINT"))
        seedRegimeView = TextView(this).apply {
            text = "Inferential result withheld until completion."
            textSize = 13f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(seedRegimeView)

        root.addView(sectionHeading("SEALED EVIDENCE"))
        evidenceView = TextView(this).apply {
            text = "No final evidence archive yet."
            textSize = 12f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(evidenceView)

        root.addView(TextView(this).apply {
            text =
                "Primary: 666 must replicate against the exact P3.14A root-9 " +
                    "control universe in both balanced 20-seed cohorts, retain " +
                    "the late-window effect, and satisfy the existing stability " +
                    "criterion. Secondary: code×seed interaction dispersion and " +
                    "start-zone structure are tested separately and cannot rescue " +
                    "a failed primary replication."
            textSize = 12f
            setPadding(dp(4), dp(14), dp(4), 0)
        })

        scroll.addView(root)
        setContentView(scroll)

        loadManifestAndCheckpoint()
    }

    private fun archiveDir(): File =
        File(filesDir, "p314r-666-replication")

    private fun loadManifestAndCheckpoint() {
        Thread {
            try {
                val bridge = P314RExperimentBridge(applicationContext)
                val manifest = JSONObject(bridge.protocolManifest())
                val checkpoint = JSONObject(
                    bridge.checkpointStatus(archiveDir().absolutePath)
                )

                runOnUiThread {
                    protocolView.text = buildString {
                        append("Protocol SHA-256:\n")
                        append(manifest.optString("protocol_sha256", "missing"))
                        append("\n\nNumogram SHA-256:\n")
                        append(BuildConfig.NUMOGRAM_SHA256)
                        append("\n\nExperiment SHA-256:\n")
                        append(BuildConfig.EXPERIMENT_SHA256)
                        append("\n\nProtocol-file SHA-256:\n")
                        append(BuildConfig.PROTOCOL_FILE_SHA256)
                        append("\n\nBuild revision:\n")
                        append(BuildConfig.BUILD_REVISION)
                    }
                    renderCheckpoint(checkpoint)
                }
            } catch (error: Throwable) {
                runOnUiThread {
                    progressView.text =
                        "Checkpoint inspection error: " +
                            "${error::class.java.simpleName}: ${error.message}"
                }
            }
        }.start()
    }

    private fun renderCheckpoint(checkpoint: JSONObject) {
        when (checkpoint.optString("status", "unknown")) {
            "not_started" -> {
                progressView.text = "Not started."
            }
            "in_progress" -> {
                progressView.text = buildString {
                    append("Checkpoint found.\n")
                    append("Shams: ")
                    append(checkpoint.optInt("completed_shams", 0))
                    append(" / ")
                    append(checkpoint.optInt("total_shams", 40))
                    append("\nCodes: ")
                    append(checkpoint.optInt("completed_codes", 0))
                    append(" / ")
                    append(checkpoint.optInt("total_codes", 98))
                    append("\nProgress: ")
                    append(format2(checkpoint.optDouble("percent", 0.0)))
                    append("%")
                }
            }
            "completed" -> renderFinal(checkpoint)
            else -> progressView.text = checkpoint.toString(2)
        }
    }

    private fun startOrResume() {
        if (running) return
        running = true
        runButton.isEnabled = false
        statusView.text =
            "Replication running. Checkpoints are sealed after each completed " +
                "chunk. Keep Amelia open when possible; reopening the app can resume."

        Thread {
            val bridge = P314RExperimentBridge(applicationContext)
            var finished = false

            while (!finished) {
                val raw = try {
                    bridge.runNext(
                        archiveDir().absolutePath,
                        BuildConfig.NUMOGRAM_SHA256,
                        BuildConfig.EXPERIMENT_SHA256,
                        BuildConfig.PROTOCOL_FILE_SHA256,
                        BuildConfig.BUILD_REVISION
                    )
                } catch (error: Throwable) {
                    JSONObject()
                        .put("status", "error")
                        .put("error_type", error::class.java.simpleName)
                        .put("message", error.message ?: "Unknown error")
                        .toString()
                }

                val result = try {
                    JSONObject(raw)
                } catch (error: Throwable) {
                    JSONObject()
                        .put("status", "error")
                        .put("error_type", "InvalidJson")
                        .put("message", raw)
                }

                when (result.optString("status", "error")) {
                    "progress" -> runOnUiThread { renderProgress(result) }
                    "completed" -> {
                        runOnUiThread { renderFinal(result) }
                        finished = true
                    }
                    else -> {
                        runOnUiThread {
                            statusView.text = "P3.14R stopped."
                            progressView.text = buildString {
                                append(result.optString("error_type", "error"))
                                append(": ")
                                append(result.optString("message", "unknown"))
                            }
                        }
                        finished = true
                    }
                }
            }

            running = false
            runOnUiThread {
                if (!primaryView.text.toString().contains("REPLICATION HELD")) {
                    runButton.isEnabled = true
                }
            }
        }.start()
    }

    private fun renderProgress(result: JSONObject) {
        progressView.text = buildString {
            append("Phase: ")
            append(result.optString("phase", "unknown"))
            append("\nShams: ")
            append(result.optInt("completed_shams", 0))
            append(" / ")
            append(result.optInt("total_shams", 40))
            append("\nCodes: ")
            append(result.optInt("completed_codes", 0))
            append(" / ")
            append(result.optInt("total_codes", 98))
            append("\nProgress: ")
            append(format2(result.optDouble("percent", 0.0)))
            append("%")
            append("\nCheckpoint: SEALED")
            append("\nPartial statistics: WITHHELD")
        }
    }

    private fun renderFinal(result: JSONObject) {
        val primary = result.optJSONObject("primary_replication")
        val secondary = result.optJSONObject("secondary_seed_regime")

        if (primary == null) {
            statusView.text = "Completed, but primary result is unavailable."
            progressView.text = result.toString(2)
            return
        }

        val held = result.optBoolean("replication_held", false)

        statusView.text =
            if (held) {
                "Completed. 666 met the preregistered fresh-seed replication gate."
            } else {
                "Completed. 666 did not meet the preregistered fresh-seed replication gate."
            }

        progressView.text =
            "COMPLETE · final inferential results unlocked."

        primaryView.text = buildString {
            append("REPLICATION HELD: ")
            append(held)
            append("\nOverall percentile: ")
            append(format1(primary.optDouble("primary_percentile", Double.NaN)))
            append("\nRank p: ")
            append(format4(primary.optDouble("rank_p_upper", Double.NaN)))
            append("\nCohort A percentile: ")
            append(format1(primary.optDouble("cohort_a_percentile", Double.NaN)))
            append("\nCohort B percentile: ")
            append(format1(primary.optDouble("cohort_b_percentile", Double.NaN)))
            append("\nLate percentile: ")
            append(format1(primary.optDouble("late_percentile", Double.NaN)))
            append("\nStable: ")
            append(primary.optBoolean("reproducibility_held", false))
            append("\nAdvance to P3.14B: ")
            append(result.optBoolean("advance_to_p314b", false))
            append("\nNext: ")
            append(result.optString("next_required_stage", "unknown"))
        }

        if (secondary != null) {
            val interaction = secondary.optJSONObject("interaction_dispersion")
            val zone = secondary.optJSONObject("start_zone_variance")

            seedRegimeView.text = buildString {
                append("CODE×SEED INTERACTION\n")
                if (interaction != null) {
                    append("percentile: ")
                    append(format1(interaction.optDouble("percentile", Double.NaN)))
                    append("\np: ")
                    append(format4(interaction.optDouble("rank_p_upper", Double.NaN)))
                    append("\nHolm q: ")
                    append(format4(interaction.optDouble("holm_q", Double.NaN)))
                    append("\nheld: ")
                    append(interaction.optBoolean("held", false))
                }

                append("\n\nSTART-ZONE STRUCTURE\n")
                if (zone != null) {
                    append("percentile: ")
                    append(format1(zone.optDouble("percentile", Double.NaN)))
                    append("\np: ")
                    append(format4(zone.optDouble("rank_p_upper", Double.NaN)))
                    append("\nHolm q: ")
                    append(format4(zone.optDouble("holm_q", Double.NaN)))
                    append("\nheld: ")
                    append(zone.optBoolean("held", false))
                }
            }
        }

        evidenceView.text = buildString {
            append("Evidence SHA-256:\n")
            append(result.optString("evidence_sha256", "missing"))
            append("\n\nArchive:\n")
            append(result.optString("archive_file", "missing"))
            append("\n\nDiscovery evidence SHA-256:\n")
            append(result.optString("discovery_evidence_sha256", "missing"))
            append("\n\nProtocol SHA-256:\n")
            append(result.optString("protocol_sha256", "missing"))
        }

        runButton.isEnabled = false
    }

    private fun sectionHeading(textValue: String): TextView =
        TextView(this).apply {
            text = textValue
            textSize = 18f
            setPadding(0, dp(16), 0, dp(4))
        }

    private fun format1(value: Double): String =
        if (value.isNaN()) "NA" else String.format("%.1f", value)

    private fun format2(value: Double): String =
        if (value.isNaN()) "NA" else String.format("%.2f", value)

    private fun format4(value: Double): String =
        if (value.isNaN()) "NA" else String.format("%.4f", value)

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density).toInt()
}
