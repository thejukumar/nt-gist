// Display formatters for metrics.

export const formatTokens = (n: number): string => n.toLocaleString("en-US");

export const formatCost = (usd: number): string =>
  `$${usd.toFixed(usd < 0.01 ? 5 : 4)}`;

export const formatLatency = (seconds: number): string => `${seconds.toFixed(1)}s`;

export const formatPercent = (fraction: number): string =>
  `${(fraction * 100).toFixed(1)}%`;
