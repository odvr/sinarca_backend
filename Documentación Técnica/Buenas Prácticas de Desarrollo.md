# Buenas Prácticas de Desarrollo

**Stack: Python, FastAPI, SQLAlchemy, React, MariaDB, Microservicios, Docker, Route 53 (R53)**

---

## 1. Nombres Significativos

* Los nombres deben describir **claramente su propósito**.
* Evitar abreviaturas crípticas (`tmp`, `calc2`, `val`).
* Usar convenciones según lenguaje:

  * Python: `snake_case`
  * React/JS: `camelCase` para funciones y variables, `PascalCase` para componentes
  * SQL: `snake_case` para columnas y tablas
* Ejemplos buenos:

  * `get_user_by_email()`
  * `OrderSummaryCard`
  * `user_id`, `created_at`

---

## 2. Funciones Claras y Concisas

* Una función debe hacer **una sola cosa**.
* Máximo 20–30 líneas por función.
* Deben tener nombres que describan **la intención**, no la implementación.
* Evitar efectos secundarios inesperados.
* Extraer funciones cuando hay lógica anidada o múltiples pasos.

---

## 3. Estructura y Formato del Código

* Usa **formatters automáticos** (`black`, `isort`, `prettier`) y **linters** (`flake8`, `eslint`).
* Mantener la **consistencia** en el uso de espacios, indentación (2/4 espacios), y comillas.
* Divide el proyecto en carpetas por dominio o responsabilidad:

  ```
  /app
    /routers
    /schemas
    /models
    /services
    /repositories
  ```
* En React, organizar por componentes reutilizables o funciones:

  ```
  /components
  /pages
  /hooks
  /services
  ```

---

## 4. Manejo de Errores

* Nunca silenciar errores (ej. `except: pass`).
* Usa excepciones específicas (`ValueError`, `IntegrityError`) y responde adecuadamente.
* En FastAPI, usar `HTTPException(status_code=...)` y un middleware para errores globales.
* Registrar errores con `loguru`, `logging` o herramientas como Sentry.
* Validar entradas de usuarios y prevenir SQL injection o XSS.

---

## 5. Comentarios ÚTiles

* Comenta **el por qué**, no el cómo (eso lo explica el código bien escrito).
* Evitar comentarios redundantes o que repitan el nombre de la función.
* Usa TODO con contexto:
  `# TODO: Validar que el token no esté expirado antes de enviar la solicitud`
* Elimina comentarios obsoletos al refactorizar.

---

## 6. Código Orientado a Objetos

* Usar clases cuando haya **estado** o comportamiento asociado.
* Aplicar **principios de encapsulamiento**: no expongas atributos internos directamente.
* Usa `@classmethod` y `@staticmethod` apropiadamente.
* Divide responsabilidades: una clase, una responsabilidad.

---

## 7. Principios SOLID

* **S - Single Responsibility**: cada clase o función debe tener un único propósito.
* **O - Open/Closed**: abierto a extensión, cerrado a modificación.
* **L - Liskov Substitution**: una subclase debe poder reemplazar a su superclase.
* **I - Interface Segregation**: evita interfaces (clases, modelos) muy grandes.
* **D - Dependency Inversion**: depender de abstracciones, no implementaciones.

---

## 8. Pruebas Automatizadas

* Usa `pytest` en backend y `testing-library/react` en frontend.
* Escribir pruebas unitarias, de integración y e2e.
* Usar mocks para bases de datos, APIs y colas.
* Estructura común:

  ```
  /tests
    /unit
    /integration
    /e2e
  ```
* Asegurar cobertura mínima del 80%.

---

## 9. Control de Versiones

* Estructura de ramas:

  * `main`: producción
  * `develop`: integración
  * `feature/`, `fix/`, `hotfix/`
* Convención de commits (`Conventional Commits`):

  ```
  feat: agregar login de usuario
  fix: corregir error al validar email
  ```
* Siempre usar PRs. Nada de pushes directos a `main`.

---

## 10. Revisiones de Código (Code Reviews)

* Revisar PRs por otro desarrollador **antes de merge**.
* Comentar de forma constructiva.
* Verificar:

  * Calidad del código
  * Estilo
  * Seguridad
  * Pruebas
  * Impacto en otros servicios

---

## 11. Refactorización Continua

* Refactorizar cuando:

  * Se agrega nueva funcionalidad.
  * El código es difícil de entender.
  * Hay duplicación.
* Nunca hacer refactor sin pruebas de respaldo.
* Aplicar patrones de diseño si mejora claridad.

---

## 12. Buenas Prácticas por Lenguaje

### 🦍 Python + FastAPI

* Usar PEP8 + `black` + `isort`
* Dividir rutas por módulo
* Inyección de dependencias con `Depends`
* Tipado estático (`mypy`)
* Separar DTOs (`schemas.py`), modelos (`models.py`), lógica (`services.py`)

### 🐘 MariaDB

* Nombres explícitos para columnas
* ÍNDICES en campos de búsqueda frecuente
* Normalización hasta 3FN
* Migraciones con `alembic`

### ⚛️ React

* Componentes funcionales
* `useEffect` bien controlado
* Hooks personalizados (`useAuth`, `useForm`)
* Modularidad, sin lógica en componentes grandes
* Pruebas con `jest` + `testing-library/react`

---

## 13. Seguridad del Código

* Nunca exponer contraseñas, tokens o claves API (usa `.env`)
* Validación y sanitización de entradas
* CORS configurado correctamente
* Escapar variables en el frontend (`dangerouslySetInnerHTML` con precaución)
* Docker: no ejecutar como root, limitar permisos
* R53: evitar acceso público no intencionado a subdominios

---

## 14. Documentación Técnica

* Incluir README por microservicio
* Documentar rutas de API con FastAPI (`/docs`)
* Agregar comentarios a funciones complejas
* Mantener documentación actualizada en Notion, Confluence o MkDocs
* Diagrama de arquitectura general y dependencias entre servicios

---

## 15. Convenciones del Equipo

* Acuerdos sobre estructura, formato y patrones de diseño
* Checklist de PRs: pruebas, seguridad, legibilidad
* Uso obligatorio de herramientas como `pre-commit`, `docker-compose`, `make`
* Reuniones técnicas para alinear criterios

---

## 16. Responsabilidad del Desarrollador

* Entregar código limpio y probado
* Participar en revisiones de código de otros
* Documentar lo necesario
* Mantenerse actualizado técnicamente
* Ser proactivo con deuda técnica y sugerencias de mejora
