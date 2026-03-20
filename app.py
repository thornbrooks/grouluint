import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── Mail config ──────────────────────────────────────────────
app.config["MAIL_SERVER"]   = "smtp.gmail.com"
app.config["MAIL_PORT"]     = 587
app.config["MAIL_USE_TLS"]  = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

RECIPIENT = os.getenv("MAIL_RECIPIENT", os.getenv("MAIL_USERNAME"))


# ── Routes ───────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    service = request.form.get("service", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Please fill in all required fields."}), 400

    try:
        msg = Message(
            subject=f"New enquiry from {name} — Groulu Media",
            sender=app.config["MAIL_USERNAME"],
            recipients=[RECIPIENT],
            reply_to=email,
        )
        msg.body = f"""
New contact form submission from groulumedia.com

Name:    {name}
Email:   {email}
Service: {service or 'Not specified'}

Message:
{message}
        """.strip()

        mail.send(msg)
        return jsonify({"success": True, "message": "Message sent successfully!"})

    except Exception as e:
        print(f"Mail error: {e}")
        return jsonify({"success": False, "error": "Something went wrong. Please try again."}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

