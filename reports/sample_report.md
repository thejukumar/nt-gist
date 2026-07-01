# Support Context Budget Lab Report

_Generated 2026-07-01T05:35:44.224649+00:00 · session `session_635224d4`_

## Customer Scenario
Enterprise support chatbot with 100,000+ users, 10,000+ monthly support conversations, and an average of ~15 turns per conversation.

## Experiment Setup
- LLM provider: Nebius (`moonshotai/Kimi-K2.6`)
- Web tool: Tavily
- Baseline: full-history context
- Optimized: pruning-aware support memory + evidence ledger
- Pruning frequency: every 2 turns
- Recent turns retained: 2
- Turns in this session: 15

## Results Summary
- Baseline total input tokens: 9,140
- Pruned total input tokens: 5,113
- Input-token reduction: 44.1%
- Baseline estimated cost: $0.0067
- Pruned estimated cost: $0.0043
- Estimated cost savings: $0.0024 (36.2%)
- Avg latency — baseline 1.72s vs pruned 1.67s

## Turn-by-Turn Metrics
| Turn | Baseline in | Pruned in | Baseline cost | Pruned cost | Pruned |
|-----:|------------:|----------:|--------------:|------------:|:------:|
| 1 | 94 | 207 | $0.0001 | $0.0002 |  |
| 2 | 142 | 256 | $0.0002 | $0.0002 |  |
| 3 | 193 | 288 | $0.0002 | $0.0003 |  |
| 4 | 320 | 367 | $0.0003 | $0.0003 | ✂️ |
| 5 | 456 | 371 | $0.0004 | $0.0003 |  |
| 6 | 589 | 375 | $0.0004 | $0.0003 | ✂️ |
| 7 | 636 | 368 | $0.0005 | $0.0003 |  |
| 8 | 685 | 366 | $0.0005 | $0.0003 | ✂️ |
| 9 | 728 | 362 | $0.0005 | $0.0003 |  |
| 10 | 771 | 355 | $0.0005 | $0.0003 | ✂️ |
| 11 | 813 | 355 | $0.0006 | $0.0003 |  |
| 12 | 858 | 357 | $0.0006 | $0.0003 | ✂️ |
| 13 | 907 | 364 | $0.0006 | $0.0003 |  |
| 14 | 950 | 361 | $0.0006 | $0.0003 | ✂️ |
| 15 | 998 | 361 | $0.0007 | $0.0003 |  |

## Pruning Timeline
- Turn 4: compressed 3 message(s); preserved customer issue, support memory, 2 evidence source(s)
- Turn 6: compressed 7 message(s); preserved customer issue, support memory, 2 evidence source(s)
- Turn 8: compressed 11 message(s); preserved customer issue, support memory, 2 evidence source(s)
- Turn 10: compressed 15 message(s); preserved customer issue, support memory, 2 evidence source(s)
- Turn 12: compressed 19 message(s); preserved customer issue, support memory, 2 evidence source(s)
- Turn 14: compressed 23 message(s); preserved customer issue, support memory, 2 evidence source(s)

## Business Projection
Scaling this conversation's savings across 10,000 monthly conversations (~15 turns each):
- Input tokens saved / month: ~40,270,000
- Estimated cost saved / month: ~$24.1620

## Limitations
- Cost is estimated from configurable pricing, not an actual bill.
- Answer accuracy is not scored in the MVP.
- Token usage is measured from provider metadata when available; otherwise estimated.
- Pruning wins on long conversations; short chats may favor the baseline due to the pruned agent's fixed retention overhead.