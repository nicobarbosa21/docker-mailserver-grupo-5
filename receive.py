from mail_client import fetch_recent_messages, RECEIVER_EMAIL


def main() -> None:
    print("Recuperando correos para facu...")
    try:
        messages = fetch_recent_messages(limit=1)
        if not messages:
            print("No se encontraron correos.")
            return
        print("Correo mas reciente:")
        date, author, body = messages[0]
        print(f"Fecha: {date}")
        print(f"De: {author}")
        print(f"Para: {RECEIVER_EMAIL}")
        print(f"Cuerpo:\n{body}")
    except Exception as exc:
        print(f"Error al recibir el correo: {exc}")


if __name__ == "__main__":
    main()
