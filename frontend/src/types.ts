export type ThemeRow = { theme: string; count: number; negative_count: number; negative_share: number };
export type Feedback = {
  id: number; text: string; source: string; segment: string;
  theme: string; sentiment: "negative" | "neutral" | "positive"; created_at: string;
};
export type Opportunity = {
  id: number; title: string; problem_statement: string; theme: string;
  reach: number; impact: number; confidence: number; effort: number;
  status: string; rice_score: number; created_at: string;
};
export type Experiment = {
  id: number; title: string; hypothesis: string; success_metric: string;
  baseline_value: number | null; target_value: number | null;
  status: string; owner: string; created_at: string;
};
export type Dashboard = {
  feedback_count: number; negative_feedback: number; opportunity_count: number;
  active_experiments: number; sentiment: Record<string, number>;
  themes: ThemeRow[]; top_opportunities: Opportunity[]; recent_feedback: Feedback[];
  data_note: string;
};