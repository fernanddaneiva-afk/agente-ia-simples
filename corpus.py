"""Notas curtas escritas para o demo (texto próprio, sem fontes externas)."""

NOTES = [
    {"id": "sa-1", "title": "Simulated Annealing",
     "text": "Simulated Annealing é uma meta-heurística de otimização combinatória. "
             "A cada iteração gera-se uma solução vizinha por uma perturbação. Se ela "
             "melhora o objetivo, é aceita. Se piora, é aceita com probabilidade "
             "exp(-delta/T), que diminui conforme a temperatura T é resfriada."},
    {"id": "sa-2", "title": "Escalonamento em máquinas paralelas",
     "text": "No problema de máquinas paralelas com datas de liberação e tempos de setup, "
             "o objetivo é minimizar o makespan, o instante em que a última tarefa "
             "termina. O setup pode ser antecipado, começando antes da liberação da "
             "tarefa. Limitantes inferiores avaliam a qualidade das soluções."},
    {"id": "role-1", "title": "Atribuição de papéis em grafos",
     "text": "Uma r-atribuição de papéis de um grafo associa r papéis aos vértices de "
             "modo que dois vértices com o mesmo papel tenham o mesmo conjunto de papéis "
             "na vizinhança. Em redes sociais, vértices com o mesmo papel têm funções "
             "equivalentes. O problema é NP-completo para o produto Cartesiano com r >= 3."},
    {"id": "role-2", "title": "Prisma complementar",
     "text": "O prisma complementar de um grafo G liga G ao seu complemento por um "
             "emparelhamento perfeito. Ele é sempre conexo. Admite 2-atribuição de papéis "
             "exceto para o caminho de três vértices e o seu complemento."},
    {"id": "bio-1", "title": "Bioacústica de abelhas",
     "text": "Abelhas polinizadoras podem ser identificadas pelo som do voo e da "
             "vibração em flores. Modelos de aprendizado profundo sobre espectrogramas "
             "classificam espécies ou funções ecológicas, como polinizadora efetiva "
             "ou apenas coletora de néctar."},
    {"id": "fair-1", "title": "Equidade em reconhecimento facial",
     "text": "Em verificação facial, medem-se a taxa de falsa aceitação (FMR) e a de "
             "falsa rejeição (FNMR) por grupo demográfico. Com um único limiar global, "
             "os grupos podem ter FNMR muito diferentes mesmo com FMR estável, o que "
             "indica viés do sistema."},
]
