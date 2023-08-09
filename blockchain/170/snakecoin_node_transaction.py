from snakecoin_block import Block
from snakecoin_genesis import create_genesis_block
from flask import Flask, request, jsonify
import datetime
import json
import requests

# ブロックチェーンを定義
blockchain = []
blockchain.append(create_genesis_block())

# トランザクションリスト
# このノード内のトランザクションが格納される
this_nodes_tx = []

# ブロックチェーンネットワーク上のノードURLリスト
# TODO: 新しいノードを検出する仕組みを作る
peer_nodes = []

# とりあえずマイナーのアドレスは固定
# TODO: ノードごとに一意に生成して設定する仕組みを作る
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"


# Proof of Work アルゴリズム
# BitCoinなどでは計算量の多い特定条件のハッシュ値探索だが
# ここでは簡略化するために
#   「処理※回数が9で割り切れる」 AND 「前回の結果で割り切れる」
#   ※今回はただのインクリメント
# を発見することとしている。
# ただし、この状態だと発見処理をサーバーが実行しているため
# 処理が分散されず、ブロックチェーンの分岐も起きやすい状態になる。
# TODO: 計算量が多い部分はクライアント側で実装する想定で、サーバー側では確認処理のみが実装されている状態にする
def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


# 各ノードが保持するブロックチェーン情報を取得する
def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.reloads(block)
        other_chains.append(block)
    return other_chains


# 新しいブロックを繋げる末端を探す
def consensus():
    global blockchain
    longest_chain = blockchain
    # 他のノードが保持するブロックチェーン情報を取得
    other_chains = find_new_chains()
    # 最長のブロックチェーンを探索して、最長のブロックチェーンを採用する。
    # なお現状の配列によるブロックチェーン実装だと分岐したブロックチェーンの短い枝の情報がロストする。
    # TODO: 有向グラフのような実装で分岐した枝を保持しつつ、採用のブロックチェーンを採用するのではなく最長の末端を採用するロジックに変更
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain


#### endpoints

node = Flask(__name__)


# snakecoinの受け渡しトランザクションを登録する
@node.route("/transactions", methods=["POST"])
def transactions():
    if request.method == "POST":
        # POSTされたトランザクションデータをトランザクションリストに追加
        new_tx = request.get_json()
        this_nodes_tx.append(new_tx)

        # 追加したトランザクションデータを標準出力
        print("New Transaction")
        print("FROM: {}".format(new_tx["from"]))
        print("TO: {}".format(new_tx["to"]))
        print("AMOUNT: {}".format(new_tx["amount"]))

        return jsonify({"message": "Transaction submission successful"}), 200


# 受け渡しトランザクションをブロック化し、ブロックチェーンにつなげる
@node.route("/mines", methods=["POST"])
def mines():
    # コンセンサスをとる
    consensus()

    # 最後のproofを取得する
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data["proof-of-work"]

    # マイニングする
    # TODO: 新しいproofをパラメータで受け取って適合性判定のみ行うようにする
    proof = proof_of_work(last_proof)

    # マイナーに報酬として 1 snakecoin を付与するトランザクションを追加
    this_nodes_tx.append({"from": "network", "to": miner_address, "amount": 1})

    # 新しいブロックに必要な値の用意
    # ここでトランザクションリストをブロックに格納している
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = datetime.datetime.now()
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_tx),
    }
    last_block_hash = last_block.hash

    # 新しいブロックを生成し、ブロックチェーンに追加
    mined_block = Block(
        new_block_index, new_block_timestamp, new_block_data, last_block_hash
    )
    blockchain.append(mined_block)

    # トランザクションリストを初期化
    this_nodes_tx[:] = []

    return jsonify(
        {
            "index": new_block_index,
            "timestamp": new_block_timestamp,
            "data": new_block_data,
            "hash": last_block_hash,
        }
    )


# このノードが保持するブロックチェーン情報を参照する
@node.route("/blocks", methods=["GET"])
def get_blocks():
    chain_to_send = blockchain[:]
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        # Blockクラスのプロパティを文字列化
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        # JSON文字列化できるように辞書型に変換
        chain_to_send[i] = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash,
        }
    # JSON文字列に変換してクライアントに返す
    return jsonify(chain_to_send)


node.run()
