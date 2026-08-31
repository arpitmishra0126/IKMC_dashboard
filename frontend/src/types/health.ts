/** Mirrors the GET /api/health response in backend/app/main.py. */
export interface HealthResponse {
  status: string
  app: string
  env: string
}
