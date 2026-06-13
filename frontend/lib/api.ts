export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type Decision = "APPROVE" | "REJECT" | "TIE" | "NONE";
export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface RiskCategory {
  score: number;
  signals: string[];
}

export interface RiskAnalysis {
  overall_score: number;
  level: RiskLevel;
  categories: Record<string, RiskCategory>;
  mitigations: string[];
  prompt_injection_signals: string[];
  complexity_modifier: number;
}

export interface ValidatorSignals {
  specialization_hits: string[];
  red_flags: string[];
  mitigations: string[];
}

export interface ValidatorMemoryContext {
  evaluations: number;
  approvals: number;
  rejections: number;
  rejection_rate: number;
  high_risk_flags: number;
  last_decision: Decision | null;
  last_risk_level: RiskLevel | null;
  observed_types: Record<string, number>;
}

export interface SimulationValidator {
  validator: string;
  name: string;
  model: string;
  specialization: string;
  personality: string;
  philosophy: string;
  governance_bias: string;
  aggression_level: number;
  decentralization_preference: number;
  memory_pressure: number;
  trust_score: number;
  consensus_influence: number;
  instability_contribution: number;
  recent_voting_trend: string;
  weight: number;
  response: "APPROVE" | "REJECT";
  confidence: number;
  risk_score: number;
  reasoning: string;
  reasoning_trace: string[];
  risk_level: RiskLevel;
  signals: ValidatorSignals;
  memory_context: ValidatorMemoryContext;
  disagrees: boolean;
}

export interface ConsensusResult {
  proposal_id: string | null;
  proposal: string;
  proposal_type: string;
  risk_analysis: RiskAnalysis;
  results: SimulationValidator[];
  consensus_score: number;
  weighted_consensus_score: number;
  weighted_approve_score: number;
  weighted_reject_score: number;
  majority_decision: Decision;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  approve_count: number;
  reject_count: number;
  avg_confidence: number;
  has_disagreement: boolean;
  disagreement_count: number;
  disagreement_rate: number;
  disagreement_summary: Array<{ validator: string; decision: "APPROVE" | "REJECT"; reason: string; confidence: number }>;
  optimistic_rounds: Array<Record<string, unknown>>;
  validator_negotiations: Array<Record<string, unknown>>;
  challenge_period: Record<string, unknown>;
  attack_simulation: Record<string, unknown>;
  anomaly_detection: Record<string, unknown>;
  final_verdict: string;
}

export interface PromptAnalysis {
  prompt: string;
  is_suspicious: boolean;
  detected_patterns: string[];
  risk_score: number;
  severity: "LOW" | "MEDIUM" | "HIGH";
  dynamic_risk_analysis: RiskAnalysis;
  recommendation: string;
}

export interface ProposalHistoryItem {
  id: string;
  prompt: string;
  proposal_type: string;
  majority_decision: Decision;
  consensus_score: number;
  weighted_consensus_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  risk_score: number;
  has_disagreement: boolean;
  created_at: string;
}

export interface GovernanceMetrics {
  total_proposals: number;
  average_confidence: number;
  consensus_volatility: number;
  governance_stability_score: number;
  attack_likelihood_score: number;
  disagreement_rate: number;
  validator_reputation: Record<string, number>;
}

export interface GovernanceEvent {
  id: number;
  proposal_id: string;
  event_type: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export async function apiFetch<T>(path: string, init?: RequestInit, retries = 1): Promise<T> {
  let lastError: unknown;
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      const response = await fetch(`${API_BASE}${path}`, {
        ...init,
        headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
      });
      if (!response.ok) {
        throw new Error(`API ${response.status}: ${response.statusText}`);
      }
      return (await response.json()) as T;
    } catch (error) {
      lastError = error;
      if (attempt < retries) await new Promise((resolve) => setTimeout(resolve, 400 * (attempt + 1)));
    }
  }
  throw lastError instanceof Error ? lastError : new Error("ConsensusScope API request failed");
}
