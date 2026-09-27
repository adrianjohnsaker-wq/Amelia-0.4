package com.amelia.exp1

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * Narrow bridge for P3.14 Experiment 1A.
 *
 * This bridge exposes only the frozen protocol manifest and the sealed assay.
 * It does not call the renderer, PFM, P3.12 or P3.13.
 */
class P314Experiment1Bridge(private val context: Context) {

    private fun module() = run {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        Python.getInstance().getModule("P314Experiment1")
    }

    fun protocolManifest(): String =
        module().callAttr("protocol_manifest").toString()

    fun runExperiment(archiveDir: String): String =
        module().callAttr("run_experiment", archiveDir).toString()
}
