"""Context-pruning engine (reusable, decoupled from metrics).

Components:
- RetentionPolicy: what the pruned agent must always retain.
- SupportMemory: durable support state that survives pruning.
- EvidenceLedger / EvidenceItem: compact Tavily evidence instead of raw blobs.
- ContextPruner: builds the compact context sent to the pruned agent.
"""

from .evidence_ledger import EvidenceItem, EvidenceLedger
from .retention_policy import RetentionPolicy
from .support_memory import SupportMemory

__all__ = ["RetentionPolicy", "SupportMemory", "EvidenceItem", "EvidenceLedger"]
