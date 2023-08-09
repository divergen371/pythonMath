from snakecoin_block import Block
import datetime


def create_genesis_block() -> Block:
    return Block(
        index=0,
        timestamp=datetime.datetime.now(),
        data={"message": "Genesis Block", "proof-of-work": 9},
        previous_hash="0",
    )
