import sqlite3
import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Veritabanı Ayarları
DB_FOLDER = '/app/data'
DB_FILE = os.path.join(DB_FOLDER, 'guestbook.db')

def init_db():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- 1. KISIM: MEVCUT HTML ARAYÜZÜ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if request.method == 'POST':
        # HTML Formundan gelen veri (Form Data)
        name = request.form.get('name')
        content = request.form.get('content')
        c.execute("INSERT INTO messages (name, content) VALUES (?, ?)", (name, content))
        conn.commit()
        conn.close()
        return redirect('/')

    c.execute("SELECT name, content FROM messages ORDER BY id DESC")
    messages = c.fetchall()
    conn.close()
    
    return render_template('index.html', messages=messages)

# --- 2. KISIM: YENİ API ENDPOINTLERİ ---

# API: Tüm mesajları JSON olarak getir
@app.route('/api/mesajlar', methods=['GET'])
def api_get_messages():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, content FROM messages ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    
    # Veritabanından gelen veriyi JSON formatına (Liste içinde Sözlük) çeviriyoruz
    json_data = []
    for row in data:
        json_data.append({"gonderen": row[0], "mesaj": row[1]})
        
    return jsonify(json_data)

# API: Yeni mesaj ekle (JSON kabul eder)
@app.route('/api/ekle', methods=['POST'])
def api_add_message():
    # JSON verisini al (Form değil!)
    yeni_veri = request.get_json()
    
    if not yeni_veri or 'name' not in yeni_veri or 'content' not in yeni_veri:
        return jsonify({"hata": "Eksik veri! 'name' ve 'content' gerekli."}), 400
        
    name = yeni_veri['name']
    content = yeni_veri['content']
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    conn.close()
    
    return jsonify({"durum": "Basarili", "mesaj": "Kayit eklendi!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
