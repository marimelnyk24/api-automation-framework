from dataclasses import dataclass

@dataclass
class Comment:
    postId: int
    id: int
    name: str
    email: str
    body: str