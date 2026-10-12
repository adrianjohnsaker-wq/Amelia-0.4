package com.amelia.driftg11

import android.app.Activity
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import android.widget.*
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import org.json.JSONObject
import java.io.File
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private val worker = Executors.newSingleThreadExecutor()
    private lateinit var banner: TextView
    private lateinit var detail: TextView
    private lateinit var seed: EditText
    private val buttons = mutableListOf<Button>()
    private var engine: PyObject? = null
    private var ready = false
    private var pendingExport: File? = null
    private val runRoot get() = File(filesDir, "drift_runs").absolutePath

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(18), dp(18), dp(12))
            setBackgroundColor(Color.rgb(244, 247, 247))
        }
        root.addView(TextView(this).apply { text = "AMELIA · DRIFT-1A"; textSize = 24f; setTextColor(Color.rgb(18,67,67)) })
        root.addView(TextView(this).apply {
            text = "G1.1 · Canonical / graph control / memory reset\nOffline synthetic runs · saved after every tick"
            textSize = 13f; setPadding(0, dp(6), 0, dp(12))
        })
        banner = TextView(this).apply { text = "Checking source integrity and device parity…"; textSize = 16f }
        root.addView(banner)
        val inputs = LinearLayout(this)
        seed = EditText(this).apply { hint = "Seed"; setText("101"); inputType = 2; contentDescription = "Synthetic seed" }
        inputs.addView(seed, LinearLayout.LayoutParams(0, -2, 1f))
        root.addView(inputs)
        fun row(vararg actions: Pair<String, () -> Unit>) {
            val line = LinearLayout(this)
            for ((label, action) in actions) {
                val button = Button(this).apply { text = label; isEnabled = false; setOnClickListener { action() } }
                buttons.add(button)
                line.addView(button, LinearLayout.LayoutParams(0, -2, 1f))
            }
            root.addView(line)
        }
        row("New run" to {
            val s = seed.text.toString().toLongOrNull()
            if (s == null || s !in 0L..2147483647L) {
                banner.text = "Enter a seed from 0 to 2147483647."
            } else {
                task("Creating run…") { renderLater(engine!!.callAttr("create", runRoot, s).toString()) }
            }
        }, "Verify run" to {
            task("Replaying saved run…") {
                val message = engine!!.callAttr("verify_run", runRoot).toString()
                runOnUiThread { banner.text = message }
            }
        })
        row("1 tick" to { advance(1) }, "32 ticks" to { advance(32) }, "Finish 512" to { advance(512) })
        row("Export evidence" to { exportEvidence() })
        detail = TextView(this).apply { textSize = 14f; setTextIsSelectable(true); setPadding(0,dp(12),0,0) }
        root.addView(ScrollView(this).apply { addView(detail) }, LinearLayout.LayoutParams(-1,0,1f))
        setContentView(root)
        task("Checking source integrity and device parity…") {
            val manifest = assets.open("g11_runtime/runtime_manifest.json").bufferedReader().use { it.readText() }
            val digest = JSONObject(manifest).getString("digest")
            val runtime = File(filesDir,"g11_code/$digest")
            copyAssets("g11_runtime",runtime)
            engine = Python.getInstance().getModule("drift_bootstrap").callAttr("load",runtime.absolutePath)
            val parity = engine!!.callAttr("check_reference").toString()
            ready = true
            Log.i("DRIFT_G11",parity)
            val state = engine!!.callAttr("status",runRoot).toString()
            renderLater(state)
            runOnUiThread { banner.text = "G1.1 device parity: PASS · ready" }
            if (intent.getBooleanExtra("g11_smoke",false)) {
                engine!!.callAttr("create",runRoot,101)
                renderLater(engine!!.callAttr("advance",runRoot,512).toString())
                val result = engine!!.callAttr("verify_run",runRoot).toString()
                engine!!.callAttr("export_zip",runRoot,File(filesDir,"g11-smoke-evidence.zip").absolutePath)
                Log.i("DRIFT_G11","G11_SMOKE_PASS $result")
                runOnUiThread { banner.text = "G11_SMOKE_PASS · 512 ticks replayed" }
            }
        }
    }

    private fun advance(n: Int) {
        task("Advancing and saving…") { renderLater(engine!!.callAttr("advance",runRoot,n).toString()) }
    }

    private fun task(message: String, action: () -> Unit) {
        buttons.forEach { it.isEnabled = false }
        banner.text = message
        worker.execute {
            try { action() }
            catch (e: Exception) {
                Log.e("DRIFT_G11","Operation failed",e)
                runOnUiThread { banner.text = "Stopped: ${e.message}" }
            }
            finally { runOnUiThread { buttons.forEach { it.isEnabled = ready } } }
        }
    }

    private fun renderLater(raw: String) = runOnUiThread {
        val r = JSONObject(raw)
        if (!r.optBoolean("exists")) {
            detail.text = "Source integrity and device parity are checked on launch.\n\nChoose New run to begin.\n\nEach tick contains one legal move. Uniform entry is used at episode starts. Boundary: 0, 3, 6, 9. Each run follows 512 fixed synthetic inputs shared across C, G and M. No live beacon or language model is used. Previous runs are retained when you create a new one."
            return@runOnUiThread
        }
        banner.text = "Saved ${r.getInt("ticks")} / ${r.getInt("limit")} ticks"
        val text = StringBuilder("Seed ${r.getInt("seed")} · uniform entry · one move/tick\n\n")
        val zones = r.getJSONObject("zones")
        val counts = r.getJSONObject("counts")
        for (a in listOf("C","G","M")) {
            val label = when(a) { "C" -> "Canonical + memory"; "G" -> "Rewired + memory"; else -> "Canonical + reset" }
            text.append("$a · $label\nCurrent zone: ${zones.getInt(a)}\nPost-move visits 0–9: ${counts.getJSONArray(a)}\n")
            if (r.getJSONObject("last_events").has(a)) {
                val event = r.getJSONObject("last_events").getJSONObject(a)
                val edge = event.getJSONArray("selected_edge")
                val selection = event.getJSONObject("selection")
                text.append("Last: ${edge.getInt(0)} → ${edge.getInt(1)} (${edge.getString(2)})\n")
                text.append("Commitment: ${!selection.isNull("commitment_bias")} · retention floor: ${selection.getJSONObject("retention").getBoolean("floor_applied")}\n")
            }
            val metrics = r.getJSONObject("metrics").getJSONObject(a)
            text.append("Episodes: ${metrics.getInt("completed_episodes")} · Warp: ${metrics.getInt("warp")} · Plex: ${metrics.getInt("plex")}\n")
            text.append("Mean completed length: ${metrics.optDouble("mean_completed_length")} · unfinished: ${!metrics.isNull("right_censored")}\n")
            text.append('\n')
        }
        text.append("Evidence head\n${r.getString("ledger_head")}\n\nRun ${r.getString("session")}\n\nEngineering pilot only; not a registered live experiment.")
        detail.text = text.toString()
    }

    private fun exportEvidence() {
        task("Preparing evidence archive…") {
            val file = File(cacheDir,"Amelia-DRIFT1A-G11-evidence.zip")
            engine!!.callAttr("export_zip",runRoot,file.absolutePath)
            pendingExport = file
            runOnUiThread {
                val intent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE); type = "application/zip"
                    putExtra(Intent.EXTRA_TITLE,"Amelia-DRIFT1A-G11-evidence.zip")
                }
                startActivityForResult(intent,100)
                banner.text = "Choose where to save the evidence archive."
            }
        }
    }

    @Deprecated("Legacy callback supported on Android 7+")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode,resultCode,data)
        val uri = data?.data
        if (requestCode == 100 && resultCode == RESULT_OK && uri != null) {
            task("Exporting…") {
                contentResolver.openOutputStream(uri).use { out ->
                    requireNotNull(out) { "Cannot open export destination" }
                    pendingExport!!.inputStream().use { it.copyTo(out) }
                }
                runOnUiThread { banner.text = "Evidence exported." }
            }
        }
    }

    private fun copyAssets(source: String, target: File) {
        val children = assets.list(source) ?: emptyArray()
        if (children.isEmpty()) {
            target.parentFile?.mkdirs()
            assets.open(source).use { input -> target.outputStream().use { input.copyTo(it) } }
        } else {
            target.mkdirs()
            children.forEach { copyAssets("$source/$it",File(target,it)) }
        }
    }
    override fun onDestroy() {
        worker.shutdown()
        super.onDestroy()
    }

    private fun dp(n: Int) = (n*resources.displayMetrics.density).toInt()
}
