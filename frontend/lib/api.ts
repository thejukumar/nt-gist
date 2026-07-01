// Typed client for the backend API.

import type {
  ChatTurnResponse,
  DemoRunResponse,
  RetentionPolicy,
  SessionStartResponse,
} from "./types";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

export const api = {
  health: () => get<{ status: string }>("/health"),

  startSession: (opts?: {
    retention_policy?: Partial<RetentionPolicy>;
    prune_every?: number;
    recent_turns_to_keep?: number;
  }) => post<SessionStartResponse>("/api/session/start", opts ?? {}),

  // Wired in feat/agents-ab-endpoint.
  chatTurn: (session_id: string, message: string) =>
    post<ChatTurnResponse>("/api/chat/turn", { session_id, message }),

  runDemo: (session_id: string, scenario = "telecom_support") =>
    post<DemoRunResponse>("/api/demo/run", { session_id, scenario }),

  getReport: (session_id: string) =>
    get<{ json_log_path: string; markdown_report_path: string }>(
      `/api/report/${session_id}`,
    ),
};
