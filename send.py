from mail_client import send_email

if __name__ == "__main__":
    print("Enviando correo de prueba...")
    try:
        send_email(
            subject="Prueba de correo para el TPI",
            body="Este es el cuerpo del mensaje de prueba.",
        )
        print("Correo enviado exitosamente de nico a facu.")
    except Exception as exc:
        print(f"Error al enviar el correo: {exc}")
