# Governance Engine

The Optimistic Democracy Engine evaluates proposals through multiple intelligence layers.

## Flow

1. Detect proposal type from governance, security, economic, and technical signals.
2. Run dynamic risk analysis for category risks, mitigations, complexity, and prompt injection.
3. Ask each validator persona for an independent decision.
4. Compute weighted consensus from validator weight and confidence.
5. Detect disagreement, dissenting validators, and challenge-period requirements.
6. Persist proposal history, decisions, events, memory, and analytics.

## Weighted Consensus

Each validator contributes:

```text
vote_power = validator_weight * confidence_percent
```

The final majority decision follows the larger weighted side, not only the raw vote count.

## Risk Intelligence

The engine flags:

- prompt injection attempts
- governance capture
- low quorum or unfair voting design
- exploit and access-control concerns
- treasury drain and unsustainable tokenomics
- infrastructure fragility and rollback gaps

## Challenge Periods

Challenge periods are generated when disagreement or high-risk findings appear. This models Optimistic Democracy review windows before final execution.

