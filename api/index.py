from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
from supabase import create_client, Client
import os

url = "https://hwuzklwcarlsjcyuhulv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh3dXprbHdjYXJsc2pjeXVodWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkyMDQ4MTEsImV4cCI6MjA1NDc4MDgxMX0.XdcIM_6-mmBQa48g0MlHfBckHDG0g4LzMYu01e3y6VA"
supabase: Client = create_client(url, key)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        userid = data.get('userid')
        password_hash = data.get('password_hash')

        try:
            response = supabase.table('users').select('*').eq('userid', userid).execute()
            
            if not response.data:
                self.send_error(401, 'Invalid credentials')
                return

            user = response.data[0]
            if user['password_hash'] != password_hash:
                self.send_error(401, 'Invalid credentials')
                return

            if user['role'] == 'admin':
                all_users = supabase.table('users').select('userid, role').execute()
                result = {
                    'success': True,
                    'role': 'admin',
                    'data': all_users.data
                }
            else:
                result = {
                    'success': True,
                    'role': 'user',
                    'data': [{'userid': user['userid'], 'role': user['role']}]
                }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            self.send_error(500, f'An error occurred: {str(e)}')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
