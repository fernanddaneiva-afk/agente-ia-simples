"""Agente de IA simples: laço decidir -> usar ferramenta -> observar -> responder.

O "modelo" é plugável (interface Model.decide). Aqui há dois: RuleModel, determinístico
e offline (usado nos testes e no demo), e ScriptedModel, que reproduz uma sequência
fixa de decisões. Para usar um LLM de verdade, implemente Model.decide chamando a API
do provedor com as descrições das ferramentas.
"""
import ast
import operator
import re
from dataclasses import dataclass, field
from typing import Callable

from corpus import NOTES
from retrieval import BM25


# ----------------------------------------------------------------- mensagens
@dataclass
class ToolCall:
    name: str
    args: dict


@dataclass
class Final:
    answer: str


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable


# ----------------------------------------------------------------- ferramentas
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.Mod: operator.mod}


def safe_eval(expr):
    """Calculadora segura: só números e operadores aritméticos (sem eval)."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            if isinstance(node.op, ast.Pow) and abs(ev(node.right)) > 100:
                raise ValueError("expoente grande demais")
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError("expressão não permitida")
    return ev(ast.parse(expr, mode="eval").body)


def make_tools(index):
    def calculator(expression):
        return str(safe_eval(expression))

    def search_notes(query):
        hits = index.search(query, k=2)
        if not hits:
            return "nenhum trecho relevante"
        return "\n".join(f"[{h['id']}] {h['title']}: {h['text']}" for h in hits)

    return {
        "calculator": Tool("calculator", "Avalia uma expressão aritmética.", calculator),
        "search_notes": Tool("search_notes", "Busca trechos nas notas.", search_notes),
    }


# ----------------------------------------------------------------- modelos
class RuleModel:
    """Política determinística: aritmética -> calculadora; senão -> busca e resposta
    citando as fontes recuperadas."""

    EXPR = re.compile(r"(?:quanto é|calcule|calcular)?\s*([-+*/%().\d\s^]+)\s*\??$", re.I)

    def decide(self, question, observations):
        if not observations:
            m = self.EXPR.search(question.strip())
            expr = m.group(1).replace("^", "**").strip() if m else ""
            if expr and any(c.isdigit() for c in expr) and re.search(r"[-+*/%]", expr):
                return ToolCall("calculator", {"expression": expr})
            return ToolCall("search_notes", {"query": question})
        name, result = observations[-1]
        if name == "calculator":
            return Final(f"Resultado: {result}")
        if result == "nenhum trecho relevante":
            return Final("Não encontrei isso nas notas, então prefiro não responder.")
        first = result.splitlines()[0]
        ids = ", ".join(re.findall(r"^\[([^\]]+)\]", result, re.M))
        return Final(f"{first}\n(fontes: {ids})")


class ScriptedModel:
    def __init__(self, decisions):
        self.decisions = list(decisions)

    def decide(self, question, observations):
        return self.decisions.pop(0)


# ----------------------------------------------------------------- agente
@dataclass
class Agent:
    model: object
    tools: dict
    max_steps: int = 4
    trace: list = field(default_factory=list)

    def run(self, question):
        observations = []
        for step in range(self.max_steps):
            decision = self.model.decide(question, observations)
            if isinstance(decision, Final):
                self.trace.append(("final", decision.answer))
                return decision.answer
            tool = self.tools.get(decision.name)
            if tool is None:                      # guarda: ferramenta inexistente
                result = f"erro: ferramenta desconhecida '{decision.name}'"
            else:
                try:
                    result = tool.fn(**decision.args)
                except Exception as exc:          # guarda: falha vira observação
                    result = f"erro: {exc}"
            self.trace.append((decision.name, decision.args, result))
            observations.append((decision.name, result))
        return "Não consegui concluir dentro do limite de passos."


def default_agent():
    return Agent(RuleModel(), make_tools(BM25(NOTES)))
