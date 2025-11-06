package.com.antonio.my.ai.girlfriend.free.amelia.introspection.bridge

import android.content.Context
import android.util.Log
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

/**
 * IntrospectionBridge
 * ─────────────────────────────────────────────────────────────────────────────
 * Kotlin/Chaquopy bridge to meta_introspection_index.py.
 *
 * Responsibilities:
 *  - Ensure Python is started
 *  - Add app-local python module path (e.g., files/python_modules) if present
 *  - Provide typed wrappers for indexing, querying, runtime registry, diagnostics
 *
 * All calls return JSONObject/JSONArray for easy Android-side consumption.
 */
class IntrospectionBridge(private val context: Context) {

    companion object {
        private const val TAG = "IntrospectionBridge"
        private const val PY_MOD = "meta_introspection_index"
    }

    private fun ensurePython(): Python {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context))
        }
        return Python.getInstance()
    }

    /** Optionally add a local Python modules directory into sys.path */
    private fun addLocalPythonPath(py: Python) {
        try {
            val modulesDir = File(context.filesDir, "python_modules").absolutePath
            py.getModule("sys").get("path").callAttr("insert", 0, modulesDir)
        } catch (e: Exception) {
            Log.w(TAG, "Could not add local python path: ${e.message}")
        }
    }

    /** Load our Python module object */
    private fun mod(): com.chaquo.python.PyObject {
        val py = ensurePython()
        addLocalPythonPath(py)
        return py.getModule(PY_MOD)
    }

    private fun callJson(method: String, vararg args: Any?): JSONObject {
        return try {
            val resultStr = mod().callAttr("call", method, *args).toString()
            JSONObject(resultStr)
        } catch (e: Exception) {
            Log.e(TAG, "callJson error on $method: ${e.message}", e)
            JSONObject().put("ok", false).put("error", e.message ?: "unknown")
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Public API
    // ─────────────────────────────────────────────────────────────────────────

    /** Initialize the Python indexer. You can pass custom module paths and eager modules. */
    fun initialize(paths: List<String> = emptyList(), modules: List<String> = emptyList()): JSONObject {
        val cfg = JSONObject().apply {
            put("paths", JSONArray(paths))
            put("modules", JSONArray(modules))
        }
        return callJson("initialize", cfg.toString())
    }

    /** Build (or rebuild) index. If modules/paths omitted, it indexes already-imported ones. */
    fun buildIndex(modules: List<String>? = null, paths: List<String>? = null): JSONObject {
        val args = mutableListOf<Any?>()
        if (modules != null) args.add(JSONArray(modules).toString()) else args.add(null)
        if (paths != null) args.add(JSONArray(paths).toString()) else args.add(null)
        // The Python `call` expects native args, so we pass strings for JSON and handle None inside Python.
        return callJson("build_index", modules?.let { JSONArray(it).toList() } ?: emptyList<String>(),
            paths?.let { JSONArray(it).toList() } ?: emptyList<String>())
    }

    /** Force a refresh using previously-seen imports */
    fun refresh(): JSONObject = callJson("refresh")

    /** Query by (partial) name. */
    fun queryByName(name: String): JSONObject = callJson("query_by_name", name)

    /** Heuristic concept-based query. */
    fun queryByConcept(concept: String): JSONObject = callJson("query_by_concept", concept)

    /** Full-text style search across names/docs. */
    fun search(text: String, limit: Int = 50): JSONObject = callJson("search", text, limit)

    /** Overall stats, including counts and modules with errors. */
    fun stats(): JSONObject = callJson("stats")

    /** Register an opaque state object in the Python runtime registry. */
    fun registerRuntime(name: String, state: JSONObject): JSONObject =
        callJson("register_runtime", name, state.toString())

    /** Retrieve a runtime object’s last state. */
    fun getRuntime(name: String): JSONObject = callJson("get_runtime", name)

    /** List registered runtime object names. */
    fun listRuntime(): JSONObject = callJson("list_runtime")

    /** High-level diagnostics: uptime, sample class/function entries. */
    fun diagnostics(): JSONObject = callJson("diagnostics")
}

/**
 * Small helpers to turn JSONArray -> Kotlin List in a null-safe way
 * (used above to keep signatures flexible).
 */
private fun JSONArray.toList(): List<String> {
    val out = ArrayList<String>(length())
    for (i in 0 until length()) {
        val v = optString(i, null)
        if (v != null) out.add(v)
    }
    return out
}
