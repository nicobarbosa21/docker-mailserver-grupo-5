from flask import Flask, redirect, render_template, request, url_for, flash

from mail_client import (
    RECEIVER_EMAIL,
    SENDER_EMAIL,
    fetch_recent_messages,
    send_email,
)

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/", methods=["GET", "POST"])
def index():
    status_message = None
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        body = request.form.get("body", "").strip()
        recipient = request.form.get("recipient", RECEIVER_EMAIL).strip()

        if not subject or not body:
            flash("El asunto y el cuerpo son obligatorios.")
            return redirect(url_for("index"))

        try:
            send_email(subject=subject, body=body, recipient=recipient)
            flash("Correo enviado correctamente.")
            return redirect(url_for("index"))
        except Exception as exc:
            status_message = f"Error al enviar el correo: {exc}"

    messages = fetch_recent_messages(limit=10)
    return render_template(
        "index.html",
        messages=messages,
        sender=SENDER_EMAIL,
        recipient=RECEIVER_EMAIL,
        status_message=status_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
