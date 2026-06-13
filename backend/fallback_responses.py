from __future__ import annotations

from collections import defaultdict
from itertools import count
from typing import Any


def _entry(decision: str, confidence: int, risk_level: str, reasoning: str) -> dict[str, Any]:
    return {
        "decision": decision,
        "confidence": confidence,
        "risk_level": risk_level,
        "reasoning": reasoning,
    }


VALIDATOR_FALLBACKS: dict[str, dict[str, list[dict[str, Any]]]] = {
    "GPT-4 Security Validator": {
        "governance": [
            _entry("APPROVE", 82, "LOW", "Governance controls are clear enough to proceed if execution remains transparent and reversible."),
            _entry("APPROVE", 78, "MEDIUM", "The proposal is acceptable, but admin permissions should be documented before activation."),
            _entry("REJECT", 69, "MEDIUM", "The governance path lacks a clear rollback mechanism for unsafe execution outcomes."),
            _entry("APPROVE", 86, "LOW", "Validator accountability and voting thresholds appear sufficient for a controlled rollout."),
            _entry("REJECT", 73, "HIGH", "The proposal gives governance broad authority without enough operational safeguards."),
        ],
        "security": [
            _entry("REJECT", 88, "HIGH", "Security-critical changes should not proceed without audit evidence and explicit failure handling."),
            _entry("APPROVE", 81, "MEDIUM", "The risk is manageable if the contract is deployed behind staged limits and monitoring."),
            _entry("REJECT", 84, "HIGH", "The proposal does not sufficiently explain how exploit prevention will be enforced."),
            _entry("APPROVE", 79, "MEDIUM", "Controls are reasonable for testnet, provided privileged actions remain observable."),
            _entry("REJECT", 90, "HIGH", "The plan introduces attack surface without a matching incident response process."),
        ],
        "economic": [
            _entry("APPROVE", 77, "MEDIUM", "Economic risk is acceptable if treasury exposure is capped during the first phase."),
            _entry("REJECT", 74, "MEDIUM", "The proposal does not quantify downside scenarios for validators or users."),
            _entry("APPROVE", 83, "LOW", "The incentive design is conservative and should not destabilize validator behavior."),
            _entry("REJECT", 80, "HIGH", "Treasury allocation rules are too vague to approve without stricter limits."),
            _entry("APPROVE", 76, "MEDIUM", "The economics are viable for testnet if rewards are reviewed after live usage data."),
        ],
        "technical": [
            _entry("APPROVE", 84, "LOW", "The implementation path is technically sound for a staged GenLayer governance release."),
            _entry("REJECT", 72, "MEDIUM", "The proposal needs clearer operational metrics before production-style adoption."),
            _entry("APPROVE", 79, "MEDIUM", "The technical approach is acceptable if observability and rollback hooks are included."),
            _entry("REJECT", 82, "HIGH", "The system design lacks enough detail about degraded validator or model responses."),
            _entry("APPROVE", 87, "LOW", "The architecture is simple, testable, and appropriate for an ecosystem demonstration."),
        ],
    },
    "Claude Governance Validator": {
        "governance": [
            _entry("APPROVE", 88, "LOW", "The proposal aligns with transparent governance and preserves validator agency."),
            _entry("APPROVE", 83, "LOW", "The decision process is understandable and gives participants enough context to consent."),
            _entry("REJECT", 71, "MEDIUM", "The governance rationale is incomplete and could create ambiguity for future voters."),
            _entry("APPROVE", 80, "MEDIUM", "The proposal is directionally useful, though it should define success criteria more tightly."),
            _entry("REJECT", 76, "HIGH", "The plan concentrates decision power without sufficient checks from independent validators."),
        ],
        "security": [
            _entry("APPROVE", 75, "MEDIUM", "The proposal can proceed if security assumptions are disclosed to voters before execution."),
            _entry("REJECT", 79, "HIGH", "Governance should not approve security changes without a clear audit and disclosure trail."),
            _entry("APPROVE", 82, "LOW", "The security posture appears compatible with a cautious testnet governance process."),
            _entry("REJECT", 73, "MEDIUM", "The proposal does not adequately explain who is accountable if controls fail."),
            _entry("APPROVE", 78, "MEDIUM", "Approval is reasonable if emergency procedures are documented and visible to the community."),
        ],
        "economic": [
            _entry("APPROVE", 81, "LOW", "The economic changes are modest and should support long-term ecosystem participation."),
            _entry("REJECT", 70, "MEDIUM", "The distribution impact is unclear and could reduce perceived fairness among validators."),
            _entry("APPROVE", 84, "LOW", "Incentives appear balanced and avoid excessive extraction from the network."),
            _entry("REJECT", 77, "HIGH", "The treasury logic needs stronger public constraints before governance approval."),
            _entry("APPROVE", 79, "MEDIUM", "The proposal is acceptable if economic outcomes are reviewed through transparent milestones."),
        ],
        "technical": [
            _entry("APPROVE", 82, "LOW", "The technical plan is understandable and gives governance enough visibility into outcomes."),
            _entry("REJECT", 74, "MEDIUM", "The implementation lacks a clear explanation for non-technical ecosystem participants."),
            _entry("APPROVE", 80, "MEDIUM", "The rollout is acceptable if validator feedback is collected after deployment."),
            _entry("REJECT", 78, "HIGH", "The design creates governance risk because failure states are not described clearly."),
            _entry("APPROVE", 85, "LOW", "The proposal supports ecosystem learning while keeping operational complexity contained."),
        ],
    },
    "Gemini Economic Validator": {
        "governance": [
            _entry("APPROVE", 79, "MEDIUM", "Governance overhead is justified if the proposal improves measurable network utility."),
            _entry("REJECT", 72, "MEDIUM", "The proposal needs a clearer cost-benefit model before validators commit support."),
            _entry("APPROVE", 84, "LOW", "The governance process should create positive ecosystem value without large capital risk."),
            _entry("REJECT", 75, "HIGH", "Decision rights and economic accountability are not aligned strongly enough."),
            _entry("APPROVE", 81, "LOW", "The plan is economically sensible because it keeps scope limited and outcomes measurable."),
        ],
        "security": [
            _entry("REJECT", 76, "HIGH", "A security incident could create economic loss that is not priced into the proposal."),
            _entry("APPROVE", 74, "MEDIUM", "The proposal is acceptable if exposure is capped while security confidence increases."),
            _entry("REJECT", 82, "HIGH", "The expected value is negative without stronger exploit mitigation and monitoring."),
            _entry("APPROVE", 78, "MEDIUM", "Limited testnet deployment keeps economic downside manageable while evidence is gathered."),
            _entry("REJECT", 80, "HIGH", "The plan shifts too much risk to users without defining compensation or recovery paths."),
        ],
        "economic": [
            _entry("APPROVE", 87, "LOW", "The incentive structure is balanced and likely to improve sustainable validator participation."),
            _entry("REJECT", 73, "MEDIUM", "The reward assumptions are under-specified and could distort validator behavior."),
            _entry("APPROVE", 82, "LOW", "Treasury impact appears controlled and proportionate to the expected ecosystem benefit."),
            _entry("REJECT", 79, "HIGH", "The proposal creates concentrated economic upside without adequate downside protection."),
            _entry("APPROVE", 85, "LOW", "The economic model is conservative enough for a GenLayer governance milestone."),
        ],
        "technical": [
            _entry("APPROVE", 77, "MEDIUM", "The technical plan is viable if implementation costs stay within the proposed milestone scope."),
            _entry("REJECT", 71, "MEDIUM", "The proposal lacks enough detail to estimate infrastructure and maintenance costs."),
            _entry("APPROVE", 80, "LOW", "The design should scale economically because it avoids unnecessary persistent computation."),
            _entry("REJECT", 76, "HIGH", "Operational complexity may create hidden costs that outweigh the expected benefits."),
            _entry("APPROVE", 83, "LOW", "The implementation is lean and should provide useful network insight at low cost."),
        ],
    },
    "Mistral Technical Validator": {
        "governance": [
            _entry("APPROVE", 80, "LOW", "The governance workflow is simple enough to implement and verify consistently."),
            _entry("REJECT", 73, "MEDIUM", "The proposal needs clearer state transitions before validators can reproduce outcomes."),
            _entry("APPROVE", 84, "LOW", "The process is technically auditable and compatible with deterministic reporting."),
            _entry("REJECT", 77, "HIGH", "The governance logic leaves too much room for inconsistent validator interpretation."),
            _entry("APPROVE", 82, "LOW", "The plan can be implemented cleanly with explicit proposal identifiers and stored results."),
        ],
        "security": [
            _entry("REJECT", 86, "HIGH", "Security requirements are not precise enough to validate implementation correctness."),
            _entry("APPROVE", 78, "MEDIUM", "A constrained testnet launch is acceptable if logs and validator outputs are preserved."),
            _entry("REJECT", 81, "HIGH", "The proposal does not describe safe handling for malformed or adversarial inputs."),
            _entry("APPROVE", 76, "MEDIUM", "The design can proceed if permissions are explicit and monitored during execution."),
            _entry("REJECT", 84, "HIGH", "The technical risk is too high without validation tests for security edge cases."),
        ],
        "economic": [
            _entry("APPROVE", 75, "MEDIUM", "The economic logic is technically feasible if values are parameterized and observable."),
            _entry("REJECT", 70, "MEDIUM", "The implementation cannot be validated because economic parameters are too vague."),
            _entry("APPROVE", 79, "LOW", "The design avoids complex settlement paths and should be straightforward to test."),
            _entry("REJECT", 78, "HIGH", "The contract behavior under treasury edge cases is not specified sufficiently."),
            _entry("APPROVE", 81, "LOW", "The proposal is technically sound if economic limits are encoded as explicit constraints."),
        ],
        "technical": [
            _entry("APPROVE", 89, "LOW", "The architecture is direct, observable, and suitable for GenLayer governance validation."),
            _entry("REJECT", 74, "MEDIUM", "The plan should define latency, retry, and failure handling before approval."),
            _entry("APPROVE", 83, "LOW", "The implementation is compact and should integrate cleanly with the demo API."),
            _entry("REJECT", 79, "HIGH", "The proposal omits important details about persistence and validator result consistency."),
            _entry("APPROVE", 86, "LOW", "The technical scope is realistic and provides a useful ecosystem reference implementation."),
        ],
    },
}


