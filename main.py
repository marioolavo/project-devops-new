import smtplib
from flask import Flask,request ,render_template
import requests
from dotenv import load_dotenv
import os

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

app = Flask(__name__)


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
        send_email(message)
        return render_template ("contact.html", send_form=True)
    elif request.method == "GET":
        return render_template("contact.html", send_form=False)

if __name__ == "__main__":
    app.run(debug=True)