# Notificaciones vía Whatsapp 


**Usuario:** odvr

## Resumen

En esta bitácora se documentan los pasos realizados para configurar y ejecutar un servidor Express en un contenedor Docker con la finalidad de enviar mensajes de WhatsApp utilizando la biblioteca `whatsapp-web.js`.

## Pasos Realizados

### 1. Creación del Proyecto

1. **Descripción:** Se creó un proyecto Node.js con un servidor Express.
2. **Archivos relevantes:**
   - `server.js`
   - `package.json`

```javascript name=server.js
const express = require('express');
const cors = require('cors');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const app = express();
const port = process.env.PORT || 3000;

// Middleware para parsear JSON
app.use(express.json());

// Configurar CORS
app.use(cors());

// Crear una nueva instancia del cliente de WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    }
});

// Generar un QR code para escanear con la aplicación de WhatsApp
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escanea el QR code con tu aplicación de WhatsApp.');
});

// Confirmar que la autenticación se ha realizado correctamente
client.on('ready', () => {
    console.log('Cliente está listo!');
});

// Iniciar el cliente de WhatsApp
client.initialize();

// Ruta para enviar mensajes de WhatsApp
app.post('/send-message', (req, res) => {
    const { number, message } = req.body;

    if (!number || !message) {
        return res.status(400).send({ error: 'Número y mensaje son requeridos.' });
    }

    const chatId = `${number}@c.us`;
    
    client.sendMessage(chatId, message).then(response => {
        res.status(200).send({ success: true, response });
    }).catch(err => {
        res.status(500).send({ success: false, error: err.message });
    });
});

// Iniciar el servidor Express
app.listen(port, () => {
    console.log(`Servidor escuchando en el puerto ${port}`);
});
```

```json name=package.json
{
  "name": "whatsapp-api",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "whatsapp-web.js": "^1.14.1",
    "qrcode-terminal": "^0.12.0",
    "cors": "^2.8.5"
  }
}
```

### 2. Configuración del Dockerfile

1. **Descripción:** Se configuró un archivo `Dockerfile` para construir una imagen Docker con las dependencias necesarias.
2. **Archivos relevantes:**

```dockerfile name=Dockerfile
# Utilizar una imagen base de Node.js
FROM node:18

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copiar el archivo package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias del proyecto
RUN npm install

# Instalar las dependencias necesarias para Puppeteer
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    lsb-release \
    xdg-utils \
    wget

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["node", "server.js"]
```

### 3. Configuración de Docker Compose

1. **Descripción:** Se configuró un archivo `docker-compose.yml` para ejecutar el contenedor Docker.
2. **Archivos relevantes:**

```yaml name=docker-compose.yml
services:
  whatsapp-api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
```

### 4. Construcción y Ejecución del Contenedor

1. **Descripción:** Se construyó y ejecutó el contenedor Docker utilizando los siguientes comandos:
   
   ```bash
   docker-compose build
   docker-compose up
   ```

2. **Resultado:** El contenedor se ejecutó correctamente y el servidor Express quedó a la espera de la autenticación mediante el escaneo del código QR.

### 5. Prueba de Envío de Mensaje con Postman

1. **Descripción:** Se configuró Postman para enviar una petición POST y probar el envío de mensajes de WhatsApp.
2. **Configuración de la Petición:**
   - **Método:** POST
   - **URL:** `http://localhost:3000/send-message`
   - **Headers:** `Content-Type: application/json`
   - **Body:**
   
```json
{
  "number": "1234567890",
  "message": "Hola, este es un mensaje de prueba desde Postman."
}
```

### Conclusión

Se logró configurar y ejecutar un servidor Express en un contenedor Docker para enviar mensajes de WhatsApp utilizando la biblioteca `whatsapp-web.js`. La autenticación se realizó mediante el escaneo de un código QR y se verificó el correcto funcionamiento mediante una prueba en Postman.