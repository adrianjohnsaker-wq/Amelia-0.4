package com.amelia.p314

import android.app.Activity
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.amelia.exp1.P314Experiment1Bridge
import org.json.JSONObject
import java.io.File

/**
 * Amelia P3.14 — Experiment 1A.
 *
 * Numerical-operator specificity assay.
 *
 * Frozen upstream:
 *   P3.12 causal incorporation assay: untouched.
 *   P3.13 renderer-faithfulness assay: untouched.
 *
 * P3.14 is intentionally offline and independent of both. No language model,
 * no ProcessFieldMemory and no semantic interpretation enters this assay.
 */
class MainActivity : Activity() {

    private lateinit var runButton: Button
    private lateinit var statusView: TextView
    private lateinit var protocolView: TextView
    private lateinit var endpointView: TextView
    private lateinit var targetsView: TextView
    private lateinit var evidenceView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(22), dp(18), dp(30))
        }

        root.addView(TextView(this).apply {
            text = "AMELIA · P3.14"
            textSize = 25f
            gravity = Gravity.CENTER_HORIZONTAL
        })

        root.addView(TextView(this).apply {
            text = "EXPERIMENT 1A · NUMERICAL-OPERATOR SPECIFICITY"
            textSize = 14f
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(8), 0, dp(16))
        })

        statusView = TextView(this).apply {
            text =
                "Ready. This is a sealed offline assay. 333, 137, 666 and 360 " +
                    "are treated only as numerical zone-address operators. " +
                    "All measurements occur after the numerical pulse has been removed."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(statusView)

        root.addView(sectionHeading("LOCKED PROTOCOL"))
        protocolView = TextView(this).apply {
            text = "Loading protocol fingerprint…"
            textSize = 12f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(protocolView)

        runButton = Button(this).apply {
            text = "RUN SEALED EXPERIMENT 1A"
            setOnClickListener { runExperiment() }
        }
        root.addView(runButton)

        root.addView(sectionHeading("PRIMARY ENDPOINT"))
        endpointView = TextView(this).apply {
            text = "No assay run yet."
            textSize = 14f
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(endpointView)

        root.addView(sectionHeading("TARGET-CODE RESULTS"))
        targetsView = TextView(this).apply {
            text = "No results yet."
            textSize = 12f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(targetsView)

        root.addView(sectionHeading("SEALED EVIDENCE"))
        evidenceView = TextView(this).apply {
            text = "No evidence archive yet."
            textSize = 12f
            typeface = Typeface.MONOSPACE
            setPadding(dp(4), dp(8), dp(4), dp(14))
        }
        root.addView(evidenceView)

        root.addView(TextView(this).apply {
            text =
                "P3.14 does not alter Numogram.py and does not invoke the P3.12/P3.13 " +
                    "packages. The reference population is exhaustive: every three-digit " +
                    "integer with the same digital root as a target is evaluated. " +
                    "A positive P3.14A result still cannot advance directly to Experiment 2; " +
                    "it must first survive the prespecified P3.14B topology/label-shuffle test."
            textSize = 12f
            setPadding(dp(4), dp(14), dp(4), 0)
        })

        scroll.addView(root)
        setContentView(scroll)

        loadProtocol()
    }

    private fun loadProtocol() {
        Thread {
            val text = try {
                val bridge = P314Experiment1Bridge(applicationContext)
                val manifest = JSONObject(bridge.protocolManifest())
                buildString {
                    append("Protocol SHA-256:\n")
                    append(manifest.optString("protocol_sha256", "missing"))
                    append("\n\nNumogram SHA-256:\n")
                    append(manifest.optString("numogram_source_sha256", "missing"))
                    append("\n\nExperiment source SHA-256:\n")
                    append(manifest.optString("experiment_source_sha256", "missing"))
                }
            } catch (error: Throwable) {
                "Protocol load error: ${error::class.java.simpleName}: ${error.message}"
            }

            runOnUiThread {
                protocolView.text = text
            }
        }.start()
    }

    private fun runExperiment() {
        runButton.isEnabled = false
        statusView.text =
            "Running the full sealed root-matched population. Keep Amelia open. " +
                "No renderer or network call is involved."
        endpointView.text = "Experiment in progress…"
        targetsView.text = "Waiting for all prespecified codes and controls…"
        evidenceView.text = "Archive will be created only after the assay completes."

        Thread {
            val raw = try {
                val bridge = P314Experiment1Bridge(applicationContext)
                val archiveDir = File(filesDir, "p314-exp1a")
                bridge.runExperiment(archiveDir.absolutePath)
            } catch (error: Throwable) {
                JSONObject()
                    .put("schema", "amelia-p3.14-exp1a-android-v1")
                    .put("status", "error")
                    .put("error_type", error::class.java.simpleName)
                    .put("message", error.message ?: "Unknown P3.14 error")
                    .toString()
            }

            runOnUiThread {
                renderResult(raw)
                runButton.isEnabled = true
            }
        }.start()
    }

    private fun renderResult(raw: String) {
        try {
            val result = JSONObject(raw)
            val status = result.optString("status", "unknown")

            if (status != "success") {
                statusView.text = "P3.14 stopped: $status"
                endpointView.text = buildString {
                    append("No scientific endpoint was accepted.\n")
                    append(result.optString("error_type", ""))
                    val message = result.optString("message", "")
                    if (message.isNotBlank()) {
                        append("\n")
                        append(message)
                    }
                }
                return
            }

            val held = result.optBoolean("operator_specificity_held", false)
            val family = result.getJSONObject("family_randomization")
            val confirmed = result.optJSONArray("confirmed_targets")

            statusView.text =
                if (held) {
                    "Completed. P3.14A met its preregistered operator-specificity gate."
                } else {
                    "Completed. P3.14A did not meet its preregistered operator-specificity gate."
                }

            endpointView.text = buildString {
                append("OPERATOR SPECIFICITY HELD: ")
                append(held)
                append("\nFamily randomization p: ")
                append(format6(family.optDouble("upper_tail_p", Double.NaN)))
                append("\nConfirmed targets: ")
                if (confirmed == null || confirmed.length() == 0) {
                    append("none")
                } else {
                    for (i in 0 until confirmed.length()) {
                        if (i > 0) append(", ")
                        append(confirmed.getInt(i))
                    }
                }
                append("\nAdvance to Experiment 2: false")
                append("\nNext required stage: ")
                append(result.optString("next_required_stage", "unknown"))
            }

            val targets = result.getJSONObject("target_results")
            val order = listOf("333", "137", "666", "360")
            targetsView.text = buildString {
                append("code  pct    p       q       D-split C-split late   stable held\n")
                order.forEach { code ->
                    val item = targets.getJSONObject(code)
                    append(code.padEnd(5))
                    append(format1(item.optDouble("primary_percentile", Double.NaN)).padStart(5))
                    append("  ")
                    append(format4(item.optDouble("rank_p_upper", Double.NaN)).padStart(6))
                    append("  ")
                    append(format4(item.optDouble("bh_q", Double.NaN)).padStart(6))
                    append("  ")
                    append(format1(item.optDouble("discovery_percentile", Double.NaN)).padStart(6))
                    append("  ")
                    append(format1(item.optDouble("confirmatory_percentile", Double.NaN)).padStart(6))
                    append("  ")
                    append(format1(item.optDouble("late_percentile", Double.NaN)).padStart(5))
                    append("  ")
                    append(if (item.optBoolean("reproducibility_held", false)) "yes" else "no ")
                    append("    ")
                    append(if (item.optBoolean("individual_held", false)) "YES" else "no")
                    append("\n")
                }
            }

            evidenceView.text = buildString {
                append("Evidence SHA-256:\n")
                append(result.optString("evidence_sha256", "missing"))
                append("\n\nArchive:\n")
                append(result.optString("archive_file", "missing"))
                append("\n\nElapsed seconds: ")
                append(format1(result.optDouble("elapsed_seconds", Double.NaN)))
                append("\n\nProtocol SHA-256:\n")
                append(result.optString("protocol_sha256", "missing"))
                append("\n\nNumogram SHA-256:\n")
                append(result.optString("numogram_source_sha256", "missing"))
            }
        } catch (error: Throwable) {
            statusView.text = "Could not parse P3.14 result."
            endpointView.text =
                "${error::class.java.simpleName}: ${error.message}\n\n$raw"
        }
    }

    private fun sectionHeading(textValue: String): TextView =
        TextView(this).apply {
            text = textValue
            textSize = 18f
            setPadding(0, dp(16), 0, dp(4))
        }

    private fun format1(value: Double): String =
        if (value.isNaN()) "NA" else String.format("%.1f", value)

    private fun format4(value: Double): String =
        if (value.isNaN()) "NA" else String.format("%.4f", value)

    private fun format6(value: Double): String =
        if (value.isNaN()) "NA" else String.format("%.6f", value)

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density).toInt()
}
