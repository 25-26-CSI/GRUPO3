"""
Ejemplo Interactivo de Firma Digital DSA
=========================================
Simula un escenario real: envío de un mensaje firmado digitalmente
"""

from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class PersonaConFirmaDigital:
    """Representa una persona con capacidad de firmar digitalmente"""
    
    def __init__(self, nombre):
        self.nombre = nombre
        # Generar par de claves al crear la persona
        self.clave_privada = dsa.generate_private_key(key_size=2048)
        self.clave_publica = self.clave_privada.public_key()
        print(f"👤 {nombre} ha generado sus claves DSA")
    
    def firmar_mensaje(self, mensaje):
        """Firma un mensaje usando la clave privada"""
        if isinstance(mensaje, str):
            mensaje = mensaje.encode()
        
        firma = self.clave_privada.sign(mensaje, hashes.SHA256())
        print(f"✍️  {self.nombre} ha firmado el mensaje")
        return firma
    
    def obtener_clave_publica(self):
        """Comparte la clave pública (puede ser pública)"""
        return self.clave_publica


def verificar_firma(clave_publica, mensaje, firma):
    """Verifica si una firma es válida para un mensaje dado"""
    if isinstance(mensaje, str):
        mensaje = mensaje.encode()
    
    try:
        clave_publica.verify(firma, mensaje, hashes.SHA256())
        return True
    except InvalidSignature:
        return False


# ============================================================================
# SIMULACIÓN DE USO REAL
# ============================================================================
print("=" * 70)
print("SIMULACIÓN: Envío de Mensaje con Firma Digital")
print("=" * 70)

# Crear dos personas
print("\n1️⃣ Creando participantes...")
alice = PersonaConFirmaDigital("Alice")
bob = PersonaConFirmaDigital("Bob")

# Alice envía un mensaje firmado
print("\n2️⃣ Alice envía un mensaje firmado a Bob...")
mensaje_original = "Bob, te debo $100. Firmado: Alice"
print(f"   📄 Mensaje: '{mensaje_original}'")
firma_alice = alice.firmar_mensaje(mensaje_original)

# Bob verifica la firma de Alice
print("\n3️⃣ Bob verifica la firma usando la clave pública de Alice...")
clave_publica_alice = alice.obtener_clave_publica()
es_valida = verificar_firma(clave_publica_alice, mensaje_original, firma_alice)

if es_valida:
    print("   ✅ ¡Firma VÁLIDA! Bob confirma que Alice envió el mensaje")
else:
    print("   ❌ Firma INVÁLIDA")

# Un atacante intenta modificar el mensaje
print("\n4️⃣ Un atacante intercepta y modifica el mensaje...")
mensaje_modificado = "Bob, te debo $1000. Firmado: Alice"  # ¡Cambió 100 por 1000!
print(f"   📄 Mensaje modificado: '{mensaje_modificado}'")
print("   (El atacante usa la misma firma de Alice)")

print("\n5️⃣ Bob verifica la firma del mensaje modificado...")
es_valida_modificado = verificar_firma(clave_publica_alice, mensaje_modificado, firma_alice)

if es_valida_modificado:
    print("   ✅ Firma válida")
else:
    print("   ❌ ¡Firma INVÁLIDA! Bob detecta que el mensaje fue alterado")
    print("   🛡️ La firma digital protegió a Bob del fraude")

# Bob intenta hacerse pasar por Alice
print("\n6️⃣ Bob intenta firmar un mensaje como si fuera Alice...")
mensaje_falso = "Hola, soy Alice (pero realmente es Bob)"
firma_bob = bob.firmar_mensaje(mensaje_falso)
print("   (Bob firma con su propia clave privada)")

print("\n7️⃣ Alguien verifica usando la clave pública de Alice...")
es_valida_falsa = verificar_firma(clave_publica_alice, mensaje_falso, firma_bob)

if es_valida_falsa:
    print("   ✅ Firma válida")
else:
    print("   ❌ ¡Firma INVÁLIDA! La firma no corresponde a Alice")
    print("   🛡️ Bob no puede hacerse pasar por Alice")

print("\n" + "=" * 70)
print("CONCLUSIÓN:")
print("=" * 70)
print("✓ La firma digital permite verificar la identidad del remitente")
print("✓ Cualquier modificación del mensaje invalida la firma")
print("✓ Es imposible falsificar la firma sin la clave privada")
print("=" * 70)
