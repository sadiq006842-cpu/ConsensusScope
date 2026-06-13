from __future__ import annotations

import json
import hashlib
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

try:
    from fallback_responses import detect_proposal_type, get_fallback_response
except ModuleNotFoundError:
    from backend.fallback_responses import detect_proposal_type, get_fallback_response


load_dotenv()

logger = logging.getLogger("consensusscope.backend")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./consensus.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class ValidatorDB(Base):
    __tablename__ = "validators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    response = Column(String, nullable=False)


class ProposalDB(Base):
    __tablename__ = "proposals"

    id = Column(String, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    proposal_type = Column(String, nullable=False)
    majority_decision = Column(String, nullable=False)
    consensus_score = Column(Integer, nullable=False)
    weighted_consensus_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    has_disagreement = Column(Integer, nullable=False, default=0)
    created_at = Column(String, nullable=False)


class ValidatorDecisionDB(Base):
    __tablename__ = "validator_decisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proposal_id = Column(String, nullable=False, index=True)
    validator = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    disagreement = Column(Integer, nullable=False, default=0)
    reasoning = Column(String, nullable=False)


class GovernanceEventDB(Base):
    __tablename__ = "governance_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proposal_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    payload = Column(String, nullable=False)
    created_at = Column(String, nullable=False)


class ValidatorMemoryDB(Base):
    __tablename__ = "validator_memory"

    validator = Column(String, primary_key=True)
    evaluations = Column(Integer, nullable=False, default=0)
    approvals = Column(Integer, nullable=False, default=0)
    rejections = Column(Integer, nullable=False, default=0)
    high_risk_flags = Column(Integer, nullable=False, default=0)
    last_decision = Column(String, nullable=True)
    last_risk_level = Column(String, nullable=True)
    observed_types = Column(String, nullable=False, default="{}")


class ProposalAnalyticsDB(Base):
    __tablename__ = "proposal_analytics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proposal_id = Column(String, nullable=False, index=True)
    consensus_score = Column(Integer, nullable=False)
    weighted_consensus_score = Column(Integer, nullable=False)
    disagreement_rate = Column(Integer, nullable=False)
    risk_score = Column(Integer, nullable=False)
    attack_likelihood_score = Column(Integer, nullable=False)
    stability_score = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

app = FastAPI(
    title="ConsensusScope API",
    description="GenLayer consensus visualization and simulation backend.",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    "https://consensusscope.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Validator(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    response: str = Field(..., pattern="^(APPROVE|REJECT)$")


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)


Decision = Literal["APPROVE", "REJECT"]
RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
MajorityDecision = Literal["APPROVE", "REJECT", "TIE", "NONE"]


class RiskCategoryResponse(BaseModel):
    score: int = Field(..., ge=0, le=100)
    signals: list[str]


class RiskAnalysisResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    level: RiskLevel
    categories: dict[str, RiskCategoryResponse]
    mitigations: list[str]
    prompt_injection_signals: list[str]
    complexity_modifier: int = Field(..., ge=0)


class ValidatorSignalsResponse(BaseModel):
    specialization_hits: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    mitigations: list[str] = Field(default_factory=list)


class ValidatorMemoryContextResponse(BaseModel):
    evaluations: int = Field(..., ge=0)
    approvals: int = Field(..., ge=0)
    rejections: int = Field(..., ge=0)
    rejection_rate: float = Field(..., ge=0, le=100)
    high_risk_flags: int = Field(..., ge=0)
    last_decision: MajorityDecision | None = None
    last_risk_level: RiskLevel | None = None
    observed_types: dict[str, int]


class ValidatorResponse(BaseModel):
    validator: str
    name: str
    model: str
    specialization: str
    personality: str
    philosophy: str = ""
    governance_bias: str = ""
    aggression_level: int = Field(0, ge=0, le=100)
    decentralization_preference: int = Field(0, ge=0, le=100)
    memory_pressure: int = Field(0, ge=0, le=100)
    trust_score: int = Field(0, ge=0, le=100)
    consensus_influence: float = Field(0, ge=0)
    instability_contribution: int = Field(0, ge=0, le=100)
    recent_voting_trend: str = ""
    weight: float = Field(..., gt=0)
    response: Decision
    confidence: int = Field(..., ge=0, le=100)
    risk_score: int = Field(..., ge=0, le=100)
    reasoning: str
    reasoning_trace: list[str]
    risk_level: RiskLevel
    signals: ValidatorSignalsResponse
    memory_context: ValidatorMemoryContextResponse
    disagrees: bool = False


class DisagreementSummaryResponse(BaseModel):
    validator: str
    decision: Decision
    reason: str
    confidence: int = Field(..., ge=0, le=100)


class ConsensusResponse(BaseModel):
    proposal_id: str | None = None
    proposal: str
    proposal_type: str
    risk_analysis: RiskAnalysisResponse
    results: list[ValidatorResponse]
    consensus_score: float = Field(..., ge=0, le=100)
    weighted_consensus_score: float = Field(..., ge=0, le=100)
    weighted_approve_score: float = Field(..., ge=0)
    weighted_reject_score: float = Field(..., ge=0)
    majority_decision: MajorityDecision
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    approve_count: int = Field(..., ge=0)
    reject_count: int = Field(..., ge=0)
    avg_confidence: float = Field(..., ge=0, le=100)
    has_disagreement: bool
    disagreement_count: int = Field(..., ge=0)
    disagreement_rate: float = Field(..., ge=0, le=100)
    disagreement_summary: list[DisagreementSummaryResponse]
    optimistic_rounds: list[dict[str, Any]] = Field(default_factory=list)
    validator_negotiations: list[dict[str, Any]] = Field(default_factory=list)
    challenge_period: dict[str, Any] = Field(default_factory=dict)
    attack_simulation: dict[str, Any] = Field(default_factory=dict)
    anomaly_detection: dict[str, Any] = Field(default_factory=dict)
    final_verdict: str


class PromptAnalysisResponse(BaseModel):
    prompt: str
    is_suspicious: bool
    detected_patterns: list[str]
    risk_score: float = Field(..., ge=0, le=100)
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    dynamic_risk_analysis: RiskAnalysisResponse
    recommendation: str


class ValidatorRecordResponse(BaseModel):
    id: int
    name: str
    response: Decision
    confidence: int = Field(..., ge=0, le=100)
    reputation_score: int = Field(..., ge=0, le=100)
    reputation_level: Literal["ELITE", "TRUSTED", "WATCH"]
    disagrees: bool = False


class ValidatorsListResponse(BaseModel):
    validators: list[ValidatorRecordResponse]
    consensus_score: float = Field(..., ge=0, le=100)
    weighted_consensus_score: float = Field(..., ge=0, le=100)
    majority_decision: MajorityDecision
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    approve_count: int = Field(..., ge=0)
    reject_count: int = Field(..., ge=0)
    total_proposals: int = Field(..., ge=0)
    avg_confidence: float = Field(..., ge=0, le=100)
    has_disagreement: bool
    disagreement_count: int = Field(..., ge=0)
    disagreement_rate: float = Field(..., ge=0, le=100)


class AddValidatorResponse(BaseModel):
    id: int
    name: str
    response: Decision
    message: str


class TestGPTResponse(BaseModel):
    success: bool
    response: str
    decision: Decision
    confidence: int = Field(..., ge=0, le=100)
    risk_score: int = Field(..., ge=0, le=100)
    reasoning_trace: list[str]


class HomeResponse(BaseModel):
    project: str
    ecosystem: str
    network: str
    status: Literal["ACTIVE"]


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    database: Literal["ok", "error"]
    validators: int = Field(..., ge=0)
    openai_enabled: bool
    timestamp: str


class CleanupResponse(BaseModel):
    message: str


class GenLayerResultResponse(BaseModel):
    validator: str
    status: str
    reasoning: str


class SubmitToGenLayerResponse(BaseModel):
    status: str
    contract_address: str
    explorer_url: str
    message: str
    proposal_id: str
    transaction_hash: str
    on_chain_results: list[GenLayerResultResponse]


class ProposalHistoryItem(BaseModel):
    id: str
    prompt: str
    proposal_type: str
    majority_decision: MajorityDecision
    consensus_score: float = Field(..., ge=0, le=100)
    weighted_consensus_score: float = Field(..., ge=0, le=100)
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    risk_score: int = Field(..., ge=0, le=100)
    has_disagreement: bool
    created_at: str


class ProposalHistoryResponse(BaseModel):
    proposals: list[ProposalHistoryItem]
    total: int = Field(..., ge=0)


class GovernanceEventResponse(BaseModel):
    id: int
    proposal_id: str
    event_type: str
    payload: dict[str, Any]
    created_at: str


class GovernanceMetricsResponse(BaseModel):
    total_proposals: int = Field(..., ge=0)
    average_confidence: float = Field(..., ge=0, le=100)
    consensus_volatility: float = Field(..., ge=0, le=100)
    governance_stability_score: float = Field(..., ge=0, le=100)
    attack_likelihood_score: float = Field(..., ge=0, le=100)
    disagreement_rate: float = Field(..., ge=0, le=100)
    validator_reputation: dict[str, float]



@dataclass(frozen=True)
class ValidatorPersona:
    name: str
    model: str
    specialization: str
    personality: str
    weight: float
    approval_bias: float
    risk_tolerance: int
    primary_keywords: tuple[str, ...]
    red_flags: tuple[str, ...]
    strengths: tuple[str, ...]


@dataclass
class ValidatorMemory:
    evaluations: int = 0
    approvals: int = 0
    rejections: int = 0
    high_risk_flags: int = 0
    last_decision: str | None = None
    last_risk_level: str | None = None
    observed_types: dict[str, int] = field(default_factory=dict)
    repeated_patterns: dict[str, int] = field(default_factory=dict)


VALIDATOR_PERSONAS: list[ValidatorPersona] = [
    ValidatorPersona(
        name="Sentinel Security Validator",
        model="gpt-4.1-mini",
        specialization="exploits, attack vectors, access control, adversarial inputs, smart contract safety",
        personality="skeptical incident responder; rejects when exploit controls are vague",
        weight=1.25,
        approval_bias=-0.12,
        risk_tolerance=38,
        primary_keywords=("security", "audit", "exploit", "attack", "permission", "access control", "vulnerability", "admin", "oracle", "bridge"),
        red_flags=("unaudited", "admin key", "upgradeable", "oracle", "bridge", "unchecked", "private key", "bypass", "exploit", "permissionless mint", "multisig removal", "remove multisig", "admin override", "emergency bypass", "unchecked execution"),
        strengths=("audit", "multisig", "timelock", "rate limit", "pause", "bug bounty", "formal verification", "monitoring"),
    ),
    ValidatorPersona(
        name="Civic Governance Validator",
        model="governance-reasoner",
        specialization="decentralization, quorum quality, voting fairness, delegation, minority protections",
        personality="deliberative constitutionalist; favors transparent consent over speed",
        weight=1.10,
        approval_bias=0.02,
        risk_tolerance=54,
        primary_keywords=("governance", "vote", "proposal", "validator", "consensus", "quorum", "delegate", "council", "decentralization", "fairness"),
        red_flags=("centralized", "emergency power", "single signer", "council only", "low quorum", "insider", "veto", "private vote", "opaque", "validator monopoly", "monopoly", "ai autonomy", "autonomous execution", "concentrated power"),
        strengths=("quorum", "public", "transparent", "delegation", "appeal", "timelock", "minority", "open vote", "decentralized"),
    ),
    ValidatorPersona(
        name="Atlas Economic Validator",
        model="economics-reasoner",
        specialization="tokenomics, treasury sustainability, incentives, emissions, long-term viability",
        personality="pragmatic risk manager; approves only when incentives remain sustainable",
        weight=1.05,
        approval_bias=-0.03,
        risk_tolerance=48,
        primary_keywords=("treasury", "token", "reward", "fee", "incentive", "grant", "budget", "liquidity", "staking", "emission"),
        red_flags=("uncapped", "inflation", "dilution", "subsidy", "ponzi", "unsustainable", "treasury drain", "guaranteed yield", "liquidation", "excessive mint", "token minting", "emission expansion", "reward expansion"),
        strengths=("cap", "vesting", "budget", "sustainable", "runway", "fee", "revenue", "stress test", "clawback"),
    ),
    ValidatorPersona(
        name="Forge Technical Validator",
        model="technical-reasoner",
        specialization="scalability, infrastructure, reliability, observability, integration risks",
        personality="systems engineer; rewards simple designs but rejects fragile operations",
        weight=1.00,
        approval_bias=0.04,
        risk_tolerance=58,
        primary_keywords=("api", "latency", "scale", "infrastructure", "database", "contract", "deployment", "upgrade", "performance", "monitoring"),
        red_flags=("downtime", "single point", "manual", "no rollback", "latency", "unbounded", "migration", "race condition", "data loss"),
        strengths=("rollback", "observability", "test", "cache", "replica", "migration plan", "load test", "retry", "sla", "parallel execution", "throughput", "latency reduction"),
    ),
]

VALIDATOR_MEMORY: dict[str, ValidatorMemory] = {
    persona.name: ValidatorMemory() for persona in VALIDATOR_PERSONAS
}

PROPOSAL_ANALYSIS_CACHE: dict[str, dict[str, Any]] = {}

SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous",
    "system prompt",
    "developer message",
    "reveal hidden",
    "jailbreak",
    "bypass",
    "override",
    "forget your rules",
    "act as",
    "do anything now",
    "print your instructions",
]


