package com.amelia.bridge

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * P3.6's narrow Kotlin-to-Python boundary for the tensor Numogram. P3.5A
 * compiled this class without instantiating it; P3.6 activated the
 * Torch-runtime report and initialize -> status -> transition lifecycle.
 * P3.7 adds the sealed, non-mutating fork: runFork() seals the live
 * (transition_tensor, zone_magnetism) pair and runs FULL / ABLATED_TRANSITION
 * / ABLATED_MAGNETISM / ABLATED_BOTH / NEUTRAL_RESET against it without
 * touching the live system; verifyLastFork() independently re-derives that
 * same capsule's branches and confirms they still match.
 */
class NumogramBridge(private val context: Context) {
    private fun module() = run {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        Python.getInstance().getModule("Numogram")
    }

    fun runtimeInfo(): String {
        return module().callAttr("get_runtime_info").toString()
    }

    fun initialize(seed: Int = 0, dimension: Int = 3): String {
        return module().callAttr("initialize_system", seed, dimension).toString()
    }

    fun status(): String {
        return module().callAttr("get_status").toString()
    }

    fun transition(currentZone: Int, contextJson: String = "{}"): String {
        return module().callAttr("transition", currentZone, contextJson).toString()
    }

    fun runFork(currentZone: Int, contextJson: String = "{}"): String {
        return module().callAttr("run_fork", currentZone, contextJson).toString()
    }

    fun verifyLastFork(): String {
        return module().callAttr("verify_last_fork").toString()
    }
}
