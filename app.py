from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import re
import socket

# Зареждане на .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default123')

# Конфигурация на мейл
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'

mail = Mail(app)
YOUR_EMAIL = os.getenv('YOUR_EMAIL')

# Timeout за SMTP
socket.setdefaulttimeout(5)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if not all([name, email, subject, message]) or not is_valid_email(email):
            flash("Моля, попълнете всички полета коректно.")
            return redirect("/contact")

        msg = Message(
            subject=f"Съобщение от сайта: {subject}",
            sender=(name, app.config['MAIL_USERNAME']),
            recipients=[YOUR_EMAIL]
        )
        msg.body = f"""
        Съобщение от: {name}
        Имейл: {email}

        {message}
        """

        try:
            mail.send(msg)
            flash("Съобщението беше изпратено успешно!")
        except Exception as e:
            print(f"[ГРЕШКА при изпращане]: {e}")
            flash("Имейлът не можа да бъде изпратен. Провери SMTP настройките.")

        return redirect("/contact")

    return render_template("contact.html")

