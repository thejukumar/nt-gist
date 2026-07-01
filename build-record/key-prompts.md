# Key Prompts

The important prompts that directed the build (not every tiny message).

1. **Framing** — "Build a UI-first app that compares two Nebius + Tavily support agents side by side:
   a baseline that keeps full history vs a pruned agent using context pruning… show real metrics for
   input tokens, output tokens, latency, and cost over a multi-turn support conversation."
2. **Scope discipline** — "We are stretching a bit; remember 'a small thing done well.' The pruning
   logic and the metrics are separate… capture actual stats from each Nebius call for both agents."
3. **Token counting** — "Primary: read `usage_metadata` from the Nebius/LangChain response. Fallback:
   use a tokenizer/local estimator."
4. **Branching** — "Group the branches into a max of 6 logical branches; everything branches off
   `main` and merges back."
5. **Run story** — "I need a run script to make setup easy, with a crisp README."
