from datetime import datetime
import hashlib


class Block:
    def __init__(
        self, index: int, timestamp: datetime, data: str, previous_hash: str
    ) -> None:
        self.index: int = index
        self.timestamp: datetime = timestamp
        self.data: str = data
        self.previous_hash: str = previous_hash
        self.hash: str = self.hashblock()

    def hashblock(self) -> str:
        sha = hashlib.sha256()
        sha.update(
            (
                str(self.index)
                + str(self.timestamp)
                + str(self.data)
                + str(self.previous_hash)
            ).encode("utf-8")
        )
        return sha.hexdigest()
