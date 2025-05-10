# BITÁCORA: Implementación de Restablecimiento de Contraseña

## 📌 Requerimiento
**Asunto:** "Implementar restablecimiento de contraseña vía código numérico"  
**Descripción:** Usuarios no pueden recuperar acceso autónomamente. Se requiere sistema que:
- Genere código de 6 dígitos
- Valide identidad por correo
- Permita establecer nueva contraseña

## 🎯 Alcance/Objetivo
| Área | Detalle                                                 |
|-------|---------------------------------------------------------|
| Backend | 2 nuevos endpoints (solicitud/validación)               |
| Frontend | Nuevo Botón  de ¿ olvide mi contraseña?                 |
| Seguridad | Validación tiempo real y protección contra fuerza bruta |

## 🌿 Rama
`main`

## ️ Ajustes Base de Datos
```sql
N/A

📦 Módulos Afectados
auth_service 

email_service (Plantilla correo)

frontend  Autenticación 

security_monitoring (Registro de intentos)

🔄 Flujo Esperado


🛡️ Reglas de Seguridad
Expiración: 15 minutos

Intentos máximos: 3 por código

Complejidad nueva contraseña:

regex
^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
Logging:
python
logger.audit(
    f"Reset pass attempt - User:{user_id} "
    f"IP:{request.client.host} "
    f"Status:{status}"
)
🧪 Casos de Prueba
Escenario	Entrada	Resultado Esperado
Email no registrado	"noexiste@test.com"	HTTP 200 (mensaje genérico)
Código correcto	"123456"	HTTP 200 + update password
Código expirado	(código >15min)	HTTP 410 Gone
4to intento fallido	4 códigos erróneos	HTTP 429 Too Many Requests
📝 Documentación Frontend
Componentes requeridos:

javascript
// Ejemplo React
const ResetPasswordFlow = () => {
  const [step, setStep] = useState('request'); // 'request' | 'verify'
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  // ... handlers para API calls
}
Llamadas API:

javascript
// Solicitar código
await axios.post('/auth/request-reset-code', { email });

// Validar código
await axios.post('/auth/verify-reset-code', {
  email,
  code,
  new_password: "NuevaClave123!"
});
✅ Checklist
Endpoints implementados (Backend)

Plantilla de email configurada

Validación frontend de:

Formato email

Complejidad contraseña

