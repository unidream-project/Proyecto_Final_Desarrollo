def to_pgvector(vec: list[float]) -> str:
    return "[" + ",".join(str(x) for x in vec) + "]"
