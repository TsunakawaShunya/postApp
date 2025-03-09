from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'あなたのユニークで秘密のキー'  # ここにユニークな秘密のキーを設定

# MySQLの設定
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blog'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM rooms")
    rooms = cur.fetchall()
    cur.close()
    return render_template('index.html', rooms=rooms)

@app.route('/room/<int:room_id>')
def room(room_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE room_id = %s ORDER BY created_at DESC", (room_id,))
    posts = cur.fetchall()
    cur.close()
    return render_template('room.html', posts=posts, room_id=room_id)

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rooms (name) VALUES (%s)", (room_name,))
        mysql.connection.commit()
        cur.close()
        flash('部屋が作成されました！')
        return redirect(url_for('index'))
    return render_template('create_room.html')

@app.route('/room/<int:room_id>/create_post', methods=['GET', 'POST'])
def create_post(room_id):
    if request.method == 'POST':
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (room_id, content) VALUES (%s, %s)", (room_id, content))
        mysql.connection.commit()
        cur.close()
        flash('投稿が作成されました！')
        return redirect(url_for('room', room_id=room_id))
    return render_template('create_post.html', room_id=room_id)

if __name__ == '__main__':
    app.run(debug=True)