# 🔐 Firma Digital y DSA - Guía Completa

## 📚 ¿Qué es una Firma Digital?

Una **firma digital** es el equivalente electrónico de una firma manuscrita, pero mucho más segura. Es como un sello único e imposible de falsificar que garantiza:

- **✅ Autenticidad**: Confirma quién envió el mensaje
- **✅ Integridad**: Asegura que el mensaje no fue alterado
- **✅ No repudio**: El firmante no puede negar que lo firmó

## 🔑 ¿Qué es DSA?

**DSA (Digital Signature Algorithm)** es un algoritmo matemático para crear firmas digitales. Fue desarrollado por el gobierno de EE.UU. y es un estándar federal.

### ¿Cómo funciona DSA? (Explicación simple)

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

## 💻 Instalación de Dependencias

```bash
pip install cryptography
```

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


## 📚 Referencias

- [Documentación de Cryptography](https://cryptography.io/)
- [FIPS 186-4: Digital Signature Standard](https://csrc.nist.gov/publications/detail/fips/186/4/final)

---