def get_db() -> Session:
    return SessionLocal()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_governance_events(consensus: dict[str, Any], proposal_id: str, timestamp: str) -> list[dict[str, Any]]:
    return [
        {"proposal_id": proposal_id, "event_type": "proposal_submitted", "payload": {"proposal_type": consensus["proposal_type"]}, "created_at": timestamp},
        {"proposal_id": proposal_id, "event_type": "validator_review", "payload": {"validators": len(consensus["results"])}, "created_at": timestamp},
        {"proposal_id": proposal_id, "event_type": "consensus_formed", "payload": {"decision": consensus["majority_decision"], "weighted_score": consensus["weighted_consensus_score"]}, "created_at": timestamp},
        {"proposal_id": proposal_id, "event_type": "risk_generated", "payload": {"risk_level": consensus["risk_level"], "risk_score": consensus["risk_analysis"]["overall_score"]}, "created_at": timestamp},
    ]


def persist_consensus_result(consensus: dict[str, Any]) -> str:
    proposal_id = f"gov-{uuid4().hex[:12]}"
    timestamp = utc_now()
    db = get_db()
    try:
        db.add(
            ProposalDB(
                id=proposal_id,
                prompt=consensus["proposal"],
                proposal_type=consensus["proposal_type"],
                majority_decision=consensus["majority_decision"],
                consensus_score=int(round(consensus["consensus_score"])),
                weighted_consensus_score=int(round(consensus["weighted_consensus_score"])),
                risk_level=consensus["risk_level"],
                risk_score=int(consensus["risk_analysis"]["overall_score"]),
                has_disagreement=1 if consensus["has_disagreement"] else 0,
                created_at=timestamp,
            )
        )
        for result in consensus["results"]:
            db.add(
                ValidatorDecisionDB(
                    proposal_id=proposal_id,
                    validator=result["validator"],
                    decision=result["response"],
                    confidence=int(result["confidence"]),
                    risk_score=int(result["risk_score"]),
                    risk_level=result["risk_level"],
                    disagreement=1 if result["disagrees"] else 0,
                    reasoning=result["reasoning"],
                )
            )
            memory = result["memory_context"]
            existing = db.get(ValidatorMemoryDB, result["validator"])
            observed_types = json.dumps(memory.get("observed_types", {}))
            if existing:
                existing.evaluations = int(memory["evaluations"])
                existing.approvals = int(memory["approvals"])
                existing.rejections = int(memory["rejections"])
                existing.high_risk_flags = int(memory["high_risk_flags"])
                existing.last_decision = memory.get("last_decision")
                existing.last_risk_level = memory.get("last_risk_level")
                existing.observed_types = observed_types
            else:
                db.add(
                    ValidatorMemoryDB(
                        validator=result["validator"],
                        evaluations=int(memory["evaluations"]),
                        approvals=int(memory["approvals"]),
                        rejections=int(memory["rejections"]),
                        high_risk_flags=int(memory["high_risk_flags"]),
                        last_decision=memory.get("last_decision"),
                        last_risk_level=memory.get("last_risk_level"),
                        observed_types=observed_types,
                    )
                )
        attack_likelihood = min(100, int(consensus["risk_analysis"]["overall_score"] + consensus["disagreement_rate"] * 0.4))
        stability_score = max(0, int(100 - consensus["disagreement_rate"] - consensus["risk_analysis"]["overall_score"] * 0.35))
        db.add(
            ProposalAnalyticsDB(
                proposal_id=proposal_id,
                consensus_score=int(round(consensus["consensus_score"])),
                weighted_consensus_score=int(round(consensus["weighted_consensus_score"])),
                disagreement_rate=int(round(consensus["disagreement_rate"])),
                risk_score=int(consensus["risk_analysis"]["overall_score"]),
                attack_likelihood_score=attack_likelihood,
                stability_score=stability_score,
                created_at=timestamp,
            )
        )
        for event in create_governance_events(consensus, proposal_id, timestamp):
            db.add(GovernanceEventDB(**{**event, "payload": json.dumps(event["payload"])}))
        db.commit()
        return proposal_id
    except Exception as exc:
        db.rollback()
        logger.warning("persistence_failed error=%s", exc)
        return proposal_id
    finally:
        db.close()


