# 🔐 Sistema de Firma Digital de Documentos

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Cryptography](https://img.shields.io/badge/Cryptography-RSA--2048-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Descripción del Proyecto

Aplicación educativa de **firma digital de documentos** desarrollada como proyecto de aprendizaje en criptografía. Este sistema implementa firma digital usando **RSA** y **SHA-256**, permitiendo:

- ✅ Generar pares de claves RSA (pública/privada)
- ✅ Crear certificados digitales X.509
- ✅ Firmar documentos de texto y PDF
- ✅ Verificar la autenticidad e integridad de firmas
- ✅ Gestionar certificados digitales

### 🎯 Objetivos de Aprendizaje

- Comprender el funcionamiento de la **criptografía asimétrica**
- Implementar **firmas digitales** usando estándares de la industria
- Aprender sobre **hashing criptográfico** (SHA-256)
- Trabajar con **certificados digitales** y PKI
- Aplicar **buenas prácticas** de programación en Python

---

## 🏗️ Arquitectura del Proyecto

```
TAREA04-U02-G03/
│
├── src/                          # Código fuente
│   ├── __init__.py              # Inicializador del paquete
│   ├── main.py                  # Aplicación principal (CLI)
│   ├── key_manager.py           # Gestión de claves RSA
│   ├── digital_signature.py     # Firma de documentos
│   └── verification.py          # Verificación de firmas
│
├── keys/                         # Claves y certificados (*.pem)
├── documents/                    # Documentos a firmar
├── signatures/                   # Firmas generadas (*.json)
├── docs/                         # Documentación adicional
├── tests/                        # Tests unitarios
│
├── requirements.txt              # Dependencias Python
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo
```

---

## 🔧 Instalación

### Prerrequisitos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio** (o descargar el proyecto):
   ```bash
   git clone <url-del-repositorio>
   cd TAREA04-U02-G03
   ```

2. **Crear un entorno virtual** (recomendado):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Uso de la Aplicación

### Ejecutar la Aplicación

```bash
cd src
python main.py
```

### Menú Principal

```
╔══════════════════════════════════════════════════════════════╗
║        🔐 SISTEMA DE FIRMA DIGITAL DE DOCUMENTOS 🔐         ║
╚══════════════════════════════════════════════════════════════╝

MENÚ PRINCIPAL
==============================================================
1. 🔑 Generar nuevo par de claves y certificado
2. 📂 Cargar claves existentes
3. ✍️  Firmar un documento
4. ✅ Verificar una firma
5. 📋 Ver información del certificado actual
6. ℹ️  Ayuda - ¿Cómo funciona la firma digital?
0. 🚪 Salir
```

---

## 📚 Guía de Uso Paso a Paso

### 1️⃣ Generar Claves y Certificado

**Objetivo**: Crear tu identidad digital

1. Selecciona la opción `1` del menú
2. Ingresa tu información personal:
   - Nombre completo
   - Organización
   - Ciudad, estado, país
3. Asigna un nombre a tus claves (ej: `juan_perez`)
4. Opcionalmente, protege tu clave privada con contraseña

**Resultado**: Se crean 3 archivos en `keys/`:
- `nombre_private.pem` - Tu clave privada (¡MANTENER SEGURA!)
- `nombre_public.pem` - Tu clave pública (puede compartirse)
- `nombre_cert.pem` - Tu certificado digital

### 2️⃣ Firmar un Documento

**Objetivo**: Crear una firma digital para un documento

1. Asegúrate de tener claves cargadas (opción 1 o 2)
2. Coloca tu documento en la carpeta `documents/`
3. Selecciona opción `3`
4. Ingresa la ruta del documento (ej: `documents/contrato.txt`)
5. Define un nombre para la firma

**Resultado**: Archivo JSON en `signatures/` con:
- Hash del documento
- Firma digital
- Metadatos (fecha, algoritmo, firmante)

### 3️⃣ Verificar una Firma

**Objetivo**: Comprobar autenticidad e integridad

1. Selecciona opción `4`
2. Proporciona:
   - Ruta del documento original
   - Ruta del archivo de firma (.json)
   - Ruta de la clave pública del firmante
3. El sistema verifica:
   - ✅ Integridad (documento no modificado)
   - ✅ Autenticidad (firma genuina)
   - ✅ Validez del certificado (si aplica)

---

## 🔬 Conceptos Criptográficos Implementados

### 🔑 RSA (Rivest-Shamir-Adleman)

**Criptografía asimétrica** con dos claves:
- **Clave Privada**: Secreta, para firmar
- **Clave Pública**: Compartida, para verificar

```python
# Generación de claves de 2048 bits
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()
```

### 🔍 SHA-256 (Secure Hash Algorithm)

**Función hash criptográfica** que genera una "huella digital" de 256 bits:

```python
hash = hashlib.sha256(data).hexdigest()
# Ejemplo: "a7b3c9d..." (64 caracteres hexadecimales)
```

**Propiedades**:
- Determinístico (mismo input = mismo hash)
- Irreversible (no se puede obtener el original del hash)
- Resistente a colisiones (dos inputs diferentes = hashes diferentes)

### ✍️ Proceso de Firma Digital

```
Documento → SHA-256 → Hash → Cifrar con Clave Privada → FIRMA
```

### ✅ Proceso de Verificación

```
Documento → SHA-256 → Hash₁
FIRMA → Descifrar con Clave Pública → Hash₂
Hash₁ == Hash₂ ? → VÁLIDA : INVÁLIDA
```

### 📜 Certificados X.509

Vinculan una **identidad** con una **clave pública**:
- Información del propietario (nombre, organización)
- Clave pública
- Periodo de validez
- Firma de la Autoridad Certificadora (en este caso, autofirmado)

---

## 📖 Ejemplos de Uso

### Ejemplo Completo

```bash
# 1. Ejecutar la aplicación
cd src
python main.py

# 2. Generar claves (opción 1)
#    Nombre: alice
#    Organización: ESPOL

# 3. Crear un documento de prueba
echo "Este es un contrato importante" > ../documents/contrato.txt

# 4. Firmar el documento (opción 3)
#    Documento: ../documents/contrato.txt
#    Nombre firma: contrato_firmado

# 5. Verificar la firma (opción 4)
#    Documento: ../documents/contrato.txt
#    Firma: ../signatures/contrato_firmado.json
#    Clave pública: ../keys/alice_public.pem
```

---

## 🧪 Estructura de Archivos Generados

### Archivo de Firma (JSON)

```json
{
    "document_name": "contrato.txt",
    "document_hash": "a7b3c9d2e5f8...",
    "signature": "3f6a9c2d...",
    "timestamp": "2025-11-26T14:30:00",
    "algorithm": "RSA-PSS with SHA-256",
    "key_size": 2048,
    "signer": {
        "nombre": "Alice",
        "organizacion": "ESPOL",
        "certificado_serie": "12345..."
    }
}
```

---

## 🛡️ Seguridad y Mejores Prácticas

### ✅ Recomendaciones

1. **Protege tu clave privada**:
   - Usa contraseña para cifrarla
   - NUNCA la compartas
   - Guárdala en lugar seguro

2. **Tamaño de clave**:
   - Mínimo: 2048 bits (usado en este proyecto)
   - Recomendado para alta seguridad: 4096 bits

3. **Verificación**:
   - Siempre verifica las firmas antes de confiar en un documento
   - Comprueba la validez del certificado

### ⚠️ Limitaciones (Proyecto Educativo)

- Certificados **autofirmados** (no hay Autoridad Certificadora real)
- No implementa **revocación de certificados** (CRL/OCSP)
- No verifica **cadena de confianza** completa
- Almacenamiento local simple (sin HSM)

---

## 📦 Dependencias

| Librería | Versión | Propósito |
|----------|---------|-----------|
| `cryptography` | 41.0.7 | Operaciones criptográficas (RSA, SHA-256, X.509) |
| `PyPDF2` | 3.0.1 | Manejo de archivos PDF |
| `colorama` | 0.4.6 | Colores en terminal (opcional) |
| `pydantic` | 2.5.0 | Validación de datos |

---

## 🧑‍💻 Desarrollo

### Ejecutar Tests

```bash
cd tests
python -m pytest
```

### Agregar Nuevas Funcionalidades

El proyecto está modularizado:
- `key_manager.py`: Lógica de claves
- `digital_signature.py`: Lógica de firma
- `verification.py`: Lógica de verificación
- `main.py`: Interfaz de usuario

---

## 📝 Documentación Técnica

### Módulos Principales

#### `KeyManager`
- `generate_key_pair()`: Genera par RSA
- `save_private_key()`: Guarda clave privada en PEM
- `load_public_key()`: Carga clave pública
- `create_certificate()`: Crea certificado X.509

#### `DigitalSignature`
- `calculate_hash()`: Calcula SHA-256 de archivo
- `sign_document()`: Firma documento con clave privada
- `save_signature()`: Guarda firma en JSON

#### `SignatureVerifier`
- `verify_signature()`: Verifica firma digital
- `verify_certificate()`: Valida certificado
- `full_verification()`: Verificación completa

---

## 🎓 Recursos de Aprendizaje

### Lecturas Recomendadas

1. [RFC 8017 - PKCS #1: RSA Cryptography](https://tools.ietf.org/html/rfc8017)
2. [FIPS 180-4 - SHA-256 Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)
3. [RFC 5280 - X.509 Certificates](https://tools.ietf.org/html/rfc5280)

### Videos y Tutoriales

- [Cómo funciona RSA - Computerphile](https://www.youtube.com/watch?v=wXB-V_Keiu8)
- [SHA-256 explicado - Computerphile](https://www.youtube.com/watch?v=DMtFhACPnTY)

---

## 👥 Autores

**Grupo 3 - Proyecto de Criptografía**
- Tema: Firma Digital y Electrónica
- Institución: ESPOL
- Fecha: Noviembre 2025

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible con fines educativos.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## ❓ Preguntas Frecuentes (FAQ)

### ¿Puedo usar esto en producción?
No, este es un proyecto educativo. Para producción, usa servicios profesionales de firma digital.

### ¿Por qué RSA y no ECDSA?
RSA es más fácil de entender conceptualmente para fines educativos. ECDSA es más eficiente pero más complejo.

### ¿Qué pasa si pierdo mi clave privada?
No podrás firmar más documentos con esa identidad. Deberás generar un nuevo par de claves.

### ¿Puedo firmar archivos grandes?
Sí, el sistema usa hashing que maneja archivos de cualquier tamaño eficientemente.

---

## 📞 Soporte

Para preguntas o problemas:
- Abre un Issue en GitHub
- Contacta al equipo de desarrollo

---

**¡Gracias por usar nuestro Sistema de Firma Digital! 🔐**
