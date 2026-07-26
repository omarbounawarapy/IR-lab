from dataclasses import dataclass

@dataclass
class Token:
    def __init__(
        self,
        content: str,
        start_offset: int | None = None,
        end_offset: int | None = None,
        position: int | None = None,
        payload: dict | None = None,
    ):
        self.content = content
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.position = position
        self.payload = payload or {}


    def __repr__(self):
        return (
            f"Token("
            f"content={self.content!r}, "
            f"position={self.position!r}, "
            f"start_offset={self.start_offset!r}, "
            f"end_offset={self.end_offset!r}, "
            f"payload={self.payload!r}"
            f")"
        )