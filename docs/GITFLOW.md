# Política de Control de Versiones y Flujo de Trabajo (Gitflow)

Este documento define cómo el equipo de **SOCIALIT** utilizará Git y GitHub para gestionar el código fuente y asegurar la calidad del software entregable.

---

## 1. Estrategia de Ramas (Branching Model)

Utilizaremos una adaptación de **Gitflow**. El repositorio tendrá dos ramas principales y múltiples ramas temporales.

### Ramas Principales 

* **`master`**: 🔴 **INTOCABLE.** Contiene únicamente el código de producción listo para ser entregado al profesor.
    * *Regla:* Solo recibe cambios desde `develop` cuando se completa una fase del proyecto (Inception, Design, Construction).
    * *Protección:* Requiere Pull Request obligatoria. Nadie puede hacer push directo.
* **`develop`**: 🟡 **INTEGRACIÓN.** Es la rama base para el trabajo diario. Contiene las últimas funcionalidades terminadas y probadas.
    * *Regla:* Todo el equipo crea sus ramas a partir de aquí.

### Ramas de Soporte (Temporales)

* **Feature Branches (`feature/nombre-tarea`)**:
    * **Uso:** Para desarrollar nuevas historias de usuario o requerimientos (ej. "Crear Login", "Diseñar Muro").
    * **Origen:** `develop`.
    * **Destino:** `develop` (vía Pull Request).

### 💬 Mensajes de Commit 
Usar prefijos para identificar cambios rápidamente en el historial:
* `feat:` Nueva funcionalidad.
* `fix:` Corrección de error.
* `docs:` Cambios en documentación.
* `style:` Cambios de formato (espacios, comas) sin cambio lógico.
* `refactor:` Mejoras de código sin cambiar funcionalidad.

### 🔀 Pull Requests (PR)
1.  Nunca hacer push directo a `main` o `develop`.
2.  Crear un PR desde tu rama `feature/...` hacia `develop`.
3.  **Revisión:** Otro compañero debe aprobar el PR (Code Review) para evitar copias idénticas o errores lógicos.