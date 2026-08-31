/**
 * Thin fetch wrapper for the FastAPI backend (backend/app/main.py).
 *
 * This is intentionally dumb: it sends requests and parses JSON. It never
 * computes, derives, or reformats a business value - every field returned
 * by `get<T>()` is exactly what the backend responded with, typed against
 * backend/app/schemas/*.py.
 */

export const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8000"

export class ApiError extends Error {
  status: number
  detail: string

  constructor(status: number, detail: string) {
    super(detail)
    this.name = "ApiError"
    this.status = status
    this.detail = detail
  }
}

async function parseErrorDetail(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown }
    if (typeof body.detail === "string") return body.detail
    if (body.detail) return JSON.stringify(body.detail)
  } catch {
    // response body wasn't JSON - fall through to generic message
  }
  return `Request failed with status ${response.status}`
}

export async function apiGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { signal })
  } catch {
    throw new ApiError(0, "Could not reach the API server.")
  }

  if (!response.ok) {
    throw new ApiError(response.status, await parseErrorDetail(response))
  }

  return (await response.json()) as T
}

export async function apiPost<T>(path: string, signal?: AbortSignal): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { method: "POST", signal })
  } catch {
    throw new ApiError(0, "Could not reach the API server.")
  }

  if (!response.ok) {
    throw new ApiError(response.status, await parseErrorDetail(response))
  }

  return (await response.json()) as T
}
