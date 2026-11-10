import pytest

from agent import (Agent, Final, ScriptedModel, ToolCall, default_agent, make_tools,
                   safe_eval)
from corpus import NOTES
from retrieval import BM25


def test_busca_recupera_nota_certa():
    top = BM25(NOTES).search("meta-heurística temperatura resfriamento", k=1)[0]
    assert top["id"] == "sa-1"


def test_busca_sem_resultado():
    assert BM25(NOTES).search("xyzzy qwerty") == []


def test_calculadora_segura():
    assert safe_eval("(12 + 8) * 3 / 4") == 15
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('ls')")


def test_calculadora_rejeita_expoente_enorme():
    with pytest.raises(ValueError):
        safe_eval("9 ** 9999")


def test_agente_responde_com_fonte():
    ans = default_agent().run("O que é Simulated Annealing?")
    assert "sa-1" in ans


def test_agente_usa_calculadora():
    agent = default_agent()
    assert agent.run("(12 + 8) * 3 / 4") == "Resultado: 15.0"
    assert agent.trace[0][0] == "calculator"


def test_agente_recusa_sem_evidencia():
    ans = default_agent().run("Qual a capital da França?")
    assert "Não encontrei" in ans


def test_ferramenta_desconhecida_vira_observacao():
    tools = make_tools(BM25(NOTES))
    model = ScriptedModel([ToolCall("rm_rf", {}), Final("ok")])
    agent = Agent(model, tools)
    assert agent.run("x") == "ok"
    assert "desconhecida" in agent.trace[0][2]


def test_limite_de_passos():
    tools = make_tools(BM25(NOTES))
    model = ScriptedModel([ToolCall("search_notes", {"query": "abelha"})] * 10)
    agent = Agent(model, tools, max_steps=3)
    assert "limite" in agent.run("x")
    assert len(agent.trace) == 3
