--- P310MainActivity.kt
+++ P310MainActivity_FIXED.kt
@@ -220,8 +220,14 @@
 
         val origin = currentZone
         val context = EventModulePlanner.numogramContext(userText)
-        val transition = JSONObject(bridge.transition(origin, context.toString()))
-        currentZone = transition.optInt("to", origin)
+
+        // Numogram.py returns a transport envelope:
+        // {"status":"transitioned","event":{...},"system":{...}}
+        // P3.10.0 incorrectly treated that outer envelope as the event itself.
+        val transitionEnvelope =
+            JSONObject(bridge.transition(origin, context.toString()))
+        val transition = requireTransitionEvent(transitionEnvelope)
+        currentZone = transition.getInt("to")
         val postTransition = JSONObject(bridge.status())
 
         val stagedModules = PythonModuleVault.list(applicationContext)
@@ -244,6 +250,7 @@
             .put("initialization", initialization)
             .put("before", before)
             .put("input_field", context)
+            .put("transition_envelope", transitionEnvelope)
             .put("transition", transition)
             .put("post_transition", postTransition)
             .put("event_plan", plan.toJson())
@@ -304,9 +311,9 @@
             result.put(
                 "status",
                 when {
+                    sealed.responseClass.name != "SUCCESS_TEXT" -> "terminal_response"
                     !noFeedbackHeld -> "feedback_violation"
-                    sealed.responseClass.name == "SUCCESS_TEXT" -> "success"
-                    else -> "terminal_response"
+                    else -> "success"
                 }
             )
         }
@@ -369,9 +376,21 @@
                         "P3.10 FAIL-CLOSED: post-render Numogram state differs from the sealed post-transition state."
                 }
 
-                "terminal_response", "transport_failed" -> {
+                "terminal_response" -> {
+                    val responseClass =
+                        result.optString("response_class", "UNKNOWN")
+                    val httpStatus =
+                        result.optInt("http_status", -1)
+
                     statusView.text =
-                        "The event completed, but the one-call language relay did not return display text."
+                        "Numogram event completed. Language relay returned " +
+                            "$responseClass (HTTP $httpStatus)."
+                }
+
+                "transport_failed" -> {
+                    statusView.text =
+                        "Numogram event completed. Language relay transport failed " +
+                            "before a terminal provider response was received."
                 }
 
                 else -> {
@@ -401,9 +420,53 @@
         }
     }
 
-    private fun sameEvolutionState(a: JSONObject, b: JSONObject): Boolean =
-        a.optInt("evolution_step", -1) == b.optInt("evolution_step", -2) &&
-            a.optInt("transition_history", -1) == b.optInt("transition_history", -2)
+    private fun requireTransitionEvent(envelope: JSONObject): JSONObject {
+        val status = envelope.optString("status", "")
+        if (status != "transitioned") {
+            val errorType =
+                envelope.optString("error_type", "NumogramTransitionError")
+            val message =
+                envelope.optString("message", "Numogram transition did not complete.")
+            throw IllegalStateException("$errorType: $message")
+        }
+
+        return envelope.optJSONObject("event")
+            ?: throw IllegalStateException(
+                "Numogram transition envelope is missing its event object."
+            )
+    }
+
+    /**
+     * Numogram.py get_status() returns:
+     * {"status":"ready","init_digest":"...","system":{...}}
+     *
+     * Compare the actual nested substrate state. P3.10.0 mistakenly looked
+     * for these values on the outer envelope, which made this check fail on
+     * every successful request.
+     */
+    private fun sameEvolutionState(
+        beforeRender: JSONObject,
+        afterRender: JSONObject
+    ): Boolean {
+        val beforeSystem =
+            beforeRender.optJSONObject("system") ?: return false
+        val afterSystem =
+            afterRender.optJSONObject("system") ?: return false
+
+        val integerKeys = listOf(
+            "seed",
+            "dimension",
+            "evolution_step",
+            "transition_history"
+        )
+
+        return integerKeys.all { key ->
+            beforeSystem.has(key) &&
+                afterSystem.has(key) &&
+                beforeSystem.optLong(key, Long.MIN_VALUE) ==
+                    afterSystem.optLong(key, Long.MAX_VALUE)
+        }
+    }
 
     private fun pickPythonModule() {
         val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
