import type { Dashboard, Experiment, Feedback, Opportunity } from "./types";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  dashboard: () => request<Dashboard>("/api/dashboard"),
  feedback: (search = "") => request<Feedback[]>(`/api/feedback${search ? `?search=${encodeURIComponent(search)}` : ""}`),
  addFeedback: (payload: { text: string; source: string; segment: string }) =>
    request<Feedback>("/api/feedback", { method: "POST", body: JSON.stringify(payload) }),
  opportunities: () => request<Opportunity[]>("/api/opportunities"),
  addOpportunity: (payload: Partial<Opportunity>) =>
    request<Opportunity>("/api/opportunities", { method: "POST", body: JSON.stringify(payload) }),
  updateOpportunity: (id: number, status: string) =>
    request<Opportunity>(`/api/opportunities/${id}/status`, { method: "PATCH", body: JSON.stringify({ status }) }),
  experiments: () => request<Experiment[]>("/api/experiments"),
  addExperiment: (payload: Partial<Experiment>) =>
    request<Experiment>("/api/experiments", { method: "POST", body: JSON.stringify(payload) }),
  updateExperiment: (id: number, status: string) =>
    request<Experiment>(`/api/experiments/${id}/status`, { method: "PATCH", body: JSON.stringify({ status }) }),
  reseed: () => request<{ status: string }>("/api/demo/reseed", { method: "POST" }),
};