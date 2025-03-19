from flask import Flask, request, jsonify
from auth import app as auth_app, token_required
import jwt
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS funds (
                            id INTEGER PRIMARY KEY,
                            amount TEXT,
                            description TEXT
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS payouts (
                            id INTEGER PRIMARY KEY,
                            amount TEXT,
                            admin TEXT
                        )''')
        conn.commit()

init_db()

@app.route('/funds', methods=['GET'])
@token_required
def get_funds(current_user):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funds')
        funds = cursor.fetchall()
    return jsonify(funds)

@app.route('/withdraw', methods=['POST'])
@token_required
def withdraw(current_user):
    data = request.get_json()
    amount = data.get('amount')
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO payouts (amount, admin) VALUES (?, ?)', (amount, current_user))
        conn.commit()
    return jsonify({'message': 'Withdrawal successful'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