PROPOSAL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "security": (
        "security",
        "audit",
        "exploit",
        "attack",
        "permission",
        "access control",
        "vulnerability",
        "safe",
        "emergency",
        "pause",
    ),
    "economic": (
        "treasury",
        "token",
        "reward",
        "fee",
        "incentive",
        "grant",
        "budget",
        "liquidity",
        "staking",
        "emission",
    ),
    "technical": (
        "api",
        "latency",
        "scale",
        "infrastructure",
        "database",
        "contract",
        "deployment",
        "upgrade",
        "performance",
        "monitoring",
    ),
    "governance": (
        "governance",
        "vote",
        "proposal",
        "validator",
        "consensus",
        "quorum",
        "delegate",
        "policy",
        "council",
        "decision",
    ),
}


_COUNTERS: defaultdict[str, Any] = defaultdict(count)


def detect_proposal_type(prompt: str) -> str:
    normalized_prompt = prompt.lower()
    scores = {
        proposal_type: sum(keyword in normalized_prompt for keyword in keywords)
        for proposal_type, keywords in PROPOSAL_KEYWORDS.items()
    }
    best_type = max(scores, key=scores.get)
    return best_type if scores[best_type] > 0 else "governance"


def get_fallback_response(
    validator_name: str,
    proposal_type: str | None = None,
) -> dict[str, Any]:
    normalized_type = proposal_type if proposal_type in PROPOSAL_KEYWORDS else "governance"
    validator_fallbacks = VALIDATOR_FALLBACKS.get(
        validator_name,
        VALIDATOR_FALLBACKS["Claude Governance Validator"],
    )
    responses = validator_fallbacks[normalized_type]
    counter_key = f"{validator_name}:{normalized_type}"
    response_index = next(_COUNTERS[counter_key]) % len(responses)
    return responses[response_index].copy()
