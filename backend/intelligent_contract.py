# { "Depends": "py-genlayer:test" }
from genlayer import *


class GovernanceEvaluator(gl.Contract):
    proposals: dict
    total_evaluated: int

    def __init__(self):
        self.proposals = {}
        self.total_evaluated = 0

    @gl.public.write
    def evaluate_proposal(self, proposal_id: str, proposal_text: str):
        def assess():
            return gl.exec_prompt(
                f"""You are a GenLayer governance validator.
                Evaluate this proposal carefully:
                ---PROPOSAL START---
                {proposal_text}
                ---PROPOSAL END---
                Respond with ONLY valid JSON:
                {{
                  "decision": "APPROVE" or "REJECT",
                  "confidence": number between 0 and 100,
                  "reasoning": "one sentence explanation",
                  "risk_level": "LOW" or "MEDIUM" or "HIGH"
                }}"""
            )

        result = gl.eq_principle_non_comparative(assess)
        self.proposals[proposal_id] = result
        self.total_evaluated += 1

    @gl.public.view
    def get_proposal(self, proposal_id: str) -> str:
        return self.proposals.get(proposal_id, "")

    @gl.public.view
    def get_total_evaluated(self) -> int:
        return self.total_evaluated
