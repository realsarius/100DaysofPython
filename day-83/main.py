from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from datetime import datetime
from dotenv import load_dotenv
import os

# load env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

# Initialize mail
mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if email and subject and message:
            msg = Message(
                subject,
                sender=os.getenv('MAIL_USERNAME'),
                recipients=[os.getenv('MAIL_USERNAME')],
                reply_to=email
            )
            # Return E-mail as well, because we're sending the e-mail to ourselves
            msg.body = f"Email: {email}\n\nSubject: {subject}\n\nMessage: {message}"
            try:
                mail.send(msg)
                return jsonify({'message': 'Message sent successfully!'}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
