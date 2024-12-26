# app.py
from flask import Flask, jsonify, request, g
import sqlite3
import os

app = Flask(__name__)

# Configuration
DATABASE = 'db.sqlite3'  # Replace with your SQLite database path
HOST = '0.0.0.0'  # This allows external connections
PORT = 5000

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This enables column access by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route to execute SELECT queries
@app.route('/query', methods=['GET'])
def execute_query():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    if not query.lower().startswith('select'):
        return jsonify({'error': 'Only SELECT queries are allowed'}), 400
    
    try:
        cur = get_db().cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return jsonify({
            'results': [dict(row) for row in rows]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to get all tables
@app.route('/tables', methods=['GET'])
def get_tables():
    try:
        cur = get_db().cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        return jsonify({
            'tables': [dict(row) for row in tables]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to get table schema
@app.route('/schema/<table_name>', methods=['GET'])
def get_schema(table_name):
    try:
        cur = get_db().cursor()
        cur.execute(f"PRAGMA table_info({table_name});")
        schema = cur.fetchall()
        return jsonify({
            'schema': [dict(row) for row in schema]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)