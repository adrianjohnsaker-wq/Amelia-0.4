package com.antonio.my.ai.girlfriend.free.amelia.python

import com.chaquo.python.PyObject
import com.chaquo.python.Python

/**
 * PythonModuleController
 * ---------------------------------------------------------
 * Thin wrapper around Chaquopy's Python runtime.
 *
 * Responsibilities:
 *  - Load a Python module by name.
 *  - Call a function in that module with an optional single argument.
 *  - Always return a String (typically JSON from Python).
 *  - Never throw out of this boundary: errors are converted to JSON.
 *
 * Used by:
 *   - ResponseOrchestratorBridge
 *   - Any other Amelia bridges that need to call Python.
 */
object PythonModuleController {

    /**
     * Run a Python function with a single String argument.
     *
     * @param module   Python module name (without .py)
     * @param function Python function name inside that module
     * @param argument Nullable String argument (often JSON)
     *
     * @return The function's return value as String, or a JSON error object.
     */
    @JvmStatic
    @Synchronized
    fun runFunction(
        module: String,
        function: String,
        argument: String? = null
    ): String {
        return try {
            val py = Python.getInstance()
            val pyModule: PyObject = py.getModule(module)

            val result: PyObject = if (argument != null) {
                pyModule.callAttr(function, argument)
            } else {
                pyModule.callAttr(function)
            }

            // Ensure we always surface a String
            result.toString()
        } catch (e: Exception) {
            // Surface a JSON error, so callers (like ResponseOrchestratorBridge)
            // can treat this uniformly.
            """
            {
              "status": "error",
              "message": "PythonModuleController failure: ${e.message ?: "unknown error"}",
              "module": "$module",
              "function": "$function"
            }
            """.trimIndent()
        }
    }
}
