"""
Algoritmo de Cifrado Simétrico - Blowfish
==========================================
Blowfish es un algoritmo de cifrado simétrico por bloques diseñado por Bruce Schneier en 1993.
Utiliza bloques de 64 bits y claves de longitud variable (32 a 448 bits).
"""

# Importamos la librería de criptografía necesaria
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def cifrar_blowfish(mensaje, clave):
    """
    Función para cifrar un mensaje usando Blowfish
    
    Parámetros:
    - mensaje: Texto plano que queremos cifrar (string)
    - clave: Clave secreta para cifrar (string)
    
    Retorna:
    - Mensaje cifrado en base64 (string)
    - IV (Vector de Inicialización) en base64 (string)
    """
    
    # Convertimos la clave y el mensaje a bytes
    clave_bytes = clave.encode('utf-8')
    mensaje_bytes = mensaje.encode('utf-8')
    
    # Generamos un vector de inicialización aleatorio (IV)
    # El IV asegura que el mismo mensaje cifrado con la misma clave produzca resultados diferentes
    iv = get_random_bytes(8)  # Blowfish usa bloques de 8 bytes (64 bits)
    
    # Creamos el objeto cipher con modo CBC (Cipher Block Chaining)
    # CBC es un modo de operación que hace el cifrado más seguro
    cipher = Blowfish.new(clave_bytes, Blowfish.MODE_CBC, iv)
    
    # Aplicamos padding al mensaje para que sea múltiplo del tamaño de bloque
    # Blowfish requiere que los datos sean múltiplos de 8 bytes
    mensaje_padded = pad(mensaje_bytes, Blowfish.block_size)
    
    # Ciframos el mensaje
    mensaje_cifrado = cipher.encrypt(mensaje_padded)
    
    # Convertimos a base64 para poder mostrar y transmitir fácilmente
    mensaje_cifrado_b64 = base64.b64encode(mensaje_cifrado).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')
    
    return mensaje_cifrado_b64, iv_b64

def descifrar_blowfish(mensaje_cifrado_b64, clave, iv_b64):
    """
    Función para descifrar un mensaje cifrado con Blowfish
    
    Parámetros:
    - mensaje_cifrado_b64: Mensaje cifrado en base64 (string)
    - clave: Clave secreta usada para cifrar (string)
    - iv_b64: Vector de Inicialización en base64 (string)
    
    Retorna:
    - Mensaje descifrado (string)
    """
    
    # Convertimos la clave a bytes
    clave_bytes = clave.encode('utf-8')
    
    # Decodificamos el mensaje cifrado y el IV desde base64
    mensaje_cifrado = base64.b64decode(mensaje_cifrado_b64)
    iv = base64.b64decode(iv_b64)
    
    # Creamos el objeto cipher con los mismos parámetros usados para cifrar
    cipher = Blowfish.new(clave_bytes, Blowfish.MODE_CBC, iv)
    
    # Desciframos el mensaje
    mensaje_descifrado_padded = cipher.decrypt(mensaje_cifrado)
    
    # Removemos el padding aplicado anteriormente
    mensaje_descifrado = unpad(mensaje_descifrado_padded, Blowfish.block_size)
    
    # Convertimos de bytes a string
    return mensaje_descifrado.decode('utf-8')

# ========================================
# EJEMPLO DE USO
# ========================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACIÓN DEL ALGORITMO BLOWFISH")
    print("=" * 60)
    
    # Mensaje original que queremos cifrar
    mensaje_original = "Hola, este es un mensaje secreto usando Blowfish!"
    print(f"\n📝 Mensaje original: {mensaje_original}")
    
    # Clave secreta (debe ser compartida de forma segura entre emisor y receptor)
    # La longitud puede variar entre 4 y 56 bytes
    clave_secreta = "MiClaveSegura2024"
    print(f"🔑 Clave secreta: {clave_secreta}")
    
    # --- PROCESO DE CIFRADO ---
    print("\n" + "=" * 60)
    print("PROCESO DE CIFRADO")
    print("=" * 60)
    
    mensaje_cifrado, iv = cifrar_blowfish(mensaje_original, clave_secreta)
    
    print(f"\n🔒 Mensaje cifrado (Base64):")
    print(f"   {mensaje_cifrado}")
    print(f"\n🎲 Vector de Inicialización (IV):")
    print(f"   {iv}")
    
    # --- PROCESO DE DESCIFRADO ---
    print("\n" + "=" * 60)
    print("PROCESO DE DESCIFRADO")
    print("=" * 60)
    
    mensaje_descifrado = descifrar_blowfish(mensaje_cifrado, clave_secreta, iv)
    
    print(f"\n🔓 Mensaje descifrado: {mensaje_descifrado}")
    
    # --- VERIFICACIÓN ---
    print("\n" + "=" * 60)
    print("VERIFICACIÓN")
    print("=" * 60)
    
    if mensaje_original == mensaje_descifrado:
        print("✅ ¡Éxito! El mensaje descifrado coincide con el original.")
    else:
        print("❌ Error: El mensaje descifrado no coincide con el original.")
    
    # --- EJEMPLO CON CLAVE INCORRECTA ---
    print("\n" + "=" * 60)
    print("INTENTO DE DESCIFRADO CON CLAVE INCORRECTA")
    print("=" * 60)
    
    try:
        clave_incorrecta = "ClaveIncorrecta123"
        print(f"🔑 Intentando con clave incorrecta: {clave_incorrecta}")
        mensaje_erroneo = descifrar_blowfish(mensaje_cifrado, clave_incorrecta, iv)
        print(f"❌ Mensaje descifrado con clave incorrecta: {mensaje_erroneo}")
        print("   (El resultado es basura/texto ilegible)")
    except Exception as e:
        print(f"❌ Error al descifrar: {type(e).__name__}")
        print("   (Esto es esperado con una clave incorrecta)")
    
    print("\n" + "=" * 60)
    print("CARACTERÍSTICAS DE BLOWFISH")
    print("=" * 60)
    print("""
    ✓ Tamaño de bloque: 64 bits (8 bytes)
    ✓ Longitud de clave: Variable (32 a 448 bits)
    ✓ Tipo: Cifrado simétrico por bloques
    ✓ Diseñador: Bruce Schneier (1993)
    ✓ Velocidad: Muy rápido en software
    ✓ Seguridad: Considerado seguro para la mayoría de aplicaciones
    ✓ Uso: Alternativa a DES, usado en varios productos
    """)
    print("=" * 60)
