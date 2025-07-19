import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("OPENAI_API_KEY", "test-key")
import types
import pytest

import typewhat

class FakeResponse:
    def __init__(self, content: str):
        self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=content))]

def test_generate_typos(monkeypatch):
    def fake_create(model, messages, max_tokens, temperature, timeout):
        return FakeResponse("typo1\ntypo2")

    monkeypatch.setattr(typewhat.openai.chat.completions, "create", fake_create)
    typos = typewhat.generate_typos("example.com", 2)
    assert typos == ["typo1", "typo2"]

def test_check_domain_registered_true(monkeypatch):
    def fake_resolve(domain, rtype):
        return ["record"]

    monkeypatch.setattr(typewhat.dns.resolver, "resolve", fake_resolve)
    assert typewhat.check_domain_registered("example.com", "A")

def test_check_domain_registered_false(monkeypatch):
    def fake_resolve(domain, rtype):
        raise typewhat.dns.resolver.NXDOMAIN

    monkeypatch.setattr(typewhat.dns.resolver, "resolve", fake_resolve)
    assert not typewhat.check_domain_registered("bad.example", "A")

def test_get_whois_entity(monkeypatch):
    def fake_whois(domain):
        return {"org": "Example Inc"}

    monkeypatch.setattr(typewhat.whois, "whois", fake_whois)
    assert typewhat.get_whois_entity("example.com") == "Example Inc"

def test_get_whois_entity_none(monkeypatch):
    def fake_whois(domain):
        return {}

    monkeypatch.setattr(typewhat.whois, "whois", fake_whois)
    assert typewhat.get_whois_entity("example.com") is None
