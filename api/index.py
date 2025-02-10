from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase configuration
url: str = "https://hwuzklwcarlsjcyuhulv.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh3dXprbHdjYXJsc2pjeXVodWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkyMDQ4MTEsImV4cCI6MjA1NDc4MDgxMX0.XdcIM_6-mmBQa48g0MlHfBckHDG0g4LzMYu01e3y6VA"
supabase: Client = create_client(url, key)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    userid = data.get('userid')
    password_hash = data.get('password_hash')

    try:
        response = supabase.table('users').select('*').eq('userid', userid).execute()
        
        if not response.data:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        user = response.data[0]
        if user['password_hash'] != password_hash:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        if user['role'] == 'admin':
            all_users = supabase.table('users').select('userid, role').execute()
            return jsonify({
                'success': True,
                'role': 'admin',
                'data': all_users.data
            })
        else:
            return jsonify({
                'success': True,
                'role': 'user',
                'data': [{'userid': user['userid'], 'role': user['role']}]
            })

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred during login'}), 500

if __name__ == '__main__':
    app.run(debug=True)
