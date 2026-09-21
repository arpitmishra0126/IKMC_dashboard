/**
 * One function per FastAPI endpoint currently consumed by the frontend.
 * Endpoint paths and payload shapes are the source of truth defined in
 * backend/app/api/*.py and backend/app/schemas/*.py - nothing here
 * reimplements or reshapes what the backend returns.
 */
import { apiGet, apiPost } from "@/services/apiClient"
import type { AttachmentCasesResponse, AttachmentScope } from "@/types/attachmentCases"
import type { CohortsResponse } from "@/types/cohorts"
import type { DataQualityResponse } from "@/types/dataQuality"
import type { DischargeResponse } from "@/types/discharge"
import type { HealthResponse } from "@/types/health"
import type { InbornResponse } from "@/types/inborn"
import type { RefreshResponse, SyncMetadataResponse } from "@/types/meta"
import type { OutbornResponse } from "@/types/outborn"
import type { OverviewDateRange, OverviewPeriod, OverviewResponse } from "@/types/overview"
import type { ValidationDetailResponse } from "@/types/validation"

export function getHealth(signal?: AbortSignal): Promise<HealthResponse> {
  return apiGet<HealthResponse>("/api/health", signal)
}

export function getSyncMetadata(signal?: AbortSignal): Promise<SyncMetadataResponse> {
  return apiGet<SyncMetadataResponse>("/api/meta/sync", signal)
}

export function refreshData(signal?: AbortSignal): Promise<RefreshResponse> {
  return apiPost<RefreshResponse>("/api/meta/refresh", signal)
}

export function getOverview(
  period: OverviewPeriod = "all",
  customRange?: OverviewDateRange,
  signal?: AbortSignal
): Promise<OverviewResponse> {
  if (customRange) {
    const params = new URLSearchParams({ from_date: customRange.from, to_date: customRange.to })
    return apiGet<OverviewResponse>(`/api/dashboard/overview?${params.toString()}`, signal)
  }
  const query = period === "all" ? "" : `?period=${period}`
  return apiGet<OverviewResponse>(`/api/dashboard/overview${query}`, signal)
}

export function getCohorts(signal?: AbortSignal): Promise<CohortsResponse> {
  return apiGet<CohortsResponse>("/api/dashboard/cohorts", signal)
}

export function getDataQuality(signal?: AbortSignal): Promise<DataQualityResponse> {
  return apiGet<DataQualityResponse>("/api/dashboard/data-quality", signal)
}

export function getInborn(signal?: AbortSignal): Promise<InbornResponse> {
  return apiGet<InbornResponse>("/api/dashboard/inborn", signal)
}

export function getOutborn(signal?: AbortSignal): Promise<OutbornResponse> {
  return apiGet<OutbornResponse>("/api/dashboard/outborn", signal)
}

export function getDischarge(signal?: AbortSignal): Promise<DischargeResponse> {
  return apiGet<DischargeResponse>("/api/dashboard/discharge", signal)
}

export function getAttachmentCases(
  scope: AttachmentScope,
  period: OverviewPeriod = "all",
  customRange?: OverviewDateRange,
  signal?: AbortSignal
): Promise<AttachmentCasesResponse> {
  const params = new URLSearchParams({ scope })
  if (customRange) {
    params.set("from_date", customRange.from)
    params.set("to_date", customRange.to)
  } else if (period !== "all") {
    params.set("period", period)
  }
  return apiGet<AttachmentCasesResponse>(`/api/dashboard/attachment-cases?${params.toString()}`, signal)
}

export function getValidationDetail(
  check: string,
  signal?: AbortSignal
): Promise<ValidationDetailResponse> {
  return apiGet<ValidationDetailResponse>(`/api/validation/${check}`, signal)
}
