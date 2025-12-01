# 🔐 Firma Digital y DSA - Guía Completa

> **📌 Nota**: Para una navegación rápida del proyecto completo, consulta [`INDICE.md`](INDICE.md)

## 📑 Tabla de Contenidos

1. [Definición de la Tecnología](#-definición-de-la-tecnología)
2. [¿Qué es DSA?](#-qué-es-dsa)
3. [Algoritmos Criptográficos Involucrados](#-algoritmos-criptográficos-involucrados)
4. [Protocolos Criptográficos Involucrados](#-protocolos-criptográficos-involucrados)
5. [Diseño Esquemático de Funcionamiento](#-diseño-esquemático-de-funcionamiento)
6. [Escenarios de Uso Frecuente](#-escenarios-de-uso-frecuente)
7. [Instalación y Ejemplos de Código](#-instalación-y-ejemplos-de-código)
8. [Seguridad](#-seguridad)
9. [Conceptos Clave](#-conceptos-clave)
10. [Consideraciones de Seguridad](#-consideraciones-de-seguridad-importantes)
11. [Referencias](#-referencias-y-recursos-adicionales)

---

## 📚 Definición de la Tecnología

### Firma Digital

Una **firma digital** es un mecanismo criptográfico basado en criptografía asimétrica (clave pública) que permite:

1. **Autenticar** la identidad del firmante
2. **Garantizar la integridad** del documento o mensaje
3. **Proporcionar no repudio** - el firmante no puede negar haber firmado

**Definición técnica**: Es el resultado de aplicar una función matemática irreversible (hash) a un mensaje y cifrar ese hash con la clave privada del firmante. Cualquiera puede verificar la firma usando la clave pública correspondiente.

**Diferencia con Firma Electrónica**: 
- **Firma Electrónica**: Término genérico (puede ser un escaneo, un PIN, etc.)
- **Firma Digital**: Implementación criptográfica específica y matemáticamente segura

## 🔑 ¿Qué es DSA?

**DSA (Digital Signature Algorithm)** es un algoritmo criptográfico de firma digital basado en el problema matemático del logaritmo discreto. Fue propuesto por el **NIST (National Institute of Standards and Technology)** en 1991 y se convirtió en el estándar federal estadounidense **FIPS 186** en 1994.

### Características Técnicas:

- **Tipo**: Algoritmo de clave pública (asimétrico)
- **Base matemática**: Logaritmo discreto en campos finitos
- **Tamaños de clave**: 1024, 2048, 3072 bits (se recomienda 2048+ bits)
- **Solo firma**: DSA solo puede firmar, NO puede cifrar datos
- **Estándar**: FIPS 186-4 (actualizado en 2013)

## 🧮 Algoritmos Criptográficos Involucrados

### 1. **Funciones Hash (Message Digest)**
Convierten un mensaje de cualquier tamaño en un resumen de tamaño fijo:

| Algoritmo | Tamaño Salida | Estado | Uso en DSA |
|-----------|---------------|--------|------------|
| **SHA-1** | 160 bits | ⚠️ Obsoleto | Legado |
| **SHA-224** | 224 bits | ✅ Seguro | Compatible |
| **SHA-256** | 256 bits | ✅ Recomendado | Recomendado |
| **SHA-384** | 384 bits | ✅ Seguro | Alta seguridad |
| **SHA-512** | 512 bits | ✅ Seguro | Alta seguridad |
| **SHA-3** | Variable | ✅ Moderno | Alternativa |

### 2. **Generación de Números Aleatorios (RNG)**
- **CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator)
- Usado para generar claves privadas y valores "k" en el proceso de firma
- Crítico: Un RNG débil compromete toda la seguridad

### 3. **Operaciones de Campo Finito**
- **Exponenciación modular**: $g^x \mod p$
- **Multiplicación modular inversa**: $a^{-1} \mod q$
- **Aritmética en $\mathbb{Z}_q$**: Operaciones módulo un número primo

### 4. **Algoritmos de Generación de Claves**
- Generación de parámetros de dominio (p, q, g)
- Generación de pares de claves (privada/pública)

## 🌐 Protocolos Criptográficos Involucrados

### 1. **FIPS 186-4 (Digital Signature Standard - DSS)**
- **Descripción**: Estándar federal que especifica DSA
- **Función**: Define parámetros, tamaños de clave y procedimientos
- **URL**: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf

### 2. **X.509 (Certificados Digitales)**
- **Descripción**: Estándar para certificados de clave pública
- **Uso con DSA**: Los certificados X.509 pueden contener claves públicas DSA
- **Aplicación**: PKI (Public Key Infrastructure)

### 3. **PKCS #1 (Public-Key Cryptography Standards)**
- **Descripción**: Familia de estándares de RSA Labs
- **Relación**: Define formatos de firma digital (similar a DSA)

### 4. **TLS/SSL (Transport Layer Security)**
- **Versiones**: TLS 1.0 - 1.3
- **Uso**: DSA puede usarse para autenticación en handshake
- **Nota**: TLS 1.3 eliminó soporte para DSA (prefiere ECDSA, EdDSA)

### 5. **OpenPGP / GPG**
- **Descripción**: Protocolo para cifrado y firma de emails
- **Soporte DSA**: DSA/ElGamal para firmas digitales
- **Implementación**: GnuPG (GNU Privacy Guard)

### 6. **S/MIME (Secure/Multipurpose Internet Mail Extensions)**
- **Descripción**: Estándar para email firmado y cifrado
- **Uso DSA**: Permite usar DSA para firmar mensajes de correo

### 7. **SSH (Secure Shell)**
- **Versión**: SSH-2
- **Uso**: DSA para autenticación de host y usuario
- **Formato clave**: ssh-dss (deprecado en favor de RSA/Ed25519)


## 🎨 Diseño Esquemático de Funcionamiento

### Arquitectura General de Firma Digital DSA

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE FIRMA DIGITAL DSA                     │
└─────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════╗
║                    FASE 1: INICIALIZACIÓN                         ║
╚═══════════════════════════════════════════════════════════════════╝

┌──────────────────────────┐
│  Generación de Parámetros│
│       del Sistema        │
└────────────┬─────────────┘
             │
             ▼
    ┌────────────────┐
    │  p: primo grande (1024-3072 bits)
    │  q: primo pequeño (160-256 bits), q | (p-1)
    │  g: generador, g = h^((p-1)/q) mod p
    └────────────────┘

╔═══════════════════════════════════════════════════════════════════╗
║              FASE 2: GENERACIÓN DE CLAVES (Una vez)               ║
╚═══════════════════════════════════════════════════════════════════╝

┌─────────────────┐
│   Usuario/      │
│   Entidad       │
└────────┬────────┘
         │
         ├──────────────────────────────────────┐
         │                                      │
         ▼                                      ▼
┌──────────────────┐                  ┌──────────────────┐
│  CLAVE PRIVADA   │                  │  CLAVE PÚBLICA   │
│                  │                  │                  │
│  x = aleatorio   │                  │  y = g^x mod p   │
│  0 < x < q       │                  │                  │
│                  │                  │                  │
│  🔒 SECRETA      │                  │  🔓 PÚBLICA      │
│  (No compartir)  │                  │  (Compartir)     │
└──────────────────┘                  └──────────────────┘
         │                                      │
         │                                      │
    [Guardada de                           [Publicada en
     forma segura]                          certificado/servidor]


╔═══════════════════════════════════════════════════════════════════╗
║                  FASE 3: PROCESO DE FIRMADO                       ║
╚═══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────┐
│      MENSAJE ORIGINAL       │
│  "Transferir $1000 a Juan"  │
└──────────────┬──────────────┘
               │
               ▼
        ┌─────────────┐
        │  FUNCIÓN    │
        │   HASH      │◄──── SHA-256 / SHA-3
        │  (SHA-256)  │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   h(M)      │ ← Hash del mensaje (256 bits)
        └──────┬──────┘
               │
               │     ┌──────────────────┐
               │     │  k = aleatorio   │
               │     │  0 < k < q       │◄──── CSPRNG
               │     └────────┬─────────┘
               │              │
               ▼              ▼
        ┌─────────────────────────────┐
        │   ALGORITMO DE FIRMA DSA    │
        │                             │
        │  r = (g^k mod p) mod q      │
        │  s = k^(-1)(h(M)+xr) mod q  │
        └──────────────┬──────────────┘
                       │
                       ▼
                ┌─────────────┐
                │   FIRMA     │
                │   (r, s)    │ ← Par de números
                └─────────────┘


╔═══════════════════════════════════════════════════════════════════╗
║                FASE 4: PROCESO DE VERIFICACIÓN                    ║
╚═══════════════════════════════════════════════════════════════════╝

    Receptor recibe:
    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
    │   MENSAJE    │      │    FIRMA     │      │ CLAVE PÚBLICA│
    │      M       │      │    (r, s)    │      │      y       │
    └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
           │                     │                     │
           │                     └─────────┬───────────┘
           ▼                               │
    ┌─────────────┐                        │
    │  HASH(M)    │                        │
    │   h(M)      │                        │
    └──────┬──────┘                        │
           │                               │
           └───────────┬───────────────────┘
                       │
                       ▼
            ┌─────────────────────────┐
            │  ALGORITMO VERIFICACIÓN │
            │                         │
            │  w = s^(-1) mod q       │
            │  u₁= h(M)·w mod q       │
            │  u₂= r·w mod q          │
            │  v = (g^u₁·y^u₂ mod p)  │
            │         mod q           │
            └──────────┬──────────────┘
                       │
                       ▼
                ┌─────────────┐
                │  v == r ?   │
                └──────┬──────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        ┌──────────┐      ┌──────────┐
        │ v = r    │      │ v ≠ r    │
        │          │      │          │
        │ ✅ VÁLIDA│      │ ❌ INVÁLIDA│
        └──────────┘      └──────────┘
        Mensaje          Mensaje alterado
        auténtico        o firma falsa
```

### Flujo de Datos Completo

```
FIRMANTE (Alice)                      VERIFICADOR (Bob)
═══════════════                       ═════════════════

[Mensaje Original]
       │
       │ 1. Hash
       ▼
   [Hash del Msg]
       │
       │ 2. Firma con
       │    clave privada (x)
       ▼
    [Firma (r,s)]
       │
       │ 3. Envía: Mensaje + Firma
       └────────────────────────────────────┐
                                            │
                                            ▼
                                    [Recibe Msg + Firma]
                                            │
                                            │ 4. Obtiene
                                            │    clave pública (y)
                                            ▼
                                    [Hash del Mensaje]
                                            │
                                            │ 5. Verifica con
                                            │    clave pública
                                            ▼
                                       [¿v = r?]
                                            │
                                    ┌───────┴───────┐
                                    ▼               ▼
                                [Aceptar]      [Rechazar]
```

### Parámetros Matemáticos Detallados

```
┌──────────────────────────────────────────────────────────────┐
│                  PARÁMETROS DSA (FIPS 186-4)                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  p = Primo grande (módulo)                                   │
│      ├─ 1024 bits (L=1024, N=160) - Legado                  │
│      ├─ 2048 bits (L=2048, N=224/256) - Recomendado         │
│      └─ 3072 bits (L=3072, N=256) - Alta seguridad          │
│                                                              │
│  q = Primo pequeño (orden del subgrupo)                      │
│      ├─ 160 bits (para claves 1024)                         │
│      ├─ 224 bits (para claves 2048)                         │
│      └─ 256 bits (para claves 2048/3072)                    │
│      • Debe cumplir: q | (p-1)                              │
│                                                              │
│  g = Generador del subgrupo                                  │
│      • g = h^((p-1)/q) mod p, donde 1 < h < p-1             │
│      • g^q mod p = 1                                         │
│                                                              │
│  x = Clave privada                                           │
│      • Aleatorio: 0 < x < q                                  │
│                                                              │
│  y = Clave pública                                           │
│      • y = g^x mod p                                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```



Imagina que tienes dos llaves:

1. **🔒 Llave Privada (secreta)**: Solo tú la tienes, NUNCA la compartes
2. **🔓 Llave Pública (compartida)**: La pueden tener todos

**Proceso de firma:**

```
┌─────────────┐
│   MENSAJE   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   HASH      │◄─────│  SHA-256     │
│  (resumen)  │      │  (algoritmo) │
└──────┬──────┘      └──────────────┘
       │
       │  +  🔒 Llave Privada
       ▼
┌─────────────┐
│    FIRMA    │ ← Firma única para este mensaje
└─────────────┘
```

**Proceso de verificación:**

```
┌─────────────┐    ┌─────────────┐
│   MENSAJE   │    │    FIRMA    │
└──────┬──────┘    └──────┬──────┘
       │                  │
       │    🔓 Llave      │
       │     Pública      │
       ▼                  ▼
      ┌────────────────────┐
      │  ¿COINCIDEN?       │
      └────────┬───────────┘
               │
        ┌──────┴──────┐
        │             │
      ✅ Sí        ❌ No
    (válida)   (inválida)
```

## 🎯 Analogía del Mundo Real

Piensa en DSA como un **sello de lacre antiguo**:

- Tu **anillo con el sello** = Clave privada (solo tú lo tienes)
- La **marca del sello** = Clave pública (todos la conocen)
- El **lacre en la carta** = Firma digital

Si alguien abre la carta y cambia el contenido, el lacre se rompe y se nota la alteración.

---

## 💻 Instalación y Ejemplos de Código

### Instalación de Dependencias

```bash
pip install cryptography
```

### 📝 Archivos de Ejemplo Incluidos

Este proyecto incluye dos ejemplos prácticos:

1. **`firma_dsa_ejemplo.py`**: Demostración básica con explicaciones paso a paso
2. **`firma_dsa_interactivo.py`**: Simulación de un escenario real (Alice y Bob)

### Ejecutar los ejemplos:

```bash
# Ejemplo básico
python firma_dsa_ejemplo.py

# Ejemplo interactivo (más didáctico)
python firma_dsa_interactivo.py
```

### 🔧 Código Ejemplo Mejorado

Tu código original estaba casi correcto. Aquí está la versión optimizada:

```python
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature  # ← Importar excepción específica

# 1. Generar claves DSA (2048 bits recomendado)
print("Generando claves DSA...")
private_key = dsa.generate_private_key(key_size=2048)
public_key = private_key.public_key()

# 2. Mensaje a firmar
mensaje = b"Hola, esta es mi firma digital DSA"
print(f"Mensaje: {mensaje.decode()}")

# 3. Firmar el mensaje con la clave privada
firma = private_key.sign(mensaje, hashes.SHA256())
print(f"\nFirma generada: {len(firma)} bytes")
print(f"Firma (hex): {firma.hex()[:64]}...")

# 4. Verificar la firma con la clave pública
try:
    public_key.verify(firma, mensaje, hashes.SHA256())
    print("\n✔ La firma es VÁLIDA - Mensaje auténtico e íntegro")
except InvalidSignature:  # ← Específico en lugar de except genérico
    print("\n❌ La firma NO es válida - Mensaje alterado o firma incorrecta")

# 5. Demostrar detección de alteración
mensaje_alterado = b"Hola, esta es mi firma digital DSA MODIFICADO"
try:
    public_key.verify(firma, mensaje_alterado, hashes.SHA256())
    print("✔ Firma válida para mensaje alterado")
except InvalidSignature:
    print("❌ Firma INVÁLIDA para mensaje alterado - ¡Sistema funcionando!")
```

### 🎓 ¿Qué Aprendiste?

Con estos ejemplos comprenderás:

- ✓ Generación de pares de claves DSA
- ✓ Proceso de firma digital
- ✓ Verificación de firmas
- ✓ Detección de mensajes alterados
- ✓ Imposibilidad de falsificar firmas


## 🛡️ Seguridad

**¿Es seguro DSA?**

- ✅ Sí, pero se recomienda usar **EdDSA** o **RSA-PSS** para nuevos proyectos
- ✅ DSA es seguro si se usa correctamente (claves de 2048+ bits)
- ⚠️ Nunca compartas tu clave privada

## 📖 Conceptos Clave

| Término | Significado |
|---------|------------|
| **Hash** | Un "resumen" único del mensaje (como una huella digital) |
| **SHA-256** | Algoritmo para crear el hash (256 bits de salida) |
| **Clave Privada** | Tu secreto, solo para ti |
| **Clave Pública** | Compartida con todos, usada para verificar |
| **Firma** | Resultado de aplicar tu clave privada al hash del mensaje |

## 🔒 Consideraciones de Seguridad Importantes

### ⚠️ Mejores Prácticas

1. **Tamaño de Clave**: Usar mínimo 2048 bits (preferiblemente 3072)
2. **Función Hash**: Usar SHA-256 o superior (NO SHA-1)
3. **Generador de Números Aleatorios**: Usar CSPRNG confiable
4. **Protección de Clave Privada**: 
   - Almacenar cifrada
   - Usar hardware security modules (HSM) para aplicaciones críticas
   - Nunca compartir ni transmitir por canales inseguros

### 🚨 Vulnerabilidades Conocidas

| Vulnerabilidad | Descripción | Mitigación |
|----------------|-------------|------------|
| **RNG débil** | Si el valor `k` se repite o es predecible, la clave privada se puede calcular | Usar CSPRNG de calidad criptográfica |
| **Ataques de canal lateral** | Timing attacks pueden revelar información de la clave | Implementaciones constantes en tiempo |
| **SHA-1 obsoleto** | Colisiones SHA-1 ya son posibles | Usar SHA-256 o SHA-3 |
| **Claves pequeñas** | 1024 bits es factorizable | Mínimo 2048 bits |

### 📊 Comparación con Otros Algoritmos

| Característica | DSA | RSA | ECDSA | EdDSA |
|----------------|-----|-----|-------|-------|
| **Tipo** | Solo firma | Firma + Cifrado | Solo firma | Solo firma |
| **Tamaño clave** | 2048-3072 bits | 2048-4096 bits | 256-521 bits | 256 bits |
| **Velocidad firma** | Rápida | Media | Muy rápida | Muy rápida |
| **Tamaño firma** | ~70 bytes | 256-512 bytes | 64 bytes | 64 bytes |
| **Seguridad** | ✅ Alta | ✅ Alta | ✅ Muy alta | ✅✅ Excelente |
| **Recomendación** | ⚠️ Legado | ✅ Estándar | ✅ Moderno | ✅✅ Preferido |

### 🔮 Estado Actual y Futuro

- **DSA**: Considerado seguro pero en desuso
- **TLS 1.3**: Eliminó soporte para DSA
- **Recomendación actual**: EdDSA (Ed25519) o ECDSA para nuevos proyectos
- **Razón**: Claves más pequeñas, mejor rendimiento, menos riesgos de implementación



## 📚 Referencias y Recursos Adicionales

### Estándares Oficiales
- [FIPS 186-4: Digital Signature Standard (DSS)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf) - Especificación oficial de DSA
- [RFC 6979: Deterministic DSA](https://tools.ietf.org/html/rfc6979) - Mejora de seguridad para DSA
- [X.509 PKI Certificate Standard](https://www.itu.int/rec/T-REC-X.509) - Estándar de certificados digitales

### Documentación Técnica
- [Cryptography Library - Python](https://cryptography.io/) - Librería usada en los ejemplos
- [NIST Cryptographic Toolkit](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program) - Validación de algoritmos
- [OpenSSL DSA Documentation](https://www.openssl.org/docs/man1.1.1/man1/openssl-dsa.html)

### Recursos Educativos
- [Handbook of Applied Cryptography](http://cacr.uwaterloo.ca/hac/) - Capítulo 11: Digital Signatures
- [Introduction to Modern Cryptography](https://www.cs.umd.edu/~jkatz/imc.html) - Katz & Lindell
- [Serious Cryptography](https://nostarch.com/seriouscrypto) - Jean-Philippe Aumasson

### Herramientas y Librerías
- **Python**: `cryptography`, `pycryptodome`
- **Java**: Java Cryptography Architecture (JCA)
- **C/C++**: OpenSSL, Libsodium
- **JavaScript/Node.js**: `node-forge`, Web Crypto API

### Legislación y Normativa
- **eIDAS** (EU): Regulación europea de firma electrónica
- **ESIGN Act** (USA): Ley de firmas electrónicas estadounidense
- **NOM-151-SCFI** (México): Norma de firma electrónica avanzada
- **Ley 59/2003** (España): Firma electrónica

---

**Autor**: Grupo 3 - Tarea 04  
**Fecha**: Noviembre 2025  
**Licencia**: Educativo  

---

## 🌍 Escenarios de Uso Frecuente

### **Escenario 1: Firma de Documentos Legales y Contratos Digitales**

**Contexto**: Empresas y gobiernos necesitan firmar documentos con validez legal.

```
┌────────────────────────────────────────────────────────────┐
│              CASO: FIRMA DE CONTRATO LABORAL               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Empresa (RH)                          Empleado (Juan)     │
│  ════════════                          ══════════════      │
│                                                            │
│  1. Genera contrato PDF                                    │
│     "Contrato_Juan_2025.pdf"                              │
│                                                            │
│  2. Aplica firma digital DSA          3. Recibe documento  │
│     - Hash del PDF                       + firma           │
│     - Firma con clave privada                             │
│                                                            │
│  4. Envía: PDF + Firma ───────────────────────────────►    │
│                                                            │
│                                        5. Verifica firma   │
│                                           con clave pública│
│                                           de la empresa    │
│                                                            │
│                                        6. ✅ Firma válida   │
│                                           Contrato aceptado│
│                                                            │
│  RESULTADO:                                                │
│  • Validez legal: Ambas partes tienen prueba              │
│  • No repudio: RH no puede negar que firmó                │
│  • Integridad: Si se modifica, la firma se invalida       │
└────────────────────────────────────────────────────────────┘
```

**Tecnologías usadas**:
- Adobe Sign, DocuSign
- Certificados X.509
- PKI corporativa

**Ventajas**:
- ✅ Validez legal en muchos países
- ✅ Ahorro de tiempo y papel
- ✅ Trazabilidad completa

---

### **Escenario 2: Autenticación de Software y Actualizaciones**

**Contexto**: Desarrolladores de software firman sus programas para garantizar autenticidad.

```
┌────────────────────────────────────────────────────────────┐
│         CASO: ACTUALIZACIÓN DE SISTEMA OPERATIVO           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Microsoft/Ubuntu                      Usuario Final       │
│  ════════════════                      ═════════════       │
│                                                            │
│  1. Desarrolla actualización                               │
│     "windows_update_KB5012345.msu"                        │
│                                                            │
│  2. Firma el paquete con DSA/RSA                          │
│     - Hash del archivo .msu                               │
│     - Firma con clave privada Microsoft                   │
│     - Incluye firma en el paquete                         │
│                                                            │
│  3. Publica en servidores ──────────────────────────────►  │
│     Windows Update                                        │
│                                                            │
│                                        4. Descarga update  │
│                                           automáticamente  │
│                                                            │
│                                        5. Windows verifica:│
│                                           • Hash del archivo│
│                                           • Firma digital  │
│                                           • Certificado MS │
│                                                            │
│                                        6. ¿Firma válida?   │
│                                           ├─ ✅ Sí: Instala│
│                                           └─ ❌ No: Rechaza│
│                                                            │
│  PROTECCIÓN:                                               │
│  • Malware no puede inyectar código falso                 │
│  • Usuarios protegidos de actualizaciones adulteradas     │
│  • Confianza en la cadena de distribución                 │
└────────────────────────────────────────────────────────────┘
```

**Ejemplos reales**:
- **Windows**: Authenticode (usa SHA-256 + RSA/DSA)
- **Linux**: Paquetes .deb y .rpm firmados con GPG
- **macOS**: Code Signing con certificados Apple
- **Android**: APK Signature Scheme

**Aplicaciones**:
- Actualizaciones de sistema operativo
- Instaladores de software (.exe, .msi)
- Aplicaciones móviles (APK, IPA)
- Firmware de dispositivos IoT

---

### **Escenario 3: Comunicaciones Seguras y Email Firmado**

**Contexto**: Profesionales y organizaciones firman emails para autenticidad.

```
┌────────────────────────────────────────────────────────────┐
│           CASO: EMAIL CORPORATIVO FIRMADO (S/MIME)         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  CEO (alice@company.com)               CFO (bob@co.com)    │
│  ═══════════════════════               ═══════════════     │
│                                                            │
│  1. Escribe email crítico:                                 │
│     ┌──────────────────────┐                              │
│     │ Para: CFO            │                              │
│     │ Asunto: Autorización │                              │
│     │ Apruebo transferencia│                              │
│     │ de $500,000 al       │                              │
│     │ proyecto X           │                              │
│     └──────────────────────┘                              │
│                                                            │
│  2. Firma con certificado S/MIME                          │
│     - Cliente email: Outlook/Thunderbird                  │
│     - Usa clave privada del certificado                   │
│     - Adjunta firma digital                               │
│                                                            │
│  3. Envía email firmado ──────────────────────────────►    │
│     (Protocolo S/MIME sobre SMTP)                         │
│                                                            │
│                                        4. Recibe email     │
│                                                            │
│                                        5. Cliente verifica:│
│                                           • Extrae firma   │
│                                           • Valida cert.   │
│                                           • Verifica cadena│
│                                                            │
│                                        6. Muestra resultado│
│                                           ✅ "Firmado por: │
│                                           alice@company"   │
│                                           🔒 Firma válida  │
│                                                            │
│  ATAQUE PREVENIDO:                                         │
│  ❌ Phishing: Un atacante envía email falso:               │
│     "De: alice@company.com (falsificado)"                 │
│     SIN firma digital válida                              │
│     → Bob detecta que NO está firmado = SOSPECHOSO        │
└────────────────────────────────────────────────────────────┘
```

**Protocolos usados**:
- **S/MIME** (Secure/Multipurpose Internet Mail Extensions)
- **OpenPGP** / GPG (GNU Privacy Guard)
- Certificados X.509

**Casos de uso**:
- 📧 Emails corporativos sensibles
- 🏛️ Comunicaciones gubernamentales
- 💼 Órdenes de compra y facturas
- 🏥 Registros médicos (HIPAA)
- ⚖️ Comunicaciones legales

**Clientes de email compatibles**:
- Microsoft Outlook
- Mozilla Thunderbird
- Apple Mail
- Gmail (con extensiones)

---


