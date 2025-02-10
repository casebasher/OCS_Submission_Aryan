from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    userid = data.get('userid')
    password_hash = data.get('password_hash')

    response = supabase.table('users').select("*").eq('userid', userid).execute()
    
    if not response.data:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    user = response.data[0]
    if user['password_hash'] != password_hash:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    if user['role'] == 'admin':
        all_users = supabase.table('users').select("userid, role").execute()
        return jsonify({
            'success': True,
            'role': 'admin',
            'data': all_users.data
        })
    else:
        return jsonify({
            'success': True,
            'role': 'user',
            'data': [{'userid': userid, 'role': user['role']}]
        })

if __name__ == '__main__':
    app.run(debug=True)
