# SocialIT

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-6.0.1-092E20?style=for-the-badge&logo=django)
![Docker](https://img.shields.io/badge/Docker-Available-2496ED?style=for-the-badge&logo=docker)
![Status](https://img.shields.io/badge/Status-In_Development-yellow?style=for-the-badge)

> **Universidad Central de Venezuela** > **Facultad de Ciencias - Escuela de Computación** > **Materia:**  Aplicaciones con Tecnología Internet  
> **Semestre:** 2025-2

## 📖 Descripción del Proyecto

Este proyecto consiste en el desarrollo de una Red Social diseñada para conectar a profesionales de ATI con otros colegas y empresas. El objetivo principal es facilitar la búsqueda de oportunidades laborales, la construcción de relaciones comerciales y el intercambio de conocimientos.

La aplicación permite la creación de perfiles (Personas y Empresas), publicación de contenido multimedia, ofertas de empleo, chat en tiempo real y gestión de postulaciones

## 🛠 Tech Stack

El desarrollo sigue una metodología ágil (Scrum adaptado) y utiliza las siguientes tecnologías:

* **Lenguaje:** Python
* **Framework Web:** Django 6.0.1
* **Base de Datos:** SQLite (Entorno de desarrollo)
* **Contenedores:** Docker & Docker Compose
* **Control de Versiones:** Git & GitHub

## ✨ Funcionalidades Principales

### 👤 Gestión de Usuarios

* Perfiles:

  * Profesionales: Información básica, resumen profesional, educación, experiencia y gustos personales.

  * Empresas: Información comercial, logo, sector, ubicación y cultura empresarial.

* Seguidores: Sistema para seguir a personas o empresas y relacionarse entre sí.

* Autenticación: Registro, inicio de sesión y recuperación de contraseña vía email.

### 📰 Interacción y Contenido (Muro)

* Publicaciones: Texto y contenido multimedia (video, audio, fotos, enlaces).

* Empleos: Publicación de ofertas laborales y sistema de postulaciones.

* Interacción: Comentarios anidados (respuestas a respuestas) en las publicaciones.

* Búsqueda: Búsqueda avanzada de usuarios (por habilidades/educación) y de publicaciones (por palabras clave).

### 💬 Comunicación y Notificaciones

* Chat: Mensajería privada entre usuarios con lista de contactos y solicitudes de chat.

* Notificaciones: Alertas vía sistema y correo electrónico sobre nuevos mensajes, comentarios o postulaciones.

### ⚙️ Requerimientos Generales y Admin

* Panel Administrativo: Moderación de usuarios, publicaciones y comentarios (bloqueo de contenido inapropiado).

* Personalización: Soporte para "Modo Oscuro" y distintos diseños.

* Diseño Adaptativo: Interfaz responsive para distintos dispositivos.

* Internacionalización (i18n): Soporte para múltiples idiomas.

### 🚀 Instalación y Despliegue con Docker

Este proyecto utiliza **Docker** para garantizar que el entorno de desarrollo sea consistente entre todos los miembros del equipo.

#### Prerrequisitos

* [Docker Engine](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

#### Pasos para levantar el entorno (Desarrollo)

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Brhandon28/Red-Social-ATI.git
   cd Red-Social-ATI
   ```

2. **Construir y levantar los contenedores:**
Este comando descargará las imágenes necesarias, instalará las dependencias definidas en el `Dockerfile` y levantará el servidor de desarrollo.

   ```bash
   docker compose up --build
   ```

3. **Aplicar migraciones (Base de Datos):**
Una vez que el contenedor esté corriendo, abre una nueva terminal y ejecuta las migraciones para inicializar la base de datos SQLite:

   ```bash
   docker compose exec web python manage.py migrate
   ```

4. **Crear un superusuario (Admin):**
Para acceder al panel de administración de Django:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. **Acceder a la aplicación:**

* **Web:** Abre tu navegador en `http://localhost:8000`
* **Admin:** `http://localhost:8000/admin`

#### Comandos útiles de Docker

* **Detener el servidor:** Presiona `Ctrl + C` en la terminal o ejecuta:

```bash
docker compose down
```

* **Instalar una nueva dependencia:**
Si agregas una librería a `requirements.txt`, necesitas reconstruir la imagen:

```bash
docker compose up --build
```

#### Pasos para levantar el entorno (Produccion)

```bash
docker compose -f docker-compose.prod.yml up --build
```

Integrantes del equipo:

* [Brandon Oropeza](https://github.com/BlueFox07) - Front-end
* [Brhandon Palomo](https://github.com/Brhandon28) - Back-end
* [Fidel Serpa](https://github.com/Fidel244) - Back-end
* [Jesús Hernández](https://github.com/jesusrafaell) - Full-stack
* [Ronald Herrera](https://github.com/ronaldhab) - Full-stack
* [Yunior Moreno](https://github.com/yuunichi) - Q.A.

## 📚 Documentación y Normas

### ⚠️ Antes de empezar a programar

Por favor revisa nuestras normas de contribución:

* [📘 Guía de Estilo y Buenas Prácticas](docs/STYLEGUIDE.md)
* [🐙 Política de Git y Flujo de Trabajo](docs/GITFLOW.md)

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **GNU General Public License v3.0 (GPLv3)**.

Esto significa que cualquier persona es libre de usar, modificar y distribuir este software, siempre y cuando las versiones derivadas mantengan la misma licencia y el código fuente esté disponible.

Puedes consultar el texto legal completo en el archivo [LICENSE](./LICENSE) o en el sitio oficial de [GNU.org](https://www.gnu.org/licenses/gpl-3.0.es.html).
