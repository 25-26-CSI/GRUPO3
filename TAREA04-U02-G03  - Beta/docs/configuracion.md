# Configuración del Proyecto

## Información General

**Nombre del Proyecto**: Sistema de Firma Digital de Documentos  
**Versión**: 1.0.0  
**Lenguaje**: Python 3.8+  
**Tema**: Firma Digital y Electrónica  
**Grupo**: 3  
**Institución**: ESPOL  
**Fecha**: Noviembre 2025

---

## Características del Sistema

### Algoritmos Implementados

| Componente | Algoritmo/Estándar | Configuración |
|------------|-------------------|---------------|
| Firma Digital | RSA | 2048 bits |
| Hash | SHA-256 | 256 bits |
| Padding | PSS | MGF1-SHA256 |
| Certificados | X.509 v3 | Self-signed |
| Formato de Claves | PEM | PKCS#8 |

### Capacidades

- ✅ Generación de claves RSA (2048/4096 bits)
- ✅ Creación de certificados X.509
- ✅ Firma digital con RSA-PSS
- ✅ Verificación de firmas
- ✅ Hashing SHA-256
- ✅ Protección de claves con contraseña
- ✅ Exportación/importación de claves
- ✅ Metadatos de firma (timestamp, firmante)

### Limitaciones (Proyecto Educativo)

- ⚠️ Certificados autofirmados (no CA real)
- ⚠️ Sin revocación de certificados (CRL/OCSP)
- ⚠️ Almacenamiento local (no HSM)
- ⚠️ Sin timestamp authority (TSA)
- ⚠️ Validación temporal básica

---

## Estructura de Módulos

### `key_manager.py`
**Propósito**: Gestión de claves y certificados

**Clases**:
- `KeyManager`: Gestor principal

**Métodos principales**:
- `generate_key_pair()`: Genera par RSA
- `save_private_key()`: Guarda clave privada (PEM)
- `load_public_key()`: Carga clave pública
- `create_certificate()`: Crea certificado X.509
- `get_certificate_info()`: Extrae información del certificado

### `digital_signature.py`
**Propósito**: Creación de firmas digitales

**Clases**:
- `DigitalSignature`: Gestor de firmas

**Métodos principales**:
- `calculate_hash()`: Hash SHA-256
- `sign_document()`: Firma con RSA-PSS
- `save_signature()`: Guarda en JSON
- `display_signature_info()`: Muestra detalles

### `verification.py`
**Propósito**: Verificación de firmas

**Clases**:
- `SignatureVerifier`: Verificador

**Métodos principales**:
- `verify_signature()`: Verifica firma
- `verify_certificate()`: Valida certificado
- `full_verification()`: Verificación completa
- `compare_hashes()`: Compara archivos

### `main.py`
**Propósito**: Interfaz de usuario (CLI)

**Clases**:
- `DigitalSignatureApp`: Aplicación principal

**Funcionalidades**:
- Menú interactivo
- Flujos de trabajo completos
- Manejo de errores
- Ayuda integrada

---

## Configuración de Seguridad

### Tamaños de Clave

```python
# Por defecto
DEFAULT_KEY_SIZE = 2048  # Recomendado

# Alta seguridad
HIGH_SECURITY_KEY_SIZE = 4096

# Mínimo aceptable
MIN_KEY_SIZE = 2048
```

### Algoritmos de Hash

```python
# Principal
HASH_ALGORITHM = "SHA-256"

# Alternativas (no implementadas)
# SHA-384, SHA-512
```

### Validez de Certificados

```python
# Por defecto: 1 año
CERTIFICATE_VALIDITY_DAYS = 365

# Para testing: más corto
# Para producción: considerar 2-3 años
```

---

## Formatos de Archivo

### Claves Privadas (.pem)

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQI...
...
-----END ENCRYPTED PRIVATE KEY-----
```

**Protección**: AES-256-CBC (si tiene contraseña)

### Claves Públicas (.pem)

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
...
-----END PUBLIC KEY-----
```

### Certificados (.pem)

```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKoSdJCx0IQ6MA0GCSqGSIb3...
...
-----END CERTIFICATE-----
```

### Firmas (.json)

```json
{
    "document_name": "contrato.txt",
    "document_hash": "a7b3c9d2...",
    "signature": "3f6a9c2d...",
    "timestamp": "2025-11-26T14:30:00",
    "algorithm": "RSA-PSS with SHA-256",
    "key_size": 2048,
    "signer": {
        "nombre": "Usuario",
        "organizacion": "ESPOL"
    }
}
```

---

## Variables de Entorno (Futuras)

```bash
# Configuración opcional
DIGITAL_SIG_KEY_SIZE=2048
DIGITAL_SIG_HASH_ALGO=SHA256
DIGITAL_SIG_CERT_DAYS=365
```

---

## Dependencias Detalladas

### cryptography 41.0.7
- RSA key generation
- SHA-256 hashing
- X.509 certificates
- PEM serialization
- PSS padding

### PyPDF2 3.0.1
- Lectura de PDFs (futuro)
- Metadata de PDFs

### colorama 0.4.6
- Colores en terminal
- Cross-platform (Windows/Linux/Mac)

### pydantic 2.5.0
- Validación de datos
- Type checking

---

## Roadmap (Mejoras Futuras)

### v1.1 - Próximas Características
- [ ] Soporte completo para PDFs
- [ ] Interfaz gráfica (GUI)
- [ ] Múltiples firmantes
- [ ] Timestamp authority básica

### v1.2 - Características Avanzadas
- [ ] Cadena de certificados
- [ ] Revocación de certificados
- [ ] OCSP stapling
- [ ] HSM support

### v2.0 - Características Empresariales
- [ ] Base de datos de certificados
- [ ] API REST
- [ ] Integración LDAP
- [ ] Auditoría completa

---

## Testing

### Cobertura Actual

```
key_manager.py        ✅ 85%
digital_signature.py  ✅ 90%
verification.py       ✅ 88%
main.py              ⚠️  40% (UI)
```

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html

# Test específico
pytest tests/test_digital_signature.py::TestKeyManager -v
```

---

## Logs y Debugging

### Habilitar logs detallados

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Performance

### Métricas Aproximadas

| Operación | Tiempo (2048 bits) | Tiempo (4096 bits) |
|-----------|-------------------|-------------------|
| Generar claves | ~0.5s | ~3s |
| Firmar documento | ~0.01s | ~0.03s |
| Verificar firma | ~0.01s | ~0.03s |
| Hash SHA-256 (1MB) | ~0.005s | ~0.005s |

---

## Compatibilidad

### Sistemas Operativos
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Fedora)
- ✅ macOS

### Python
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12

---

## Contacto y Soporte

**Desarrollado por**: Grupo 3  
**Proyecto**: Criptografía - Firma Digital  
**Institución**: ESPOL  
**Año**: 2025
