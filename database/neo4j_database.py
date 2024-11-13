from neo4j import GraphDatabase
import config  # Import your configuration

class Neo4jDatabase:
    def __init__(self):
        self.driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    
    def close(self):
        self.driver.close()

    def query_resources(self, topic_name):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Resource)
                WHERE r.name CONTAINS $topic_name
                RETURN r.name AS name, r.link AS link
            """, topic_name=topic_name)
            return [{"name": record["name"], "link": record["link"]} for record in result]