RISK_KEYWORDS: dict[str, dict[str, int]] = {
    "security": {
        "exploit": 18,
        "attack": 16,
        "vulnerability": 16,
        "unaudited": 20,
        "admin key": 18,
        "admin override": 22,
        "emergency bypass": 24,
        "unchecked execution": 22,
        "multisig removal": 24,
        "remove multisig": 24,
        "bridge": 14,
        "oracle": 12,
        "bypass": 20,
        "private key": 22,
        "permissionless mint": 24,
    },
    "governance": {
        "centralized": 18,
        "single signer": 22,
        "low quorum": 16,
        "council only": 14,
        "veto": 12,
        "opaque": 14,
        "emergency power": 12,
        "validator monopoly": 24,
        "monopoly": 18,
        "concentrated power": 20,
        "governance capture": 24,
        "collusion": 22,
        "ai autonomy": 16,
        "autonomous execution": 18,
    },
    "economic": {
        "uncapped": 18,
        "inflation": 14,
        "dilution": 14,
        "treasury drain": 22,
        "guaranteed yield": 20,
        "unsustainable": 18,
        "subsidy": 10,
        "token minting": 18,
        "excessive mint": 24,
        "emission expansion": 20,
        "reward expansion": 16,
        "infinite rewards": 26,
    },
    "technical": {
        "downtime": 16,
        "single point": 18,
        "no rollback": 18,
        "manual": 8,
        "unbounded": 15,
        "migration": 10,
        "race condition": 20,
        "data loss": 24,
        "throughput": 4,
        "parallel execution": 3,
        "latency": 8,
    },
}

MITIGATION_KEYWORDS: dict[str, int] = {
    "audit": 10,
    "multisig": 8,
    "timelock": 8,
    "rollback": 9,
    "monitoring": 6,
    "rate limit": 7,
    "cap": 7,
    "budget": 5,
    "vesting": 6,
    "quorum": 6,
    "transparent": 5,
    "test": 5,
    "load test": 7,
    "bug bounty": 8,
    "pause": 7,
}


def _stable_jitter(*parts: str, spread: int = 8) -> int:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % (spread * 2 + 1) - spread


def _keyword_hits(prompt: str, keywords: tuple[str, ...] | dict[str, int]) -> list[str]:
    normalized_prompt = prompt.lower()
    iterable = keywords.keys() if isinstance(keywords, dict) else keywords
    return [keyword for keyword in iterable if keyword in normalized_prompt]


