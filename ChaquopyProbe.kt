package com.amelia.bridge

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

/** P3.5A's only on-device Python entry point. */
object ChaquopyProbe {
    @JvmStatic
    fun run(context: Context): String {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        val payload = JSONObject()
            .put("stage", "P3.5A")
            .put("source", "android")
            .toString()
        return Python.getInstance()
            .getModule("bridge_probe")
            .callAttr("ping", payload)
            .toString()
    }
}
