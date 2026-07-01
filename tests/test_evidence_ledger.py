"""EvidenceLedger dedup + rendering, and SupportMemory serialization."""

from support_context_budget_lab.pruning.evidence_ledger import EvidenceItem, EvidenceLedger
from support_context_budget_lab.pruning.support_memory import SupportMemory


def _item(url, turn, claim="claim"):
    return EvidenceItem(
        source_id=f"src_{url[-1]}",
        title="Title",
        url=url,
        snippet="snippet",
        relevant_claim=claim,
        first_seen_turn=turn,
        last_used_turn=turn,
    )


def test_upsert_dedupes_by_url():
    ledger = EvidenceLedger()
    ledger.upsert(_item("http://a", 1))
    ledger.upsert(_item("http://a", 5, claim="updated"))  # same url -> merge
    ledger.upsert(_item("http://b", 2))
    assert len(ledger.items) == 2
    a = next(i for i in ledger.items if i.url == "http://a")
    assert a.last_used_turn == 5
    assert a.relevant_claim == "updated"


def test_ledger_prompt_block_empty_and_populated():
    assert "empty" in EvidenceLedger().to_prompt_block().lower()
    ledger = EvidenceLedger()
    ledger.upsert(_item("http://a", 1))
    block = ledger.to_prompt_block()
    assert "Evidence ledger:" in block and "http://a" in block


def test_support_memory_prompt_block():
    assert "none captured" in SupportMemory().to_prompt_block().lower()
    mem = SupportMemory(
        customer_issue="internet drops",
        troubleshooting_steps=["restarted router"],
    )
    block = mem.to_prompt_block()
    assert "internet drops" in block
    assert "restarted router" in block
