"use client";

import type { PruningEventView } from "@/lib/types";

// Shows when pruning happened and what was preserved.
export function PruningTimeline({
  events,
}: {
  events: { turn: number; event: PruningEventView }[];
}) {
  if (events.length === 0) return null;

  return (
    <div className="glass mt-4 p-4">
      <div className="mb-2 text-[10px] uppercase tracking-wide text-white/40">Pruning timeline</div>
      <ol className="space-y-2">
        {events.map(({ turn, event }) => (
          <li key={turn} className="border-l-2 border-pruned/50 pl-3 text-sm">
            <span className="font-mono text-pruned">Turn {turn}</span>
            <span className="text-white/60">
              {" "}
              — compressed {event.compressed_messages} message(s)
              {event.preserved.length ? `; preserved ${event.preserved.join(", ")}` : ""}
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
