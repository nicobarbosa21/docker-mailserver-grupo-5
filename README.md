
1. Iniciar el contenedor del servidor de correo.
   docker compose up -d

2. Instalar dependencias de la aplicacion web (en un entorno virtual, recomendado).
   pip install -r requirements.txt

3. Ejecutar la interfaz Flask.
   flask --app app run --debug

4. Abrir `http://127.0.0.1:5000` en el navegador para interactuar con el cliente emisor y revisar el buzon receptor.
