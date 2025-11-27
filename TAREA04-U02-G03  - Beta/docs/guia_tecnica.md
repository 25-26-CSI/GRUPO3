# Guía Técnica de Firma Digital

## Fundamentos Matemáticos de RSA

### Generación de Claves

1. **Seleccionar dos números primos grandes**: p y q
2. **Calcular n**: n = p × q (módulo para operaciones)
3. **Calcular φ(n)**: φ(n) = (p-1) × (q-1)
4. **Elegir e**: 1 < e < φ(n), coprimo con φ(n) (usualmente 65537)
5. **Calcular d**: d × e ≡ 1 (mod φ(n))

**Resultado**:
- Clave pública: (n, e)
- Clave privada: (n, d)

### Proceso de Firma

```
Firma = (Hash)^d mod n
```

Donde:
- Hash: SHA-256 del documento
- d: exponente privado
- n: módulo público

### Proceso de Verificación

```
Hash_verificado = (Firma)^e mod n
```

Donde:
- e: exponente público
- n: módulo público

Si `Hash_verificado == Hash_original` → Firma válida

---

## Algoritmo SHA-256

### Características

- **Familia**: SHA-2
- **Output**: 256 bits (32 bytes, 64 caracteres hex)
- **Bloques**: Procesa en bloques de 512 bits
- **Rondas**: 64 rondas de procesamiento

### Propiedades Criptográficas

1. **Preimage Resistance**: Dado H(x), imposible encontrar x
2. **Second Preimage Resistance**: Dado x, imposible encontrar x' donde H(x) = H(x')
3. **Collision Resistance**: Imposible encontrar x ≠ y donde H(x) = H(y)

### Avalanche Effect

Cambiar un solo bit en el input cambia ~50% del output:

```
Input 1: "Hola"
SHA-256: 3d6e6f0c0d2e7c4b8a9f1e2d3c4b5a6e...

Input 2: "Hola."
SHA-256: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...
```

---

## Padding PSS (Probabilistic Signature Scheme)

### ¿Por qué PSS?

- Más seguro que PKCS#1 v1.5
- Añade aleatoriedad (salt)
- Resistente a ataques de texto elegido

### Estructura

```
EM = maskedDB || H || 0xbc

Donde:
- maskedDB: Datos enmascarados con MGF1
- H: Hash del mensaje
- 0xbc: Marcador final
```

---

## Certificados X.509

### Estructura

```
Certificate:
  - Version: v3
  - Serial Number: Único
  - Signature Algorithm: SHA256withRSA
  - Issuer: DN del emisor
  - Validity:
      - Not Before: Fecha inicio
      - Not After: Fecha fin
  - Subject: DN del propietario
  - Subject Public Key Info:
      - Algorithm: RSA
      - Public Key: (n, e)
  - Extensions: Uso de clave, etc.
  - Signature: Firma del emisor
```

### Distinguished Name (DN)

```
CN=Juan Pérez
O=ESPOL
L=Guayaquil
ST=Guayas
C=EC
```

---

## Formatos de Archivo

### PEM (Privacy Enhanced Mail)

```
-----BEGIN CERTIFICATE-----
Base64 encoded data
-----END CERTIFICATE-----
```

- Texto ASCII
- Base64 encoding
- Fácil de transportar

### DER (Distinguished Encoding Rules)

- Formato binario
- Más compacto
- No legible para humanos

---

## Cadena de Confianza

```
Root CA (Raíz de confianza)
    |
    └── Intermediate CA
            |
            └── End Entity Certificate (Usuario)
```

En este proyecto: **Autofirmado** (self-signed)
- Issuer == Subject
- Sin cadena de validación
- Solo para propósitos educativos

---

## Consideraciones de Seguridad

### Tamaño de Clave RSA

| Bits | Seguridad | Rendimiento | Recomendación |
|------|-----------|-------------|---------------|
| 1024 | ⚠️ Débil | Rápido | NO usar |
| 2048 | ✅ Bueno | Moderado | **Recomendado** |
| 4096 | ✅ Alto | Lento | Alta seguridad |

### Longitud de Hash

| Algoritmo | Bits | Estado |
|-----------|------|--------|
| MD5 | 128 | ❌ Inseguro |
| SHA-1 | 160 | ⚠️ Deprecated |
| SHA-256 | 256 | ✅ **Recomendado** |
| SHA-512 | 512 | ✅ Extra seguro |

---

## Ataques Conocidos

### 1. Man-in-the-Middle
**Mitigación**: Verificar certificados, usar PKI

### 2. Replay Attack
**Mitigación**: Timestamps en firmas

### 3. Key Extraction
**Mitigación**: Proteger clave privada con contraseña

### 4. Hash Collision
**Mitigación**: Usar SHA-256 o superior

---

## Estándares Relacionados

- **PKCS#1**: RSA Cryptography Standard
- **PKCS#7**: Cryptographic Message Syntax (CMS)
- **PKCS#8**: Private Key Information Syntax
- **RFC 5280**: X.509 Certificate Profile
- **RFC 8017**: PKCS #1 v2.2

---

## Glosario

- **Autenticidad**: Garantía de que el firmante es quien dice ser
- **Integridad**: Garantía de que el documento no fue modificado
- **No repudio**: El firmante no puede negar haber firmado
- **PKI**: Public Key Infrastructure
- **CA**: Certificate Authority (Autoridad Certificadora)
- **CRL**: Certificate Revocation List
- **OCSP**: Online Certificate Status Protocol
- **HSM**: Hardware Security Module
