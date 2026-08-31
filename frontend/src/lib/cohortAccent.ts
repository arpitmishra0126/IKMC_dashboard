/**
 * Shared color accent tokens for Inborn vs. Outborn, reused by the
 * Overview cohort cards and the Outborn page (whose NVD/C-section cards
 * are both still "Outborn", so sharing the same teal accent stays
 * accurate). Not applied to MSNCU/PNC on the Inborn page, since those are
 * both sub-units of Inborn - reusing this map there would misleadingly
 * imply one of them belongs to a different cohort.
 */
export type CohortAccent = "inborn" | "outborn"

export const COHORT_ACCENT_STYLES: Record<
  CohortAccent,
  { border: string; badge: string; icon: string }
> = {
  inborn: {
    border: "border-l-primary",
    badge: "bg-primary/10 text-primary border-primary/20",
    icon: "text-primary",
  },
  outborn: {
    border: "border-l-teal-600 dark:border-l-teal-400",
    badge:
      "bg-teal-600/10 text-teal-700 border-teal-600/20 dark:text-teal-300 dark:bg-teal-400/10 dark:border-teal-400/20",
    icon: "text-teal-700 dark:text-teal-300",
  },
}
