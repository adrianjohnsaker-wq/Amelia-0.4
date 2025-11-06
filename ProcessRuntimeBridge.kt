package com.antonio.my.ai.girlfriend.free.amelia.bridge

import com.chaquo.python.Python
import org.json.JSONObject

object ProcessRuntimeBridge {

    private val py = Python.getInstance()
    private val mod = py.getModule("process_metaphysics_runtime")

    fun evolveCycle(zone: String? = null): JSONObject {
        val result = mod.callAttr("evolve_cycle", zone ?: JSONObject.NULL).toString()
        return JSONObject(result)
    }

    fun getState(): JSONObject {
        val result = mod.callAttr("get_state").toString()
        return JSONObject(result)
    }

    fun planeOfConsistency(): JSONObject {
        val result = mod.callAttr("plane_of_consistency").toString()
        return JSONObject(result)
    }
}
