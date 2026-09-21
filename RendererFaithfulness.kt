package com.amelia.renderer

import org.json.JSONObject

/**
 * A narrow, deterministic check on the renderer boundary.
 *
 * It does not claim to solve general natural-language truthfulness. Instead,
 * it requires the renderer to copy an explicit destination claim table, then
 * compares that table and the declared ABLATED_BOTH/NEUTRAL_RESET relation to
 * the sealed fork result. A small direct-claim scan catches common prose
 * contradictions as an additional label. Unparseable text is labelled rather
 * than silently accepted, and no outcome causes another provider call.
 */
enum class FaithfulnessState {
    VERIFIED,
    CONTRADICTION_DETECTED,
    UNVERIFIABLE
}

data class BranchFact(
    val name: String,
    val from: Int,
    val to: Int,
    val fallback: Boolean
)

data class FaithfulnessVerdict(
    val state: FaithfulnessState,
    val narrative: String,
    val reasons: List<String>
) {
    fun summary(): String = when (state) {
        FaithfulnessState.VERIFIED ->
            "VERIFIED: structured destinations match the sealed branch table."
        FaithfulnessState.CONTRADICTION_DETECTED ->
            "CONTRADICTION DETECTED: renderer prose is rejected."
        FaithfulnessState.UNVERIFIABLE ->
            "UNVERIFIABLE: renderer prose is labelled, not accepted as faithful."
    }
}

object RendererFaithfulness {
    private const val RESPONSE_SCHEMA = "amelia-p3.9-render-response-v1"

    private val BRANCHES = listOf(
        "FULL",
        "ABLATED_TRANSITION",
        "ABLATED_MAGNETISM",
        "ABLATED_BOTH",
        "NEUTRAL_RESET"
    )

    fun branchFacts(forkResult: JSONObject): List<BranchFact> {
        val branches = forkResult.optJSONObject("branches") ?: return emptyList()
        return BRANCHES.mapNotNull { name ->
            val branch = branches.optJSONObject(name) ?: return@mapNotNull null
            BranchFact(
                name = name,
                from = branch.optInt("from", -1),
                to = branch.optInt("to", -1),
                fallback = branch.optBoolean("fallback", false)
            )
        }
    }

    fun branchTable(forkResult: JSONObject): String {
        val facts = branchFacts(forkResult)
        if (facts.size != BRANCHES.size) {
            return "Branch table unavailable: sealed result is incomplete."
        }
        return buildString {
            append("Sealed branch table (authoritative):\n")
            facts.forEach { fact ->
                append(fact.name)
                append(": Z")
                append(fact.from)
                append(" → Z")
                append(fact.to)
                if (fact.fallback) append(" (fallback)")
                append('\n')
            }
            append("ABLATED_BOTH / NEUTRAL_RESET relation: ")
            append(expectedRelation(forkResult, facts))
        }
    }

    fun verify(forkResult: JSONObject, rendererText: String): FaithfulnessVerdict {
        val facts = branchFacts(forkResult)
        if (facts.size != BRANCHES.size) {
            return FaithfulnessVerdict(
                FaithfulnessState.UNVERIFIABLE,
                rendererText,
                listOf("The sealed fork result did not contain all required branches.")
            )
        }

        val response = try {
            JSONObject(rendererText)
        } catch (_: Exception) {
            return FaithfulnessVerdict(
                FaithfulnessState.UNVERIFIABLE,
                rendererText,
                listOf("Renderer response was not the required P3.9 JSON envelope.")
            )
        }

        if (response.optString("schema", "") != RESPONSE_SCHEMA) {
            return FaithfulnessVerdict(
                FaithfulnessState.UNVERIFIABLE,
                response.optString("narrative", rendererText),
                listOf("Renderer response used an unexpected schema.")
            )
        }

        val narrative = response.optString("narrative", "").trim()
        if (narrative.isBlank()) {
            return FaithfulnessVerdict(
                FaithfulnessState.UNVERIFIABLE,
                "",
                listOf("Renderer response had no narrative field.")
            )
        }

        val claims = response.optJSONObject("branch_destinations")
            ?: return FaithfulnessVerdict(
                FaithfulnessState.UNVERIFIABLE,
                narrative,
                listOf("Renderer response omitted branch_destinations.")
            )

        val contradictions = mutableListOf<String>()
        val incomplete = mutableListOf<String>()
        facts.forEach { fact ->
            if (!claims.has(fact.name)) {
                incomplete += "Missing destination claim for ${fact.name}."
            } else {
                val claimed = claims.optInt(fact.name, -1)
                if (claimed !in 0..9) {
                    contradictions += "${fact.name} claimed an invalid destination: $claimed."
                } else if (claimed != fact.to) {
                    contradictions +=
                        "${fact.name} claimed Z$claimed; sealed table records Z${fact.to}."
                }
            }
        }

        val expectedRelation = expectedRelation(forkResult, facts)
        if (!response.has("ablated_both_neutral_reset_relation")) {
            incomplete += "Renderer response omitted the ABLATED_BOTH/NEUTRAL_RESET relation."
        } else {
            val claimedRelation =
                response.optString("ablated_both_neutral_reset_relation", "")
            if (claimedRelation != expectedRelation) {
                contradictions +=
                    "ABLATED_BOTH/NEUTRAL_RESET relation was '$claimedRelation'; " +
                        "sealed relation is '$expectedRelation'."
            }
        }

        contradictions += scanDirectNarrativeClaims(facts, narrative)

        return when {
            contradictions.isNotEmpty() -> FaithfulnessVerdict(
                FaithfulnessState.CONTRADICTION_DETECTED,
                narrative,
                contradictions.distinct()
            )
            incomplete.isNotEmpty() -> FaithfulnessVerdict(
                FaithfulnessState.UNVERIFIABLE,
                narrative,
                incomplete
            )
            else -> FaithfulnessVerdict(
                FaithfulnessState.VERIFIED,
                narrative,
                listOf("All sealed branch destinations and the relation token matched.")
            )
        }
    }

