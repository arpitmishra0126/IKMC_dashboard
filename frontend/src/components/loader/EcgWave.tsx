/**
 * Lightweight CSS/SVG heartbeat (ECG) waveform - no animation library.
 * A single waveform unit is drawn twice side by side inside a viewBox-clipped
 * svg; a CSS animation scrolls the pair left by exactly one unit width, so
 * the loop is seamless and continuous.
 */
const UNIT_WIDTH = 240
const WAVEFORM =
  "M0,40 L22,40 L28,40 L32,22 L36,55 L40,8 L44,66 L48,40 L54,40 L64,40 " +
  "L70,34 L76,46 L82,40 L110,40 L120,40"

export function EcgWave() {
  return (
    <svg
      className="ecg-wave"
      viewBox={`0 0 ${UNIT_WIDTH} 80`}
      preserveAspectRatio="none"
      role="img"
      aria-label="Monitoring system initializing"
    >
      <g className="ecg-wave-track">
        <path d={WAVEFORM} />
        <path d={WAVEFORM} transform={`translate(${UNIT_WIDTH}, 0)`} />
      </g>
    </svg>
  )
}
