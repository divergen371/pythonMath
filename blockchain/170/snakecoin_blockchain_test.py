from snakecoin_genesis import create_genesis_block
from snakecoin_next_block import next_block

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

num_of_blocks_to_add = 3
print(
    "Block #{} has been added to the blockchain".format(previous_block.index)
)
print("Data: {}".format(previous_block.data))
print("PrHh: {}".format(previous_block.previous_hash))
print("Hash: {}\n".format(previous_block.hash))

for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)

    print(
        "Block #{} has been added to the blockchain".format(block_to_add.index)
    )
    print("Data: {}".format(block_to_add.data))
    print("PrHh: {}".format(block_to_add.previous_hash))
    print("Hash: {}\n".format(block_to_add.hash))

    previous_block = block_to_add
