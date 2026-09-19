package com.amelia.bridge

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * P3.6's narrow Kotlin-to-Python boundary for the tensor Numogram. P3.5A
 * compiled this class without instantiating it; P3.6 activates only the
 * Torch-runtime report and initialize -> status -> transition lifecycle.
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
}
