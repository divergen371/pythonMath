from snakecoin_block import Block
import datetime



def next_block(last_block: Block) -> Block:
    this_index: int = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_data: str = "Hey! I', block" + str(this_index)
    previous_hash: str = last_block.hash
    return Block(
        index=this_index,
        timestamp=this_timestamp,
        data=this_data,
        previous_hash=previous_hash,
    )
