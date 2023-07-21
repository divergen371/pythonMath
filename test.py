# Third Party Library
from neo4j import GraphDatabase

url = "bolt://localhost:7687"
username = "neo4j"
password = "hogehoge"

mutation = """
MERGE (src:Package {name: $src})
MERGE (dest:Package {name: $dest})
MERGE (src)-[:PDEPENDS]->(dest)
"""

db = GraphDatabase.driver(url, auth=(username, password))
with db.session() as session:
    session.run(mutation, src="foo", dest="bar")
    session.run(mutation, src="bar", dest="baz")
    session.run(mutation, src="baz", dest="qux")
    session.run(mutation, src="bar", dest="foo")
    session.run(mutation, src="foo", dest="baz")
