"""Pure helpers of the provider clients (no network / no keys required)."""

import pytest

from support_context_budget_lab.llm.nebius_client import _extract_text
from support_context_budget_lab.tools.tavily_client import _normalize_results


class _Msg:
    def __init__(self, content):
        self.content = content


def test_extract_text_from_string():
    assert _extract_text(_Msg("hello")) == "hello"


def test_extract_text_from_block_list():
    blocks = [{"type": "text", "text": "part1 "}, {"type": "text", "text": "part2"}]
    assert _extract_text(_Msg(blocks)) == "part1 part2"


def test_normalize_results_from_dict():
    raw = {
        "results": [
            {"title": "T1", "url": "http://a", "content": "  some   text  "},
            {"title": "T2", "url": "http://b", "content": "more"},
        ]
    }
    records = _normalize_results(raw)
    assert [r.title for r in records] == ["T1", "T2"]
    assert records[0].snippet == "some text"  # whitespace collapsed


def test_normalize_results_from_json_string():
    raw = '{"results": [{"title": "X", "url": "http://x", "content": "hi"}]}'
    records = _normalize_results(raw)
    assert len(records) == 1 and records[0].url == "http://x"


def test_normalize_results_bad_input_is_empty():
    assert _normalize_results("not json") == []
    assert _normalize_results(None) == []


def test_to_lc_messages_maps_roles():
    pytest.importorskip("langchain_core")
    from support_context_budget_lab.llm.nebius_client import _to_lc_messages
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    msgs = _to_lc_messages(
        [
            {"role": "system", "content": "s"},
            {"role": "user", "content": "u"},
            {"role": "assistant", "content": "a"},
        ]
    )
    assert isinstance(msgs[0], SystemMessage)
    assert isinstance(msgs[1], HumanMessage)
    assert isinstance(msgs[2], AIMessage)
