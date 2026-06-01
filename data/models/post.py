from dataclasses import dataclass

@dataclass
class Post:
    userId: int
    id: int | None
    title: str
    body: str