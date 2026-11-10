"""Recuperação de trechos com BM25, em Python puro (sem dependências)."""
import math
import re
from collections import Counter

STOP = {"a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "um", "uma",
        "que", "para", "por", "com", "se", "é", "no", "na", "nos", "nas", "ao", "como",
        "the", "of", "and", "to", "in", "is", "what", "qual", "quais", "sobre"}


def tokenize(text):
    return [t for t in re.findall(r"\w+", text.lower()) if t not in STOP]


class BM25:
    def __init__(self, chunks, k1=1.5, b=0.75):
        """chunks: lista de dicts {"id": str, "text": str, ...}."""
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.tf = [Counter(tokenize(c["text"])) for c in chunks]
        self.len = [sum(t.values()) for t in self.tf]
        self.avg = sum(self.len) / max(len(chunks), 1)
        df = Counter(w for t in self.tf for w in t)
        n = len(chunks)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def score(self, query, i):
        s = 0.0
        for w in tokenize(query):
            f = self.tf[i].get(w, 0)
            if f:
                denom = f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg)
                s += self.idf[w] * f * (self.k1 + 1) / denom
        return s

    def search(self, query, k=3):
        ranked = sorted(((self.score(query, i), i) for i in range(len(self.chunks))),
                        reverse=True)
        return [dict(self.chunks[i], score=round(s, 3)) for s, i in ranked[:k] if s > 0]
