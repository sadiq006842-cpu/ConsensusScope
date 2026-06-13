# Validators

ConsensusScope uses specialized AI validators with distinct personalities, risk tolerances, weights, and memory.

## Personas

- Sentinel Security Validator — exploit vectors, adversarial inputs, access control, and smart contract safety.
- Civic Governance Validator — decentralization, voting fairness, quorum quality, and minority protections.
- Atlas Economic Validator — tokenomics, treasury sustainability, emissions, incentives, and long-term viability.
- Forge Technical Validator — scalability, infrastructure, reliability, observability, and integration risk.

## Memory

Each validator tracks:

- evaluations
- approvals and rejections
- high-risk flags
- last decision
- last risk level
- observed proposal types

Memory is used to provide context and is persisted in `validator_memory` for governance intelligence continuity.

## Disagreement

Validators are designed to disagree when their domain incentives diverge. Security may reject exploit-prone proposals that governance approves, or economics may reject a popular proposal that threatens sustainability.