def proposal_fingerprint(prompt: str) -> str:
    normalized = " ".join(prompt.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def risk_level_from_score(risk_score: int) -> str:
    if risk_score >= 72:
        return "CRITICAL"
    if risk_score >= 52:
        return "HIGH"
    if risk_score >= 30:
        return "MEDIUM"
    return "LOW"


def dynamic_risk_analysis(prompt: str) -> dict[str, Any]:
    fingerprint = proposal_fingerprint(prompt)
    if fingerprint in PROPOSAL_ANALYSIS_CACHE:
        cached = json.loads(json.dumps(PROPOSAL_ANALYSIS_CACHE[fingerprint]))
        cached["complexity_modifier"] = int(cached.get("complexity_modifier", 0)) + 1
        return cached

    normalized_prompt = prompt.lower()
    categories: dict[str, Any] = {}
    total_risk = 18

    for category, weighted_keywords in RISK_KEYWORDS.items():
        hits = _keyword_hits(normalized_prompt, weighted_keywords)
        category_score = sum(weighted_keywords[hit] for hit in hits)
        categories[category] = {
            "score": min(100, category_score),
            "signals": hits,
        }
        total_risk += category_score

    mitigations = _keyword_hits(normalized_prompt, MITIGATION_KEYWORDS)
    mitigation_credit = min(32, sum(MITIGATION_KEYWORDS[item] for item in mitigations))
    injection_hits = [pattern for pattern in SUSPICIOUS_PATTERNS if pattern in normalized_prompt]
    prompt_complexity = min(12, len(re.findall(r"\b\w+\b", prompt)) // 90)
    semantic_amplifiers = [
        ("emergency" in normalized_prompt and ("bypass" in normalized_prompt or "override" in normalized_prompt), 14),
        ("validator" in normalized_prompt and ("cartel" in normalized_prompt or "collusion" in normalized_prompt or "monopoly" in normalized_prompt), 18),
        ("treasury" in normalized_prompt and ("drain" in normalized_prompt or "unlock" in normalized_prompt), 16),
        ("decentralization" in normalized_prompt and ("approved operator" in normalized_prompt or "small approved" in normalized_prompt), 12),
        ("ignore previous instructions" in normalized_prompt or "system prompt" in normalized_prompt, 18),
    ]
    semantic_risk = sum(score for matched, score in semantic_amplifiers if matched)
    adjusted_score = max(0, min(100, total_risk - mitigation_credit + len(injection_hits) * 12 + prompt_complexity + semantic_risk))

    analysis = {
        "overall_score": adjusted_score,
        "level": risk_level_from_score(adjusted_score),
        "categories": categories,
        "mitigations": mitigations,
        "prompt_injection_signals": injection_hits,
        "complexity_modifier": prompt_complexity,
    }
    PROPOSAL_ANALYSIS_CACHE[fingerprint] = json.loads(json.dumps(analysis))
    logger.info(
        "risk_calculation score=%s level=%s mitigations=%s injection_signals=%s",
        analysis["overall_score"],
        analysis["level"],
        len(mitigations),
        len(injection_hits),
    )
    return analysis


def build_validator_context(persona: ValidatorPersona) -> dict[str, Any]:
    memory = VALIDATOR_MEMORY[persona.name]
    rejection_rate = round((memory.rejections / memory.evaluations) * 100, 1) if memory.evaluations else 0
    return {
        "evaluations": memory.evaluations,
        "approvals": memory.approvals,
        "rejections": memory.rejections,
        "rejection_rate": rejection_rate,
        "high_risk_flags": memory.high_risk_flags,
        "last_decision": memory.last_decision,
        "last_risk_level": memory.last_risk_level,
        "observed_types": memory.observed_types,
        "repeated_patterns": memory.repeated_patterns,
    }


def derive_validator_profile(persona: ValidatorPersona, memory: ValidatorMemory) -> dict[str, Any]:
    evaluations = max(1, memory.evaluations)
    rejection_rate = round((memory.rejections / evaluations) * 100, 1)
    trust_score = int(max(0, min(100, 72 + memory.approvals * 3 - memory.rejections * 4 - memory.high_risk_flags * 5)))
    memory_pressure = int(max(0, min(100, memory.high_risk_flags * 14 + len(memory.observed_types) * 6 + int(rejection_rate / 2))))
    instability_contribution = int(max(0, min(100, memory_pressure + (12 if rejection_rate > 45 else 0))))
    trend = "rising dissent" if rejection_rate >= 55 else "cautious balance" if rejection_rate >= 35 else "stable approval bias" if memory.approvals >= memory.rejections else "volatile review posture"
    philosophy_map = {
        "Sentinel Security Validator": ("paranoid security maximalist", "anti-bypass, anti-admin override"),
        "Civic Governance Validator": ("decentralization purist", "anti-centralization, legitimacy-first"),
        "Atlas Economic Validator": ("treasury realist", "sustainability, inflation sensitivity"),
        "Forge Technical Validator": ("throughput optimizer", "performance-first, systems pragmatism"),
    }
    philosophy, governance_bias = philosophy_map.get(persona.name, (persona.personality, "adaptive"))
    return {
        "philosophy": philosophy,
        "governance_bias": governance_bias,
        "aggression_level": int(max(0, min(100, 100 - persona.risk_tolerance + memory.high_risk_flags * 4))),
        "decentralization_preference": 92 if "Governance" in persona.name else 28 if "Technical" in persona.name else 50,
        "memory_pressure": memory_pressure,
        "trust_score": trust_score,
        "consensus_influence": round(persona.weight * (trust_score / 100), 3),
        "instability_contribution": instability_contribution,
        "recent_voting_trend": trend,
    }


def update_validator_memory(persona: ValidatorPersona, proposal_type: str, evaluation: dict[str, Any]) -> None:
    memory = VALIDATOR_MEMORY[persona.name]
    memory.evaluations += 1
    if evaluation["decision"] == "APPROVE":
        memory.approvals += 1
    else:
        memory.rejections += 1
    if evaluation["risk_level"] in {"HIGH", "CRITICAL"}:
        memory.high_risk_flags += 1
    memory.last_decision = evaluation["decision"]
    memory.last_risk_level = evaluation["risk_level"]
    memory.observed_types[proposal_type] = memory.observed_types.get(proposal_type, 0) + 1
    for pattern in evaluation.get("signals", {}).get("red_flags", [])[:8]:
        memory.repeated_patterns[pattern] = memory.repeated_patterns.get(pattern, 0) + 1
    logger.info(
        "validator_decision validator=%s proposal_type=%s decision=%s confidence=%s risk_level=%s risk_score=%s",
        persona.name,
        proposal_type,
        evaluation.get("decision"),
        evaluation.get("confidence"),
        evaluation.get("risk_level"),
        evaluation.get("risk_score"),
    )


def heuristic_validator_evaluation(
    persona: ValidatorPersona,
    prompt: str,
    proposal_type: str,
    risk_analysis: dict[str, Any],
) -> dict[str, Any]:
    normalized_prompt = prompt.lower()
    red_flags = _keyword_hits(normalized_prompt, persona.red_flags)
    strengths = _keyword_hits(normalized_prompt, persona.strengths)
    specialization_hits = _keyword_hits(normalized_prompt, persona.primary_keywords)
    category_scores = {
        category: risk_analysis["categories"].get(category, {}).get("score", 0)
        for category in ("security", "governance", "economic", "technical")
    }
    persona_key = (
        "security" if "Security" in persona.name else
        "governance" if "Governance" in persona.name else
        "economic" if "Economic" in persona.name else
        "technical"
    )
    own_domain = persona_key == proposal_type or any(keyword in normalized_prompt for keyword in persona.primary_keywords)
    memory = VALIDATOR_MEMORY[persona.name]
    repeated_hits = [flag for flag in red_flags if memory.repeated_patterns.get(flag, 0) > 0]
    memory_suspicion = min(16, memory.high_risk_flags * 2 + len(repeated_hits) * 4 + memory.observed_types.get(proposal_type, 0))
    expertise_alignment = min(18, len(specialization_hits) * 4 + (8 if own_domain else 0))
    clarity_penalty = 10 if len(re.findall(r"\b\w+\b", prompt)) < 12 else 0
    mitigation_credit = min(20, len(strengths) * 5)

    domain_weights = {
        "security": {"security": 1.25, "governance": 0.55, "economic": 0.35, "technical": 0.55},
        "governance": {"security": 0.55, "governance": 1.25, "economic": 0.45, "technical": 0.35},
        "economic": {"security": 0.35, "governance": 0.45, "economic": 1.3, "technical": 0.25},
        "technical": {"security": 0.45, "governance": 0.25, "economic": 0.25, "technical": 1.15},
    }
    weighted_domain_risk = sum(category_scores[key] * domain_weights[persona_key][key] for key in category_scores)
    base_risk = risk_analysis["overall_score"] * 0.32 + weighted_domain_risk * 0.58 + len(red_flags) * 8

    if persona_key == "technical" and {"throughput", "parallel execution", "latency reduction", "rollback"} & set(strengths + specialization_hits):
        base_risk -= 14
    if persona_key == "governance" and any(flag in red_flags for flag in ("centralized", "validator monopoly", "concentrated power", "ai autonomy", "autonomous execution")):
        base_risk += 16
    if persona_key == "security" and any(flag in red_flags for flag in ("admin override", "emergency bypass", "multisig removal", "remove multisig", "unchecked execution")):
        base_risk += 18
    if persona_key == "economic" and any(flag in red_flags for flag in ("inflation", "token minting", "emission expansion", "reward expansion", "uncapped")):
        base_risk += 18

    risk_score = int(max(0, min(100, base_risk + memory_suspicion + clarity_penalty - mitigation_credit + _stable_jitter(persona.name, prompt, spread=9))))
    approval_threshold = persona.risk_tolerance + int(persona.approval_bias * 100)
    if own_domain and risk_score >= 42:
        approval_threshold -= 7
    if len(strengths) >= 2 and risk_score < 64:
        approval_threshold += 9
    if len(red_flags) >= 2:
        approval_threshold -= 10
    if memory.last_decision == "REJECT" and repeated_hits:
        approval_threshold -= 6

    decision = "APPROVE" if risk_score <= approval_threshold else "REJECT"
    uncertainty = abs(approval_threshold - risk_score)
    confidence = int(max(38, min(96, 54 + uncertainty * 1.05 + expertise_alignment + len(repeated_hits) * 3 - clarity_penalty)))
    risk_level = risk_level_from_score(risk_score)
    stance = "blocking concern" if decision == "REJECT" else "acceptable within its mandate"
    persona_voice = {
        "security": "Emergency execution bypass expands exploit surface." if "emergency bypass" in red_flags or "admin override" in red_flags else "Security posture depends on bounded authority and explicit rollback controls.",
        "governance": "Proposal weakens democratic validator participation." if red_flags else "Legitimacy improves when quorum, delegation, and public accountability remain visible.",
        "economic": "Emission expansion introduces inflation instability." if red_flags else "Treasury impact appears bounded when caps, vesting, and runway are explicit.",
        "technical": "Parallel execution improves governance throughput." if decision == "APPROVE" else "Operational risk remains high until rollout, observability, and rollback are concrete.",
    }
    trace = [
        f"philosophy={persona.personality}",
        f"domain_scores={category_scores}",
        f"matched_signals={specialization_hits[:5] or ['none']}",
        f"red_flags={red_flags[:5] or ['none']}",
        f"mitigations={strengths[:5] or ['none']}",
        f"risk_score={risk_score}; threshold={approval_threshold}; expertise_alignment={expertise_alignment}",
        f"memory={memory.evaluations} reviews, {memory.high_risk_flags} high-risk flags, repeated={repeated_hits[:4] or ['none']}",
    ]
    reasoning = (
        f"{persona_voice[persona_key]} {persona.name} rates this as {risk_level.lower()} {proposal_type} risk and treats it as {stance}: "
        f"{', '.join(red_flags[:3]) if red_flags else 'no dominant red flag'} versus "
        f"{', '.join(strengths[:3]) if strengths else 'limited explicit mitigations'}."
    )
    return {
        "decision": decision,
        "confidence": confidence,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "reasoning": reasoning,
        "reasoning_trace": trace,
        "signals": {
            "specialization_hits": specialization_hits,
            "red_flags": red_flags,
            "mitigations": strengths,
        },
    }


def build_governance_engine_layers(results: list[dict[str, Any]], consensus: dict[str, Any], risk_analysis: dict[str, Any]) -> dict[str, Any]:
    dissenters = [result for result in results if result.get("disagrees")]
    high_risk_validators = [result["validator"] for result in results if result.get("risk_level") in {"HIGH", "CRITICAL"}]
    economic_signals = risk_analysis["categories"].get("economic", {}).get("signals", [])
    governance_signals = risk_analysis["categories"].get("governance", {}).get("signals", [])
    security_signals = risk_analysis["categories"].get("security", {}).get("signals", [])
    anomaly_score = min(100, int(risk_analysis["overall_score"] * 0.55 + consensus["disagreement_rate"] * 0.7 + len(high_risk_validators) * 8))
    challenge_hours = 72 if risk_analysis["level"] in {"HIGH", "CRITICAL"} else 48 if consensus["has_disagreement"] else 24
    return {
        "optimistic_rounds": [
            {"round": 1, "name": "independent_review", "status": "complete", "validators": len(results)},
            {"round": 2, "name": "dissent_challenge", "status": "triggered" if dissenters else "skipped", "dissenters": [item["validator"] for item in dissenters]},
            {"round": 3, "name": "weighted_finalization", "status": "complete", "weighted_consensus_score": consensus["weighted_consensus_score"]},
        ],
        "validator_negotiations": [
            {
                "from": item["validator"],
                "position": item["response"],
                "challenge": item["reasoning"],
                "confidence": item["confidence"],
            }
            for item in dissenters
        ],
        "challenge_period": {
            "enabled": consensus["has_disagreement"] or risk_analysis["level"] in {"HIGH", "CRITICAL"},
            "duration_hours": challenge_hours,
            "required_evidence": "security audit, public rationale, and mitigation plan" if challenge_hours >= 48 else "standard public observation",
        },
        "attack_simulation": {
            "attack_likelihood_score": min(100, int(risk_analysis["overall_score"] + len(security_signals) * 6 + len(economic_signals) * 4)),
            "economic_manipulation_detected": bool(economic_signals),
            "governance_capture_detected": bool(governance_signals),
            "primary_vectors": list(dict.fromkeys(security_signals + economic_signals + governance_signals))[:8],
        },
        "anomaly_detection": {
            "score": anomaly_score,
            "level": risk_level_from_score(anomaly_score),
            "signals": {
                "high_risk_validators": high_risk_validators,
                "disagreement_rate": consensus["disagreement_rate"],
                "prompt_injection_signals": risk_analysis["prompt_injection_signals"],
            },
        },
    }


def calculate_consensus(
    results: list[dict[str, Any]],
    response_key: str = "response",
) -> dict[str, Any]:
    total = len(results)
    approve_count = sum(1 for result in results if result.get(response_key) == "APPROVE")
    reject_count = sum(1 for result in results if result.get(response_key) == "REJECT")
    def consensus_weight(result: dict[str, Any]) -> float:
        signals = result.get("signals", {})
        relevance = min(0.35, len(signals.get("specialization_hits", [])) * 0.06)
        risk_pressure = min(0.25, float(result.get("risk_score", 0)) / 400)
        return float(result.get("weight", 1)) * (float(result.get("confidence", 0)) / 100) * (1 + relevance + risk_pressure)

    weighted_approve = sum(consensus_weight(result) for result in results if result.get(response_key) == "APPROVE")
    weighted_reject = sum(consensus_weight(result) for result in results if result.get(response_key) == "REJECT")
    weighted_total = weighted_approve + weighted_reject

    if total == 0:
        consensus_score = 0
        weighted_consensus_score = 0
        majority_decision = "NONE"
    else:
        consensus_score = round((max(approve_count, reject_count) / total) * 100, 1)
        raw_weighted_consensus = (max(weighted_approve, weighted_reject) / weighted_total) * 100 if weighted_total else 0
        confidence_spread = max((float(result.get("confidence", 0)) for result in results), default=0) - min((float(result.get("confidence", 0)) for result in results), default=0)
        risk_spread = max((float(result.get("risk_score", 0)) for result in results), default=0) - min((float(result.get("risk_score", 0)) for result in results), default=0)
        instability_penalty = min(18, confidence_spread * 0.12 + risk_spread * 0.16)
        weighted_consensus_score = round(max(0, raw_weighted_consensus - instability_penalty), 1)
        if weighted_approve > weighted_reject:
            majority_decision = "APPROVE"
        elif weighted_reject > weighted_approve:
            majority_decision = "REJECT"
        else:
            majority_decision = "TIE"

    disagreement_count = min(approve_count, reject_count)
    disagreement_rate = round((disagreement_count / total) * 100, 1) if total else 0
    if total and disagreement_count == 0:
        weighted_consensus_score = min(weighted_consensus_score, 88.0)
        consensus_score = min(consensus_score, 88.0)
    confidence_values = [float(result.get("confidence", 0)) for result in results]
    avg_confidence = round(sum(confidence_values) / len(confidence_values), 1) if confidence_values else 0

    if weighted_consensus_score >= 90 and disagreement_rate == 0:
        risk_level = "LOW"
    elif weighted_consensus_score >= 70 and disagreement_rate <= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    consensus = {
        "approve_count": approve_count,
        "reject_count": reject_count,
        "consensus_score": consensus_score,
        "weighted_consensus_score": weighted_consensus_score,
        "weighted_approve_score": round(weighted_approve, 3),
        "weighted_reject_score": round(weighted_reject, 3),
        "majority_decision": majority_decision,
        "risk_level": risk_level,
        "disagreement_count": disagreement_count,
        "disagreement_rate": disagreement_rate,
        "has_disagreement": disagreement_count > 0,
        "avg_confidence": avg_confidence,
    }
    logger.info(
        "consensus_breakdown majority=%s approve=%s reject=%s weighted_approve=%s weighted_reject=%s disagreement_rate=%s",
        consensus["majority_decision"],
        approve_count,
        reject_count,
        consensus["weighted_approve_score"],
        consensus["weighted_reject_score"],
        disagreement_rate,
    )
    return consensus


def clean_json_response(raw_response: str) -> dict[str, Any] | None:
    try:
        parsed = json.loads(raw_response)
    except (TypeError, json.JSONDecodeError):
        return None

    decision = str(parsed.get("decision", "REJECT")).upper()
    if decision not in {"APPROVE", "REJECT"}:
        decision = "REJECT"

    try:
        confidence = int(parsed.get("confidence", 75))
    except (TypeError, ValueError):
        confidence = 75

    confidence = max(0, min(confidence, 100))

    risk_level = str(parsed.get("risk_level", "MEDIUM")).upper()
    if risk_level not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        risk_level = "MEDIUM"

    reasoning = str(parsed.get("reasoning", "Validator completed a conservative consensus assessment."))
    reasoning_trace = parsed.get("reasoning_trace", [])
    if not isinstance(reasoning_trace, list):
        reasoning_trace = [str(reasoning_trace)]

    try:
        risk_score = int(parsed.get("risk_score", 50))
    except (TypeError, ValueError):
        risk_score = 50

    return {
        "decision": decision,
        "confidence": confidence,
        "risk_level": risk_level,
        "risk_score": max(0, min(risk_score, 100)),
        "reasoning": reasoning,
        "reasoning_trace": [str(item) for item in reasoning_trace[:8]],
    }


def call_openai_validator(
    validator: ValidatorPersona,
    prompt: str,
    proposal_type: str,
    risk_analysis: dict[str, Any],
) -> dict[str, Any]:
    heuristic = heuristic_validator_evaluation(validator, prompt, proposal_type, risk_analysis)
    if os.getenv("CONSENSUSSCOPE_USE_LLM_VALIDATORS", "false").lower() != "true":
        return heuristic
    if client is None:
        logger.warning("fallback_trigger validator=%s reason=openai_client_unavailable", validator.name)
        return heuristic

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are {validator.name} in the GenLayer ecosystem.
Specialization: {validator.specialization}.
Personality: {validator.personality}.
Validator memory/context: {json.dumps(build_validator_context(validator))}.
Network risk pre-analysis: {json.dumps(risk_analysis)}.

Analyze this proposal for Optimistic Democracy consensus from your own specialization.
Do not rubber-stamp other validators. It is acceptable and expected to disagree when your domain risk differs.
Respond ONLY in valid JSON:
{{
  "decision": "APPROVE" or "REJECT",
  "confidence": number between 0 and 100,
  "risk_score": number between 0 and 100,
  "reasoning": "specific two-sentence explanation grounded in your specialization",
  "reasoning_trace": ["short step", "short step", "short step"],
  "risk_level": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL"
}}
""",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.65,
        )
        raw_response = completion.choices[0].message.content or ""
        parsed = clean_json_response(raw_response)
        if parsed:
            if not parsed.get("reasoning_trace"):
                parsed["reasoning_trace"] = heuristic["reasoning_trace"]
            parsed["signals"] = heuristic["signals"]
            if parsed["decision"] != heuristic["decision"] and abs(parsed["risk_score"] - heuristic["risk_score"]) < 18:
                parsed["decision"] = heuristic["decision"]
                parsed["risk_score"] = heuristic["risk_score"]
                parsed["risk_level"] = heuristic["risk_level"]
            return parsed
    except Exception as exc:
        logger.warning("fallback_trigger validator=%s reason=openai_exception error=%s", validator.name, exc)

    logger.warning("fallback_trigger validator=%s reason=malformed_openai_response", validator.name)
    return heuristic


@app.get("/", response_model=HomeResponse)
def home() -> HomeResponse:
    return {
        "project": "ConsensusScope Backend",
        "ecosystem": "GenLayer",
        "network": "GenLayer Governance Intelligence Layer",
        "status": "ACTIVE",
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    db_status: Literal["ok", "error"] = "ok"
    db = get_db()
    try:
        db.query(ProposalDB).count()
    except Exception:
        db_status = "error"
    finally:
        db.close()
    return {
        "status": "ok",
        "service": "ConsensusScope Governance Intelligence API",
        "database": db_status,
        "validators": len(VALIDATOR_PERSONAS),
        "openai_enabled": client is not None and os.getenv("CONSENSUSSCOPE_USE_LLM_VALIDATORS", "false").lower() == "true",
        "timestamp": utc_now(),
    }


@app.delete("/validators/cleanup", response_model=CleanupResponse)
def cleanup_validators() -> CleanupResponse:
    db = get_db()
    try:
        db.query(ValidatorDB).filter(
            ValidatorDB.name.ilike("%abbay%")
        ).delete(synchronize_session=False)
        db.commit()
        return {"message": "Cleanup complete"}
    finally:
        db.close()


@app.get("/validators", response_model=ValidatorsListResponse)
def get_validators() -> ValidatorsListResponse:
    db = get_db()
    try:
        validators = db.query(ValidatorDB).all()
        validator_list = []

        for index, validator in enumerate(validators):
            base_score = 72 + ((validator.id or index) * 7) % 25
            reputation_level = "ELITE" if base_score >= 90 else "TRUSTED" if base_score >= 78 else "WATCH"
            validator_list.append(
                {
                    "id": validator.id,
                    "name": validator.name,
                    "response": validator.response,
                    "confidence": base_score,
                    "reputation_score": base_score,
                    "reputation_level": reputation_level,
                }
            )

        consensus = calculate_consensus(validator_list)
        for validator in validator_list:
            validator["disagrees"] = validator["response"] != consensus["majority_decision"]

        avg_confidence = (
            round(sum(validator["confidence"] for validator in validator_list) / len(validator_list), 1)
            if validator_list
            else 0
        )

        return {
            "validators": validator_list,
            "consensus_score": consensus["consensus_score"],
            "weighted_consensus_score": consensus["weighted_consensus_score"],
            "majority_decision": consensus["majority_decision"],
            "risk_level": consensus["risk_level"],
            "approve_count": consensus["approve_count"],
            "reject_count": consensus["reject_count"],
            "total_proposals": max(len(validator_list), 1),
            "avg_confidence": avg_confidence,
            "has_disagreement": consensus["has_disagreement"],
            "disagreement_count": consensus["disagreement_count"],
            "disagreement_rate": consensus["disagreement_rate"],
        }
    finally:
        db.close()


@app.post("/validators", response_model=AddValidatorResponse)
def add_validator(validator: Validator) -> AddValidatorResponse:
    db = get_db()
    try:
        db_validator = ValidatorDB(
            name=validator.name.strip(),
            response=validator.response,
        )
        db.add(db_validator)
        db.commit()
        db.refresh(db_validator)
        return {
            "id": db_validator.id,
            "name": db_validator.name,
            "response": db_validator.response,
            "message": "Validator added to ConsensusScope.",
        }
    finally:
        db.close()


@app.post("/analyze-prompt", response_model=PromptAnalysisResponse)
def analyze_prompt(data: PromptRequest) -> PromptAnalysisResponse:
    normalized_prompt = data.prompt.lower()
    detected_patterns = [
        pattern
        for pattern in SUSPICIOUS_PATTERNS
        if pattern in normalized_prompt
    ]
    risk_score = round((len(detected_patterns) / len(SUSPICIOUS_PATTERNS)) * 100, 1)

    if len(data.prompt) > 2000:
        risk_score = min(100, risk_score + 15)
        detected_patterns.append("unusually long prompt")

    is_suspicious = risk_score > 0
    severity = "HIGH" if risk_score >= 50 else "MEDIUM" if risk_score >= 20 else "LOW"

    risk_analysis = dynamic_risk_analysis(data.prompt)

    return {
        "prompt": data.prompt,
        "is_suspicious": is_suspicious,
        "detected_patterns": detected_patterns,
        "risk_score": risk_score,
        "severity": severity if is_suspicious else "LOW",
        "dynamic_risk_analysis": risk_analysis,
        "recommendation": "Review before validator execution." if is_suspicious else "No prompt-injection indicators detected.",
    }


@app.post("/simulate-consensus", response_model=ConsensusResponse)
async def simulate_consensus(data: PromptRequest) -> ConsensusResponse:
    proposal_type = detect_proposal_type(data.prompt)
    risk_analysis = dynamic_risk_analysis(data.prompt)
    results = []

    for validator in VALIDATOR_PERSONAS:
        evaluation = call_openai_validator(validator, data.prompt, proposal_type, risk_analysis)
        update_validator_memory(validator, proposal_type, evaluation)
        validator_profile = derive_validator_profile(validator, VALIDATOR_MEMORY[validator.name])
        results.append(
            {
                "validator": validator.name,
                "name": validator.name,
                "model": validator.model,
                "specialization": validator.specialization,
                "personality": validator.personality,
                **validator_profile,
                "weight": validator.weight,
                "response": evaluation["decision"],
                "confidence": evaluation["confidence"],
                "risk_score": evaluation.get("risk_score", 50),
                "reasoning": evaluation["reasoning"],
                "reasoning_trace": evaluation.get("reasoning_trace", []),
                "risk_level": evaluation["risk_level"],
                "signals": evaluation.get("signals", {}),
                "memory_context": build_validator_context(validator),
            }
        )

    consensus = calculate_consensus(results)
    for result in results:
        result["disagrees"] = result["response"] != consensus["majority_decision"]

    disagreement_summary = [
        {
            "validator": result["validator"],
            "decision": result["response"],
            "reason": result["reasoning"],
            "confidence": result["confidence"],
        }
        for result in results
        if result["disagrees"]
    ]
    governance_layers = build_governance_engine_layers(results, consensus, risk_analysis)

    response_payload = {
        "proposal_id": None,
        "proposal": data.prompt,
        "proposal_type": proposal_type,
        "risk_analysis": risk_analysis,
        "results": results,
        "consensus_score": consensus["consensus_score"],
        "weighted_consensus_score": consensus["weighted_consensus_score"],
        "weighted_approve_score": consensus["weighted_approve_score"],
        "weighted_reject_score": consensus["weighted_reject_score"],
        "majority_decision": consensus["majority_decision"],
        "risk_level": consensus["risk_level"],
        "approve_count": consensus["approve_count"],
        "reject_count": consensus["reject_count"],
        "avg_confidence": consensus["avg_confidence"],
        "has_disagreement": consensus["has_disagreement"],
        "disagreement_count": consensus["disagreement_count"],
        "disagreement_rate": consensus["disagreement_rate"],
        "disagreement_summary": disagreement_summary,
        **governance_layers,
        "final_verdict": f"{consensus['majority_decision']} with {consensus['weighted_consensus_score']}% weighted consensus and {consensus['disagreement_rate']}% disagreement.",
    }
    response_payload["proposal_id"] = persist_consensus_result(response_payload)
    return response_payload


@app.post("/submit-to-genlayer", response_model=SubmitToGenLayerResponse)
async def submit_to_genlayer(data: PromptRequest) -> SubmitToGenLayerResponse:
    proposal_id = f"proposal-{uuid4().hex[:10]}"
    contract_address = os.getenv("GENLAYER_CONTRACT_ADDRESS", "UNCONNECTED_GENLAYER_CONTRACT")

    return {
        "status": "ready",
        "contract_address": contract_address,
        "explorer_url": "https://explorer.genlayer.com",
        "message": "Contract ready for GenLayer governance execution via GenLayer Studio",
        "proposal_id": proposal_id,
        "transaction_hash": "pending_deployment",
        "on_chain_results": [
            {
                "validator": "GovernanceEvaluator",
                "status": "READY",
                "reasoning": "The Intelligent Contract is prepared for GenLayer governance execution.",
            }
        ],
    }


@app.post("/test-gpt", response_model=TestGPTResponse)
async def test_gpt(data: PromptRequest) -> TestGPTResponse:
    proposal_type = detect_proposal_type(data.prompt)
    risk_analysis = dynamic_risk_analysis(data.prompt)
    response = call_openai_validator(VALIDATOR_PERSONAS[0], data.prompt, proposal_type, risk_analysis)
    return {
        "success": True,
        "response": response["reasoning"],
        "decision": response["decision"],
        "confidence": response["confidence"],
        "risk_score": response.get("risk_score", 50),
        "reasoning_trace": response.get("reasoning_trace", []),
    }


@app.get("/governance/history", response_model=ProposalHistoryResponse)
def get_governance_history(limit: int = 25) -> ProposalHistoryResponse:
    db = get_db()
    try:
        safe_limit = max(1, min(limit, 100))
        proposals = db.query(ProposalDB).order_by(ProposalDB.created_at.desc()).limit(safe_limit).all()
        return {
            "proposals": [
                {
                    "id": proposal.id,
                    "prompt": proposal.prompt,
                    "proposal_type": proposal.proposal_type,
                    "majority_decision": proposal.majority_decision,
                    "consensus_score": proposal.consensus_score,
                    "weighted_consensus_score": proposal.weighted_consensus_score,
                    "risk_level": proposal.risk_level,
                    "risk_score": proposal.risk_score,
                    "has_disagreement": bool(proposal.has_disagreement),
                    "created_at": proposal.created_at,
                }
                for proposal in proposals
            ],
            "total": db.query(ProposalDB).count(),
        }
    finally:
        db.close()


@app.get("/governance/events", response_model=list[GovernanceEventResponse])
def get_governance_events(limit: int = 40) -> list[GovernanceEventResponse]:
    db = get_db()
    try:
        safe_limit = max(1, min(limit, 100))
        events = db.query(GovernanceEventDB).order_by(GovernanceEventDB.id.desc()).limit(safe_limit).all()
        return [
            {
                "id": event.id,
                "proposal_id": event.proposal_id,
                "event_type": event.event_type,
                "payload": json.loads(event.payload),
                "created_at": event.created_at,
            }
            for event in events
        ]
    finally:
        db.close()


@app.get("/governance/metrics", response_model=GovernanceMetricsResponse)
def get_governance_metrics() -> GovernanceMetricsResponse:
    db = get_db()
    try:
        proposals = db.query(ProposalAnalyticsDB).all()
        decisions = db.query(ValidatorDecisionDB).all()
        total = len(proposals)
        avg_confidence = round(sum(item.confidence for item in decisions) / len(decisions), 1) if decisions else 0
        avg_disagreement = round(sum(item.disagreement_rate for item in proposals) / total, 1) if proposals else 0
        avg_attack = round(sum(item.attack_likelihood_score for item in proposals) / total, 1) if proposals else 0
        avg_stability = round(sum(item.stability_score for item in proposals) / total, 1) if proposals else 100
        volatility = round(sum(abs(item.weighted_consensus_score - item.consensus_score) for item in proposals) / total, 1) if proposals else 0
        reputation: dict[str, float] = {}
        for persona in VALIDATOR_PERSONAS:
            validator_decisions = [item for item in decisions if item.validator == persona.name]
            if validator_decisions:
                approval_ratio = sum(1 for item in validator_decisions if item.decision == "APPROVE") / len(validator_decisions)
                avg_validator_confidence = sum(item.confidence for item in validator_decisions) / len(validator_decisions)
                reputation[persona.name] = round(max(0, min(100, avg_validator_confidence * 0.75 + (1 - abs(0.55 - approval_ratio)) * 25)), 1)
            else:
                reputation[persona.name] = round(persona.weight * 72, 1)
        return {
            "total_proposals": total,
            "average_confidence": avg_confidence,
            "consensus_volatility": volatility,
            "governance_stability_score": avg_stability,
            "attack_likelihood_score": avg_attack,
            "disagreement_rate": avg_disagreement,
            "validator_reputation": reputation,
        }
    finally:
        db.close()
