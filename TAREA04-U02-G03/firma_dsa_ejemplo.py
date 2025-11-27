"""
Demostración de Firma Digital usando DSA (Digital Signature Algorithm)
========================================================================

Este ejemplo muestra cómo:
1. Generar un par de claves DSA (pública y privada)
2. Firmar un mensaje con la clave privada
3. Verificar la firma con la clave pública
"""

from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

print("=" * 70)
print("DEMOSTRACIÓN DE FIRMA DIGITAL DSA")
print("=" * 70)

# ============================================================================
# PASO 1: Generar claves DSA
# ============================================================================
print("\n📌 PASO 1: Generando par de claves DSA...")
private_key = dsa.generate_private_key(key_size=2048)
public_key = private_key.public_key()
print("   ✔ Clave privada generada (mantener en secreto)")
print("   ✔ Clave pública generada (compartir libremente)")

# ============================================================================
# PASO 2: Crear y firmar el mensaje
# ============================================================================
mensaje = b"Hola, esta es mi firma digital DSA"
print(f"\n📌 PASO 2: Firmando el mensaje...")
print(f"   Mensaje original: {mensaje.decode()}")

# Firmar el mensaje usando la clave privada
firma = private_key.sign(
    mensaje,
    hashes.SHA256()
)

print(f"   ✔ Firma generada ({len(firma)} bytes)")
print(f"   Firma (primeros 32 bytes en hex): {firma[:32].hex()}")

# ============================================================================
# PASO 3: Verificar la firma (mensaje original)
# ============================================================================
print("\n📌 PASO 3: Verificando la firma del mensaje original...")
try:
    public_key.verify(
        firma,
        mensaje,
        hashes.SHA256()
    )
    print("   ✔ ¡La firma es VÁLIDA! El mensaje no ha sido modificado.")
except InvalidSignature:
    print("   ❌ La firma NO es válida")

# ============================================================================
# PASO 4: Intentar verificar con un mensaje alterado
# ============================================================================
print("\n📌 PASO 4: Probando con un mensaje ALTERADO...")
mensaje_alterado = b"Hola, esta es mi firma digital DSA modificada"
print(f"   Mensaje alterado: {mensaje_alterado.decode()}")

try:
    public_key.verify(
        firma,
        mensaje_alterado,
        hashes.SHA256()
    )
    print("   ✔ La firma es válida")
except InvalidSignature:
    print("   ❌ ¡La firma NO es válida! El mensaje fue modificado.")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 70)
print("RESUMEN:")
print("=" * 70)
print("• La firma digital garantiza la autenticidad e integridad del mensaje")
print("• Solo la clave privada puede crear la firma")
print("• Cualquiera con la clave pública puede verificar la firma")
print("• Si el mensaje cambia, la firma se invalida automáticamente")
print("=" * 70)
