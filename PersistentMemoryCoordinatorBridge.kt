package com.antonio.my.ai.girlfriend.free.bridge

import android.content.Context
import android.util.Log
import com.antonio.my.ai.girlfriend.free.PythonBridge
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject

/**
 * PersistentMemoryCoordinatorBridge
 * ---------------------------------
 * Provides a Kotlin interface for interacting with the Python-based
 * PersistentMemoryCoordinator (PMC).
 *
 * Handles unified persistence across:
 *  - MultiZoneMemory (zone/numogram memory)
 *  - SymbolicMemoryEvolutionModule (symbolic evolution)
 */
class PersistentMemoryCoordinatorBridge private constructor(context: Context) {

    private val bridge: PythonBridge = PythonBridge.getInstance(context)

    companion object {
        @Volatile
        private var INSTANCE: PersistentMemoryCoordinatorBridge? = null

        fun getInstance(context: Context): PersistentMemoryCoordinatorBridge {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: PersistentMemoryCoordinatorBridge(context.applicationContext).also {
                    INSTANCE = it
                }
            }
        }
    }

    private val moduleName = "persistent_memory_coordinator"

    // -------------------------------------------------------------------------
    // Core Unified Operations
    // -------------------------------------------------------------------------

    suspend fun heartbeatSync(): String = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "heartbeat_sync")
            result?.toString() ?: "No response"
        } catch (e: Exception) {
            Log.e("PMCBridge", "heartbeatSync error", e)
            "Error: ${e.message}"
        }
    }

    suspend fun updateZoneMemory(userId: String, info: String): String = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "update_zone_memory", userId, info)
            result?.toString() ?: "No result"
        } catch (e: Exception) {
            Log.e("PMCBridge", "updateZoneMemory error", e)
            "Error: ${e.message}"
        }
    }

    suspend fun recordSymbolicExperience(
        symbols: List<String>,
        context: String,
        intensity: Float = 1.0f
    ): String = withContext(Dispatchers.IO) {
        try {
            val symbolsJson = JSONObject(mapOf("symbols" to symbols)).toString()
            val result = bridge.executeFunction(
                moduleName,
                "record_symbolic_experience",
                symbolsJson,
                context,
                intensity
            )
            result?.toString() ?: "No result"
        } catch (e: Exception) {
            Log.e("PMCBridge", "recordSymbolicExperience error", e)
            "Error: ${e.message}"
        }
    }

    suspend fun syncZoneToSymbolic(userId: String): String = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "sync_zone_to_symbolic", userId)
            result?.toString() ?: "No result"
        } catch (e: Exception) {
            Log.e("PMCBridge", "syncZoneToSymbolic error", e)
            "Error: ${e.message}"
        }
    }

    // -------------------------------------------------------------------------
    // Retrieval / Export
    // -------------------------------------------------------------------------

    suspend fun retrieveUserZoneMemory(userId: String, zone: Int? = null): JSONObject? =
        withContext(Dispatchers.IO) {
            try {
                val result = if (zone != null) {
                    bridge.executeFunction(moduleName, "retrieve_user_zone_memory", userId, zone)
                } else {
                    bridge.executeFunction(moduleName, "retrieve_user_zone_memory", userId)
                }
                result?.toString()?.let { JSONObject(it) }
            } catch (e: Exception) {
                Log.e("PMCBridge", "retrieveUserZoneMemory error", e)
                null
            }
        }

    suspend fun generateAutobiography(
        timeframe: String = "all",
        detail: String = "medium"
    ): JSONObject? = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "generate_autobiography", timeframe, detail)
            result?.toString()?.let { JSONObject(it) }
        } catch (e: Exception) {
            Log.e("PMCBridge", "generateAutobiography error", e)
            null
        }
    }

    suspend fun exportState(): JSONObject? = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "export_state")
            result?.toString()?.let { JSONObject(it) }
        } catch (e: Exception) {
            Log.e("PMCBridge", "exportState error", e)
            null
        }
    }

    suspend fun getUnifiedStateJson(): String = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "to_json")
            result?.toString() ?: "{}"
        } catch (e: Exception) {
            Log.e("PMCBridge", "getUnifiedStateJson error", e)
            "{}"
        }
    }

    // -------------------------------------------------------------------------
    // Utility / Lifecycle
    // -------------------------------------------------------------------------

    suspend fun cleanup(): String = withContext(Dispatchers.IO) {
        try {
            val result = bridge.executeFunction(moduleName, "cleanup")
            result?.toString() ?: "Cleanup complete"
        } catch (e: Exception) {
            Log.e("PMCBridge", "cleanup error", e)
            "Error: ${e.message}"
        }
    }
}
