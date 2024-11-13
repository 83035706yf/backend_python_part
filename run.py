from app import create_app

app = create_app()

@app.teardown_appcontext
def close_neo4j_db(exception):
    app.neo4j_db.close()  # Close Neo4j database connection when app context ends

if __name__ == '__main__':
    app.run(port=5086)
