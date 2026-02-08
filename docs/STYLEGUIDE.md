# 📘 Guía de Estilo y Colaboración - Red Social ATI

Esta guía define los estándares de código y buenas prácticas para el desarrollo del proyecto **Red Social ATI** (Semestre 2025-2). El objetivo es mantener la consistencia entre todos los integrantes del equipo y facilitar la corrección por parte de los docentes.

---

## 1. Estándares de Código Python

El código debe ser legible y limpio. Seguiremos **PEP 8** estrictamente.

* **Formato Automático:** Se recomienda configurar el editor (VS Code).
* **Comentarios:** El código debe ser auto-explicativo, pero si la lógica es compleja, se debe comentar en español.

---

## 2. Convenciones de Nombres (Naming)

### 🐍 Python & Django
| Elemento | Convención | Ejemplo Correcto | Ejemplo Incorrecto |
| :--- | :--- | :--- | :--- |
| **Clases** | `PascalCase` | `UserProfile`, `JobOffer` | `user_profile`, `job_offer` |
| **Funciones/Variables** | `snake_case` | `calculate_age()`, `user_email` | `calculateAge`, `UserEmail` |
| **Constantes** | `UPPER_CASE` | `MAX_UPLOAD_SIZE` | `max_upload_size` |
| **Archivos** | `snake_case` | `utils.py`, `validators.py` | `Utils.py` |

### 🗄️ Modelos (Base de Datos)
* **Nombres de Modelos:** Siempre en **Singular**.
    * ✅ `class Post(models.Model):`
    * ❌ `class Posts(models.Model):`
* **Relaciones (Foreign Keys):** Usar el nombre del objeto, no el ID.
    * ✅ `author = models.ForeignKey(User...)`
    * ❌ `author_id = models.ForeignKey(User...)` (Django añade `_id` automáticamente).

### 🌐 URLs y Rutas
* **Rutas visibles:** Usar guiones medios (`kebab-case`).
    * `path('perfil-usuario/', ...)`
* **Nombres internos (`name=`):** Usar `snake_case`.
    * `name='user_profile_detail'`

---

## 3. Arquitectura Django

### "Fat Models, Skinny Views" (Modelos gordos, Vistas flacas)
Evita la lógica compleja en `views.py`.
* **Validaciones:** Al `forms.py` o `serializers.py`.
* **Lógica de negocio:** Métodos dentro del modelo en `models.py`.
* **Vistas:** Solo deben recibir la petición y retornar la respuesta.

### Templates
* Ubicación: `templates/` (carpeta global).
* Estructura: Mantener una base común (`base.html`) y heredar de ella.
    ```html
    {% extends "base.html" %}
    {% block content %}
        ...
    {% endblock %}
    ```

---

## 5. Entorno de Desarrollo y Docker

### Archivos de Configuración
* **`requirements.txt`:** Si instalas una nueva librería:
    1. Instala: `pip install libreria`
    2. Actualiza: `pip freeze > requirements.txt`
* **`.env`:** Las variables sensibles (`SECRET_KEY`, `DB_PASSWORD`) van aquí. **Nunca subir este archivo al repo**.
* **Docker:** Si modificas el `Dockerfile`, notifica al equipo para que reconstruyan sus contenedores (`docker-compose build`).

---

## ✅ Definition of Done (DoD)

Una tarea se considera terminada solo si:
1. [ ] El código cumple con esta guía de estilo.
2. [ ] Funciona correctamente en el entorno local (Docker).
3. [ ] No rompe funcionalidades previas.
4. [ ] Ha sido fusionada (merged) en la rama `develop`.
5. [ ] Para cumpliar con "Mobile Fisrt" ninguna issue se considera terminada (done) si no se ve bien en dispositivos moviles (adaptabilidad)
