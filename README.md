###### Flask Web Portfolio ######

Това е минимално Flask Web приложение служещо за портфолио с контактна форма, което изпраща имейли чрез SMTP ( Mailtrap). Приложението е защитено чрез Nginx reverse proxy с IP whitelisting, така че достъпът е ограничен само до определени източници.

## 📦 Изисквания

* Python 3.7+
* pip

## 🧪 Локално стартиране

1. Клониране на проекта:

git clone https://github.com/rsnsktw/Flask-app.git

2. Инсталиране на зависимостите:

pip install -r requirements.txt

3. .env Файл който съдържа необходимите променливи

touch <WORKING_PROJECT_DIRECTORY>/.env

4. Редактиране на `.env` с необходимите променливи за проекта:

SECRET_KEY=<your_secret_key>
MAIL_SERVER=<smtp.example.com>
MAIL_PORT=587
MAIL_USERNAME=<your_email>
MAIL_PASSWORD=<your_app_password>
MAIL_USE_TLS=True
MAIL_USE_SSL=False
YOUR_EMAIL=<destination_email>

5. Стартирай на приложението локално или чрез service:


## Локално стартиране като се дефинира кой app:

export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000

## Стартиране чрез service

[Unit]
Description=Gunicorn instance to serve portfolio
After=network.target

[Service]
User=<USER>
Group=<GROUP>
WorkingDirectory=<PROJECT_WORKING_DIRECTORY>
ExecStart=/usr/local/bin/gunicorn -w 3 -b 127.0.0.1:8000 run:app

[Install]
WantedBy=multi-user.target

6. Отваряне в браузър и тестване:

## Ако приложението е стартирано локално може да се достъпи така:
http://localhost:8000

## Ако приложението е пуснато чрез Service и е проксирано, се достъпва на порта по подразбиране (HTTP):
http://localhost

## 🔒 Продукционна защита

Приложението работи зад Nginx reverse proxy, който:

* Пренасочва заявките към Flask приложението на `127.0.0.1:8000`
* Блокира достъп на външни IP адреси чрез `allow/deny` правила

## Примерна Nginx конфигурация:

server {
    listen 80;
    server_name example.com;

    location / {
        allow <YOUR_IP_ADDRESS>; # Твоя IP адрес или този който искаш да разрешиш
        deny all;
        proxy_pass http://127.0.0.1:8000; # Проксиране на адреса
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📂 Структура на проекта

myportfolio/
├── app.py
├── templates/
│   ├── base.html
│   ├── contact.html
│   └── ...
├── static/
│   └── styles.css
├── .env
├── requirements.txt
└── README.md

## ☁️  Пускане на проека

Препоръчва се използване на Gunicorn + Nginx или Docker. Увери се, че `.env` файлът е настроен и достъпът до порта е ограничен през защитна стена.

