from agent import default_agent

QUESTIONS = [
    "O que é Simulated Annealing?",
    "Como medir viés em reconhecimento facial?",
    "(12 + 8) * 3 / 4",
    "Qual a capital da França?",
]

if __name__ == "__main__":
    for q in QUESTIONS:
        agent = default_agent()
        print(f"> {q}")
        print(agent.run(q))
        print("  passos:", [t[0] for t in agent.trace], "\n")
