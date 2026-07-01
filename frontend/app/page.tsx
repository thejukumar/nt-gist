import { AgentComparisonGrid } from "@/components/agent-comparison-grid";
import { ChatInput } from "@/components/chat-input";
import { ComparisonSavingsStrip } from "@/components/comparison-savings-strip";
import { Header } from "@/components/header";

// Scaffold placeholder: renders the intended split-screen layout with static
// panels. Live metrics, demo automation, and the retention modal land in
// feat/frontend (branch 5).
export default function Home() {
  return (
    <main className="mx-auto max-w-6xl p-4 md:p-8">
      <Header />
      <AgentComparisonGrid />
      <ComparisonSavingsStrip />
      <ChatInput />
      <p className="mt-6 text-center text-xs text-white/40">
        Scaffold shell — interactivity wired in <code>feat/frontend</code>.
      </p>
    </main>
  );
}
