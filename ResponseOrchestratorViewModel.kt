package.antonio.my.ai.girlfriend.free.amelia.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import org.json.JSONObject
import your.package.name.bridges.ResponseOrchestratorBridge

/**
 * ResponseOrchestratorViewModel
 * -----------------------------
 *
 * The ViewModel that handles:
 *  - receiving user input
 *  - sending it to ResponseOrchestratorBridge
 *  - updating UI state with messages
 *  - tracking loading / errors
 *
 * This becomes the main ViewModel for Amelia’s dialogue UI.
 */

class ResponseOrchestratorViewModel : ViewModel() {

    // ------------------------------
    // Message model for UI rendering
    // ------------------------------
    sealed class ChatMessage {
        data class User(val text: String) : ChatMessage()
        data class Amelia(val text: String) : ChatMessage()
    }

    // ------------------------------
    // UI State
    // ------------------------------
    data class UiState(
        val messages: List<ChatMessage> = emptyList(),
        val isLoading: Boolean = false,
        val error: String? = null
    )

    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> get() = _uiState.asStateFlow()

    // ------------------------------
    // Public function: send user message
    // ------------------------------
    fun sendMessage(userText: String) {
        if (userText.isBlank()) return

        viewModelScope.launch {
            try {
                // 1. Add user message
                appendMessage(ChatMessage.User(userText))

                // 2. Enter loading state
                setLoading(true)

                // 3. Pass to the orchestrator
                val ameliaText = ResponseOrchestratorBridge.generateResponse(
                    userText = userText,
                    baseResponse = getRawLLMResponse(userText),
                    metadata = JSONObject().apply {
                        put("source", "android_app")
                        put("timestamp", System.currentTimeMillis())
                    }
                )

                // 4. Add Amelia message
                appendMessage(ChatMessage.Amelia(ameliaText))

            } catch (e: Exception) {
                setError("Error generating Amelia response: ${e.message}")
            } finally {
                setLoading(false)
            }
        }
    }

    // ------------------------------
    // Internal helper: placeholder LLM
    // Replace with your actual LLM call
    // ------------------------------
    private suspend fun getRawLLMResponse(userText: String): String {
        // Replace this with:
        //   llm.generate(userText)
        //
        // This placeholder is useful until your app’s LLM is wired.
        return "Acknowledged: $userText"
    }

    // ------------------------------
    // Message & UI state helpers
    // ------------------------------
    private fun appendMessage(msg: ChatMessage) {
        _uiState.update { cur ->
            cur.copy(messages = cur.messages + msg)
        }
    }

    private fun setLoading(value: Boolean) {
        _uiState.update { it.copy(isLoading = value) }
    }

    private fun setError(error: String?) {
        _uiState.update { it.copy(error = error) }
    }

    // ------------------------------
    // Optional: clear error from UI
    // ------------------------------
    fun dismissError() {
        setError(null)
    }

    // ------------------------------
    // Optional: clear chat history
    // ------------------------------
    fun clearChat() {
        _uiState.value = UiState()
    }
}
