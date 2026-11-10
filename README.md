# agente-ia-simples

Um **agente de IA** minimalista em Python, escrito para mostrar a arquitetura de um agente e não para competir com um assistente real: o laço *decidir, usar ferramenta, observar, responder*, com ferramentas, guardas de segurança e testes.

> **Importante:** o "modelo" padrão (`RuleModel`) é uma política **determinística por regras**, sem LLM. Isso deixa o demo offline e testável, mas significa que ele não raciocina de verdade. A interface `Model.decide` foi pensada para ser trocada por um LLM (veja "Próximos passos"). As notas do corpus foram escritas para o demo.

## Como funciona

```text
pergunta -> Model.decide -> ToolCall ----> ferramenta ----> observação --+
                 ^                                                         |
                 +---------------------------------------------------------+
                 -> Final(resposta)
```

| Peça | Arquivo | O que faz |
|---|---|---|
| Recuperação BM25 | `retrieval.py` | Busca de trechos por relevância, em Python puro |
| Ferramentas | `agent.py` | `search_notes` (busca nas notas) e `calculator` (aritmética via AST, sem `eval`) |
| Laço do agente | `agent.py` | `Agent.run`, com limite de passos e registro do que foi feito |
| Modelos | `agent.py` | `RuleModel` (regras) e `ScriptedModel` (para testes) |
| Corpus de exemplo | `corpus.py` | Seis notas curtas |

## Guardas de segurança

- **Calculadora sem `eval`:** só números e operadores aritméticos; recusa chamadas de função e expoentes grandes.
- **Ferramenta inexistente ou com erro** vira uma observação (`erro: ...`) em vez de derrubar o agente.
- **Limite de passos** evita laço infinito.
- **Recusa sem evidência:** se a busca não acha nada relevante, o agente diz que não encontrou, em vez de inventar.

## Como executar

```bash
pip install -r requirements.txt
pytest          # 9 testes
python demo.py
```

Saída do demo:

```text
> O que é Simulated Annealing?
[sa-1] Simulated Annealing: Simulated Annealing é uma meta-heurística de otimização combinatória. ...
(fontes: sa-1)
  passos: ['search_notes', 'final']

> (12 + 8) * 3 / 4
Resultado: 15.0
  passos: ['calculator', 'final']

> Qual a capital da França?
Não encontrei isso nas notas, então prefiro não responder.
```

## Limitações

- O modelo por regras só distingue "conta" de "pergunta"; não faz planejamento nem encadeia ferramentas.
- O BM25 não trata sinônimos nem stemming; a recuperação é lexical.
- A resposta é o trecho recuperado, não uma síntese.
- Não há memória entre perguntas.

## Próximos passos

1. Implementar `Model.decide` com um LLM que receba as descrições das ferramentas e devolva `ToolCall` ou `Final` (a chave da API vem de variável de ambiente, nunca do código).
2. Trocar o BM25 por embeddings, ou combinar os dois.
3. Avaliar com um conjunto de perguntas com resposta esperada (acerto, citação correta, recusa correta).

## Autora

Fernanda Neiva Mesquita. [Lattes](https://lattes.cnpq.br/3639678638834402)
# agente-ia-simples
Agente de IA simples em Python: laço decidir-usar ferramenta-observar-responder, com busca BM25, calculadora segura e guardas; modelo plugável
