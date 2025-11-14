package com.antonio.my.ai.girlfriend.free.amelia.bridges

object ResponseOrchestratorReturnChannel {

    @Volatile
    private var callback: ((String) -> Unit)? = null

    fun register(cb: (String) -> Unit) {
        callback = cb
    }

    fun deliver(text: String) {
        callback?.invoke(text)
    }
}
