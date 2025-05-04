from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT,
        speks TEXT,
        veikliba TEXT,
        izturiba TEXT,
        harizma TEXT,
        manipulacija TEXT,
        savaldiba TEXT,
        intelekts TEXT,
        prats TEXT,
        apnemiba TEXT,
        data DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    try:
        data = {
            'vards': request.form['nam'],
            'spe': request.form['str'],
            'vei': request.form['dex'],
            'izt': request.form['sta'],
            'har': request.form['cha'],
            'man': request.form['man'],
            'sav': request.form['com'],
            'inte': request.form['int'],
            'pr': request.form['wit'],
            'apn': request.form['res']
        }
    except KeyError as e:
        return "Nav šī atbildi: {e}", 400
    except ValueError as e:
        return "Nekorekti dati", 400
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO characters (vards, speks, veikliba, izturiba, harizma, manipulacija, savaldiba, intelekts, prats, apnemiba) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (data['vards'], data['spe'], data['vei'], data['izt'], data['har'], data['man'], data['sav'], data['inte'], data['pr'], data['apn']))
    conn.commit()
    conn.close()
    return redirect(url_for('characters'))

def get_chars():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sort_columns = ['vards', 'speks', 'veikliba', 'izturiba', 'harizma', 'manipulacija', 'savaldiba', 'intelekts', 'prats', 'apnemiba', 'data']
    sort_by = request.args.get('sort', 'data')
    if sort_by not in sort_columns:
        sort_by = 'data'
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    cursor.execute('SELECT vards, speks, veikliba, izturiba, harizma, manipulacija, savaldiba, intelekts, prats, apnemiba, data FROM characters ORDER BY "{sort_by}" LIMIT ? OFFSET ?', (per_page, offset))
    characters = cursor.fetchall()
    conn.close()
    return characters

def get_current_char():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT vards, speks, veikliba, izturiba, harizma, manipulacija, savaldiba, intelekts, prats, apnemiba FROM characters ORDER BY data DESC')
    stats = cursor.fetchone()
    conn.close()
    return stats

@app.route('/result')
def characters():
    characters = get_chars()
    stats = get_current_char()
    page = request.args.get('page', 1, type=int)
    return render_template('result.html', characters=characters, stats=stats, page=page)

if __name__ == '__main__':
  app.run(debug=True)
