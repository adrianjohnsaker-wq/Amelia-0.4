package com.amelia.exp1r

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * Narrow bridge for the P3.14R 666 fresh-seed replication.
 */
class P314RExperimentBridge(private val context: Context) {

    private fun module() = run {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        Python.getInstance().getModule("P314RExperiment")
    }

    fun protocolManifest(): String =
        module().callAttr("protocol_manifest").toString()

    fun checkpointStatus(archiveDir: String): String =
        module()
            .callAttr("checkpoint_status", archiveDir)
            .toString()

    fun runNext(
        archiveDir: String,
        numogramSha256: String,
        experimentSha256: String,
        protocolFileSha256: String,
        buildRevision: String
    ): String =
        module()
            .callAttr(
                "run_next",
                archiveDir,
                numogramSha256,
                experimentSha256,
                protocolFileSha256,
                buildRevision
            )
            .toString()
}
