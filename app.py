from flask import Flask, render_template, request, session, jsonify
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'gear_secret_key_2026'

SAVE_FILE = "gear_save.json"

# Colors for skins
COLORS = {
    "Basic": "#FFFFFF", "PIXEL": "#00FFFF", "MUSIC": "#FF00FF", "RDX": "#FF0000",
    "SMOKE": "#808080", "BLOOD": "#8B0000", "SHADOW": "#0000FF", "RACER": "#FFFF00",
    "SYMBIOTE": "#00FF00", "DESPA": "#800080", "JUPITER": "#00FFFF",
    "RED MONSTER": "#FF0000", "TAZ": "#FFD700"
}

def load_users():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    if 'username' in session:
        users = load_users()
        user_data = users.get(session['username'], {})
        return render_template('game.html', 
                             username=session['username'],
                             coins=user_data.get('coins', 0),
                             high_score=user_data.get('high_score', 0),
                             nitro=user_data.get('nitro', 3),
                             unlocked_skins=user_data.get('unlocked_skins', ['Basic']),
                             current_skin=user_data.get('current_skin', 'Basic'))
    return render_template('auth.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if len(username) < 3:
        return jsonify({'success': False, 'message': 'Username too short!'}), 400
    if len(password) < 3:
        return jsonify({'success': False, 'message': 'Password too short!'}), 400
    
    users = load_users()
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists!'}), 400
    
    users[username] = {
        'password': password,
        'coins': 400,
        'unlocked_skins': ['Basic'],
        'current_skin': 'Basic',
        'high_score': 0,
        'total_distance': 0,
        'nitro': 3
    }
    save_users(users)
    session['username'] = username
    
    return jsonify({'success': True, 'message': 'Account created!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'message': 'User not found!'}), 401
    if users[username]['password'] != password:
        return jsonify({'success': False, 'message': 'Incorrect password!'}), 401
    
    session['username'] = username
    return jsonify({'success': True, 'message': 'Logged in!'})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'success': True})

@app.route('/api/user-data', methods=['GET'])
def get_user_data():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    
    users = load_users()
    user_data = users.get(session['username'], {})
    
    return jsonify({
        'success': True,
        'username': session['username'],
        'coins': user_data.get('coins', 0),
        'high_score': user_data.get('high_score', 0),
        'total_distance': user_data.get('total_distance', 0),
        'nitro': user_data.get('nitro', 3),
        'unlocked_skins': user_data.get('unlocked_skins', ['Basic']),
        'current_skin': user_data.get('current_skin', 'Basic')
    })

@app.route('/api/save-race', methods=['POST'])
def save_race():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    
    data = request.json
    distance = data.get('distance', 0)
    coins_earned = data.get('coins_earned', 0)
    
    users = load_users()
    user_data = users[session['username']]
    
    user_data['coins'] += coins_earned
    user_data['total_distance'] += distance
    if distance > user_data['high_score']:
        user_data['high_score'] = distance
    
    save_users(users)
    
    return jsonify({'success': True, 'coins': user_data['coins'], 'high_score': user_data['high_score']})

@app.route('/api/buy-skin', methods=['POST'])
def buy_skin():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    
    data = request.json
    skin = data.get('skin', '').strip().upper()
    
    skin_prices = {
        "PIXEL": 280, "MUSIC": 350, "RDX": 420, "SMOKE": 380,
        "BLOOD": 520, "SHADOW": 650, "RACER": 480, "SYMBIOTE": 720,
        "DESPA": 680, "JUPITER": 850, "RED MONSTER": 1200, "TAZ": 1100
    }
    
    if skin not in skin_prices:
        return jsonify({'success': False, 'message': 'Skin not found!'}), 400
    
    users = load_users()
    user_data = users[session['username']]
    
    if skin in user_data['unlocked_skins']:
        return jsonify({'success': False, 'message': 'Already owned!'}), 400
    if user_data['coins'] < skin_prices[skin]:
        return jsonify({'success': False, 'message': f'Need {skin_prices[skin] - user_data["coins"]} more coins!'}), 400
    
    user_data['coins'] -= skin_prices[skin]
    user_data['unlocked_skins'].append(skin)
    save_users(users)
    
    return jsonify({'success': True, 'coins': user_data['coins']})

@app.route('/api/equip-skin', methods=['POST'])
def equip_skin():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    
    data = request.json
    skin = data.get('skin', '').strip().upper()
    
    users = load_users()
    user_data = users[session['username']]
    
    if skin not in user_data['unlocked_skins']:
        return jsonify({'success': False, 'message': 'Not owned!'}), 400
    
    user_data['current_skin'] = skin
    save_users(users)
    
    return jsonify({'success': True})

@app.route('/api/reset-nitro', methods=['POST'])
def reset_nitro():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    
    users = load_users()
    user_data = users[session['username']]
    
    if user_data['coins'] < 100:
        return jsonify({'success': False, 'message': 'Not enough coins!'}), 400
    
    user_data['coins'] -= 100
    user_data['nitro'] = 3
    save_users(users)
    
    return jsonify({'success': True, 'coins': user_data['coins'], 'nitro': 3})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
