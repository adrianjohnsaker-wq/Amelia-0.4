package com.amelia.bridge

// TEMPORARY, P3.5A ONLY. Calls bridge_probe.py, nothing else -- no numpy,
// no torch, no Numogram.py. Its only job is to prove Kotlin -> Chaquopy ->
// Python -> Kotlin round-trips on the actual GitHub Actions -> APK ->
// device path before anything heavier is added. Safe to delete once P3.6
// (torch-backed Numogram.py) is confirmed working, or to leave in place as
// a standing diagnostic -- it costs nothing at runtime unless called.

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

object ChaquopyProbe {

    fun run(context: Context): String {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        val python = Python.getInstance()
        val module = python.getModule("bridge_probe")
        return module.callAttr(
            "ping",
            """{"stage":"P3.5A","source":"android"}"""
        ).toString()
    }
}
