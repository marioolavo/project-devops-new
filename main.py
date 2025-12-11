import smtplib
from flask import Flask,request ,render_template
import requests
from dotenv import load_dotenv
import os
import sqlite3

app = Flask(__name__)

# CONNECT TO DATABASE
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn

# CREATE TABLE IF NOT EXISTS
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Function Send Email
load_dotenv()
def send_email(message_to_send):
    # Email settings
    my_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="epmarioolavo@gmail.com",
                            msg=f"Formulary Data\n\n{message_to_send}")


# API JSON
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()



# Routes
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        data = request.form
        message = f"{data['name']}\n{data['phone']}\n{data['email']}\n{data['message']}"

        # Save to DATABASE
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (nome, email, message) VALUES (?, ?, ?)",
            (data['name'], data['email'], data['message'])
        )
        conn.commit()
        conn.close()
        # Send Email
        send_email(message)
        return render_template ("contact.html", send_form=True)
    elif request.method == "GET":
        return render_template("contact.html", send_form=False)


@app.route('/banco')
def ver_banco():
    # 1. Conecta
    conn = get_db()
    cursor = conn.cursor()


    try:
        cursor.execute("SELECT * FROM users")
        dados = cursor.fetchall()
    except sqlite3.OperationalError:
        dados = []

    conn.close()

    # 3. Manda para o HTML
    return render_template("banco.html", usuarios=dados)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)



