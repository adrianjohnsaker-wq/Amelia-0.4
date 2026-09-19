package com.amelia.bridge

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * Deferred P3.6 bridge for the tensor Numogram. P3.5A compiles this class but
 * deliberately does not instantiate it or import Numogram.py.
 */
class NumogramBridge(private val context: Context) {
    private fun module() = run {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        Python.getInstance().getModule("Numogram")
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
