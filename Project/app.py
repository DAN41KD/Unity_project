from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    vards = request.form['nam']
    spe = request.form['str']
    vei = request.form['dex']
    izt = request.form['sta']
    har = request.form['cha']
    man = request.form['man']
    sav = request.form['com']
    inte = request.form['int']
    pr = request.form['wit']
    apn = request.form['res']
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO characters (vards, speks, veikliba, izturiba, harizma, manipulacija, savaldiba, intelekts, prats, apnemiba) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (vards, spe, vei, izt, har, man, sav, inte, pr, apn))
    conn.commit()
    conn.close()

@app.route('/characters')
def get_chars():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    sort_by = request.args.get('sort', 'id')
    cursor.execute('SELECT vards, speks, veikliba, izturiba, harizma, manipulacija, savaldiba, intelekts, prats, apnemiba, data FROM characters ORDER BY {sort_by} LIMIT ? OFFSET ?',
                   (per_page, (page-1)*per_page))
    characters = cursor.fetchall()
    conn.close()
    return characters

def get_current_char():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT vards, speks, veikliba, izturiba, harizma, manipulacija, savaldiba, intelekts, prats, apnemiba FROM characters ORDER BY data DESC')
    stats = cursor.fetchone()[0]
    conn.close()
    return stats

@app.route('/result')
def characters():
    characters = get_chars()
    stats = get_current_char()
    return render_template('result.html', characters=characters, stats=stats)

if __name__ == '__main__':
  app.run(debug=True)
