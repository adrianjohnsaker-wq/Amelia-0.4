package com.amelia.assay

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * Narrow Kotlin bridge for the P3.12 matched causal incorporation assay.
 *
 * P3.12 uses fresh throwaway Numogram instances inside P312AssayCore.py.
 * It does not reset or mutate the P3.10/P3.11 live Numogram singleton.
 */
class P312AssayBridge(private val context: Context) {

    private fun module() = run {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        Python.getInstance().getModule("P312AssayCore")
    }

    fun runAssay(
        promptOne: String,
        promptTwo: String,
        seed: Int = 3606,
        dimension: Int = 3
    ): String {
        return module()
            .callAttr(
                "run_assay",
                promptOne,
                promptTwo,
                seed,
                dimension
            )
            .toString()
    }

    fun branchStatus(condition: String): String {
        return module()
            .callAttr("get_branch_status", condition)
            .toString()
    }
}