    private fun expectedRelation(
        forkResult: JSONObject,
        facts: List<BranchFact>
    ): String {
        val invariant = forkResult.optJSONObject("invariants")
            ?.optBoolean("ablated_both_matches_neutral_reset", false)
            ?: false
        if (!invariant) return "no_probability_distribution_equality_claim"

        val ablatedBoth = facts.firstOrNull { it.name == "ABLATED_BOTH" }
        val neutralReset = facts.firstOrNull { it.name == "NEUTRAL_RESET" }
        return if (ablatedBoth != null && neutralReset != null && ablatedBoth.to == neutralReset.to) {
            "same_probability_distribution_and_same_sampled_destination"
        } else {
            "same_probability_distribution_only"
        }
    }

    private fun scanDirectNarrativeClaims(
        facts: List<BranchFact>,
        narrative: String
    ): List<String> {
        val contradictions = mutableListOf<String>()
        val aliases = mapOf(
            "FULL" to "(?:FULL|full(?:\\s+(?:branch|condition))?)",
            "ABLATED_TRANSITION" to "(?:ABLATED_TRANSITION|ablated[\\s_-]+transition)",
            "ABLATED_MAGNETISM" to "(?:ABLATED_MAGNETISM|ablated[\\s_-]+magnetism)",
            "ABLATED_BOTH" to "(?:ABLATED_BOTH|ablated[\\s_-]+both|both[\\s_-]+factors)",
            "NEUTRAL_RESET" to "(?:NEUTRAL_RESET|neutral[\\s_-]+reset)"
        )

        facts.forEach { fact ->
            val alias = aliases[fact.name] ?: return@forEach
            val pattern = Regex(
                "(?is)$alias[\\s\\S]{0,160}?" +
                    "(?:landed|moved|went|reached|ended|arrived)\\s+" +
                    "(?:on|in|at|to)\\s+(?:zone\\s*)?z?([0-9])\\b"
            )
            pattern.findAll(narrative).forEach { match ->
                val claimed = match.groupValues[1].toIntOrNull()
                if (claimed != null && claimed != fact.to) {
                    contradictions +=
                        "Narrative states ${fact.name} reached Z$claimed; " +
                            "sealed table records Z${fact.to}."
                }
            }
        }

        val ablatedBoth = facts.firstOrNull { it.name == "ABLATED_BOTH" }
        val neutralReset = facts.firstOrNull { it.name == "NEUTRAL_RESET" }
        if (ablatedBoth != null && neutralReset != null && ablatedBoth.to != neutralReset.to) {
            val saysSameDestination = Regex(
                "(?is)(?:same|matching|identical|equal)\\s+" +
                    "(?:destination|zone|outcome|landing)"
            ).containsMatchIn(narrative)
            val namesBothPresent = Regex(
                "(?is)(?:ABLATED_BOTH|ablated[\\s_-]+both|both[\\s_-]+factors)"
            ).containsMatchIn(narrative) && Regex(
                "(?is)(?:NEUTRAL_RESET|neutral[\\s_-]+reset)"
            ).containsMatchIn(narrative)
            if (saysSameDestination && namesBothPresent) {
                contradictions +=
                    "Narrative asserts a shared destination for ABLATED_BOTH and " +
                        "NEUTRAL_RESET, but the sealed destinations differ."
            }
        }
        return contradictions
    }
}
