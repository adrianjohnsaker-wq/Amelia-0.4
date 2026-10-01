package com.amelia.one

import android.app.Activity
import android.os.Bundle
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.chaquo.python.Python
import org.json.JSONObject

/**
 * Android Amelia 1.0, milestone M1.
 * Runs the canonical integrity check on start. Only if it is ACCEPTED does it run the
 * reference substrate lineage and compare its state digests with CI's (MATCH or MISMATCH).
 */
class MainActivity : Activity() {
    private lateinit var status: TextView
    private lateinit var detail: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16), dp(16), dp(16), dp(16))
        }
        root.addView(TextView(this).apply {
            text = "AMELIA 1.0 · M1"; textSize = 23f; gravity = Gravity.CENTER_HORIZONTAL
        })
        root.addView(TextView(this).apply {
            text = "Canonical integrity · substrate reproduction · offline"
            textSize = 12f; gravity = Gravity.CENTER_HORIZONTAL; setPadding(0, dp(4), 0, dp(12))
        })
        status = TextView(this).apply { text = "Checking…"; textSize = 20f; gravity = Gravity.CENTER_HORIZONTAL }
        root.addView(status)
        detail = TextView(this).apply { textSize = 13f; setPadding(0, dp(12), 0, 0); setTextIsSelectable(true) }
        root.addView(ScrollView(this).apply { addView(detail) }, LinearLayout.LayoutParams(-1, 0, 1f))
        setContentView(root)

        Thread {
            val raw = try {
                Python.getInstance().getModule("amelia_core").callAttr("startup_check").toString()
            } catch (e: Exception) {
                JSONObject().put("ok", false).put("status", "REFUSED").put("reason", e.message ?: "Python failure").toString()
            }
            runOnUiThread { render(raw) }
            if (JSONObject(raw).optBoolean("ok", false)) {
                val ref = try {
                    Python.getInstance().getModule("amelia_core").callAttr("reference_check").toString()
                } catch (e: Exception) {
                    JSONObject().put("ok", false).put("status", "ERROR").put("reason", e.message ?: "Python failure").toString()
                }
                runOnUiThread { renderReference(ref) }
            }
        }.start()
    }

    private fun render(raw: String) {
        val r = JSONObject(raw)
        status.text = r.optString("status", "REFUSED")
        val sb = StringBuilder()
        sb.append("Version: ").append(r.optString("version")).append('\n')
        sb.append("Python: ").append(r.optString("python")).append('\n')
        if (r.has("integrity_mode")) {
            sb.append("Integrity: ").append(r.optString("integrity_mode")).append('\n')
        }
        if (!r.optBoolean("ok", false)) sb.append("Reason: ").append(r.optString("reason")).append('\n')
        if (r.has("canonical_digest")) {
            sb.append("\nCanonical digest:\n").append(r.optString("canonical_digest")).append('\n')
            sb.append("Graph digest:\n").append(r.optString("graph_digest")).append('\n')
            sb.append("Edges: ").append(r.optInt("edges")).append("  ").append(r.optJSONObject("edge_counts")?.toString() ?: "").append('\n')
        }
        val modules = r.optJSONObject("modules")
        if (modules != null) {
            sb.append("\nModules:\n")
            val keys = modules.keys()
            while (keys.hasNext()) {
                val k = keys.next()
                val m = modules.getJSONObject(k)
                val actual = m.optString("actual")
                val verification = m.optString("verification")
                sb.append(if (m.optBoolean("match")) "  ✓ " else "  ✗ ").append(k)
                if (actual.isNotBlank() && actual != "null") {
                    sb.append("  ").append(actual.take(16))
                } else if (verification.isNotBlank()) {
                    sb.append("  [").append(verification).append("]")
                }
                sb.append('\n')
            }
        }
        detail.text = sb.toString()
    }

    private fun renderReference(raw: String) {
        val r = JSONObject(raw)
        val sb = StringBuilder(detail.text)
        sb.append("\nSubstrate reference run: ").append(r.optString("status")).append('\n')
        val d = r.optJSONObject("device")
        if (d != null) {
            sb.append("  seed ").append(d.optInt("seed")).append(", ").append(d.optInt("episodes")).append(" episodes\n")
            sb.append("  P ").append(d.optString("digest_P").take(16)).append('\n')
            sb.append("  H ").append(d.optString("digest_H").take(16)).append('\n')
        }
        if (r.has("reason")) sb.append("  ").append(r.optString("reason")).append('\n')
        detail.text = sb.toString()
        status.text = status.text.toString() + " · " + r.optString("status")
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()
}
