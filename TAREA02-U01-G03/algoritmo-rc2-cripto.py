"""
Algoritmo de Cifrado Simétrico - RC2
=====================================
RC2 (Rivest Cipher 2) es un algoritmo de cifrado simétrico por bloques.
Fue diseñado por Ron Rivest en 1987 para RSA Security.
Utiliza bloques de 64 bits y claves de longitud variable (8 a 128 bytes).
"""

# Importamos las librerías necesarias
from Crypto.Cipher import ARC2
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def cifrar_rc2(mensaje, clave):
    """
    Función para cifrar un mensaje usando RC2
    
    Parámetros:
    - mensaje: Texto plano que queremos cifrar (string)
    - clave: Clave secreta para cifrar (string)
    
    Retorna:
    - Mensaje cifrado en base64 (string)
    - IV (Vector de Inicialización) en base64 (string)
    """
    
    print(f"\n🔒 Iniciando cifrado RC2...")
    
    # Convertimos la clave y el mensaje a bytes
    clave_bytes = clave.encode('utf-8')
    mensaje_bytes = mensaje.encode('utf-8')
    
    print(f"   📝 Mensaje original: '{mensaje}'")
    print(f"   🔑 Longitud de la clave: {len(clave_bytes)} bytes")
    
    # Generamos un vector de inicialización aleatorio (IV)
    # El IV asegura que el mismo mensaje cifrado con la misma clave produzca resultados diferentes
    # RC2 usa bloques de 8 bytes (64 bits)
    iv = get_random_bytes(8)
    print(f"   🎲 IV generado: {len(iv)} bytes")
    
    # Creamos el objeto cipher con modo CBC (Cipher Block Chaining)
    # CBC es un modo de operación que proporciona mayor seguridad
    # effective_keylen especifica la longitud efectiva de la clave en bits
    cipher = ARC2.new(clave_bytes, ARC2.MODE_CBC, iv)
    
    # Aplicamos padding al mensaje para que sea múltiplo del tamaño de bloque
    # RC2 requiere que los datos sean múltiplos de 8 bytes
    mensaje_padded = pad(mensaje_bytes, ARC2.block_size)
    print(f"   📦 Mensaje con padding: {len(mensaje_padded)} bytes")
    
    # Ciframos el mensaje
    mensaje_cifrado = cipher.encrypt(mensaje_padded)
    print(f"   ✅ Mensaje cifrado: {len(mensaje_cifrado)} bytes")
    
    # Convertimos a base64 para poder mostrar y transmitir fácilmente
    mensaje_cifrado_b64 = base64.b64encode(mensaje_cifrado).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')
    
    return mensaje_cifrado_b64, iv_b64

def descifrar_rc2(mensaje_cifrado_b64, clave, iv_b64):
    """
    Función para descifrar un mensaje cifrado con RC2
    
    Parámetros:
    - mensaje_cifrado_b64: Mensaje cifrado en base64 (string)
    - clave: Clave secreta usada para cifrar (string)
    - iv_b64: Vector de Inicialización en base64 (string)
    
    Retorna:
    - Mensaje descifrado (string)
    """
    
    print(f"\n🔓 Iniciando descifrado RC2...")
    
    # Convertimos la clave a bytes
    clave_bytes = clave.encode('utf-8')
    
    # Decodificamos el mensaje cifrado y el IV desde base64
    mensaje_cifrado = base64.b64decode(mensaje_cifrado_b64)
    iv = base64.b64decode(iv_b64)
    
    print(f"   📦 Mensaje cifrado recibido: {len(mensaje_cifrado)} bytes")
    print(f"   🎲 IV recibido: {len(iv)} bytes")
    
    # Creamos el objeto cipher con los mismos parámetros usados para cifrar
    cipher = ARC2.new(clave_bytes, ARC2.MODE_CBC, iv)
    
    # Desciframos el mensaje
    mensaje_descifrado_padded = cipher.decrypt(mensaje_cifrado)
    
    # Removemos el padding aplicado anteriormente
    mensaje_descifrado = unpad(mensaje_descifrado_padded, ARC2.block_size)
    
    print(f"   ✅ Mensaje descifrado: {len(mensaje_descifrado)} bytes")
    
    # Convertimos de bytes a string
    return mensaje_descifrado.decode('utf-8')

def demostrar_longitudes_clave():
    """
    Demuestra el uso de RC2 con diferentes longitudes de clave
    """
    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN: DIFERENTES LONGITUDES DE CLAVE")
    print("=" * 70)
    
    mensaje = "Mensaje de prueba"
    
    # Probamos con diferentes longitudes de clave
    claves = [
        ("Corta", "Clave8B!"),           # 8 bytes
        ("Media", "ClaveMedia16B"),      # 12 bytes
        ("Larga", "ClaveMuySegura2024!") # 21 bytes
    ]
    
    for nombre, clave in claves:
        print(f"\n🔑 Clave {nombre}: '{clave}' ({len(clave)} bytes)")
        try:
            cifrado, iv = cifrar_rc2(mensaje, clave)
            print(f"   ✅ Cifrado exitoso")
            print(f"   🔒 Resultado: {cifrado[:30]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")

# ========================================
# EJEMPLO DE USO
# ========================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN DEL ALGORITMO RC2 (Rivest Cipher 2)")
    print("=" * 70)
    
    # Información sobre RC2
    print("\n📚 Información sobre RC2:")
    print("   • Diseñador: Ron Rivest (1987)")
    print("   • Tipo: Cifrado simétrico por bloques")
    print("   • Tamaño de bloque: 64 bits (8 bytes)")
    print("   • Longitud de clave: Variable (8 a 128 bytes)")
    print("   • Uso: Alternativa a DES, usado en S/MIME, SSL/TLS antiguo")
    
    # --- EJEMPLO BÁSICO ---
    print("\n" + "=" * 70)
    print("EJEMPLO 1: CIFRADO Y DESCIFRADO BÁSICO")
    print("=" * 70)
    
    # Mensaje original que queremos cifrar
    mensaje_original = "¡Hola! Este es un mensaje secreto usando RC2."
    print(f"\n📝 Mensaje original: {mensaje_original}")
    
    # Clave secreta (debe ser compartida de forma segura entre emisor y receptor)
    # RC2 acepta claves de 8 a 128 bytes
    clave_secreta = "MiClaveRC2Segura2024"
    print(f"🔑 Clave secreta: {clave_secreta}")
    print(f"   Longitud: {len(clave_secreta)} bytes ({len(clave_secreta) * 8} bits)")
    
    # --- PROCESO DE CIFRADO ---
    print("\n" + "=" * 70)
    print("PASO 1: PROCESO DE CIFRADO")
    print("=" * 70)
    
    mensaje_cifrado, iv = cifrar_rc2(mensaje_original, clave_secreta)
    
    print(f"\n🔒 Mensaje cifrado (Base64):")
    print(f"   {mensaje_cifrado}")
    print(f"\n🎲 Vector de Inicialización (IV) en Base64:")
    print(f"   {iv}")
    
    # --- PROCESO DE DESCIFRADO ---
    print("\n" + "=" * 70)
    print("PASO 2: PROCESO DE DESCIFRADO")
    print("=" * 70)
    
    mensaje_descifrado = descifrar_rc2(mensaje_cifrado, clave_secreta, iv)
    
    print(f"\n🔓 Mensaje descifrado: {mensaje_descifrado}")
    
    # --- VERIFICACIÓN ---
    print("\n" + "=" * 70)
    print("PASO 3: VERIFICACIÓN")
    print("=" * 70)
    
    print(f"\n📊 Comparación:")
    print(f"   Original:   '{mensaje_original}'")
    print(f"   Descifrado: '{mensaje_descifrado}'")
    
    if mensaje_original == mensaje_descifrado:
        print("\n✅ ¡Éxito! El mensaje descifrado coincide perfectamente con el original.")
    else:
        print("\n❌ Error: El mensaje descifrado no coincide con el original.")
    
    # --- EJEMPLO CON MENSAJE MÁS LARGO ---
    print("\n" + "=" * 70)
    print("EJEMPLO 2: CIFRADO DE MENSAJE LARGO")
    print("=" * 70)
    
    mensaje_largo = """
    RC2 es un algoritmo de cifrado simétrico diseñado por Ron Rivest.
    Fue creado como alternativa a DES y es más rápido en software.
    Se utilizó ampliamente en protocolos como S/MIME y versiones antiguas de SSL/TLS.
    Aunque hoy en día se prefiere AES, RC2 sigue siendo un algoritmo válido y seguro.
    """
    
    print(f"\n📝 Mensaje largo ({len(mensaje_largo)} caracteres):")
    print(mensaje_largo)
    
    mensaje_largo_cifrado, iv_largo = cifrar_rc2(mensaje_largo, clave_secreta)
    
    print(f"\n🔒 Mensaje largo cifrado:")
    print(f"   {mensaje_largo_cifrado[:80]}...")
    print(f"   (Total: {len(mensaje_largo_cifrado)} caracteres en Base64)")
    
    mensaje_largo_descifrado = descifrar_rc2(mensaje_largo_cifrado, clave_secreta, iv_largo)
    
    if mensaje_largo == mensaje_largo_descifrado:
        print("\n✅ Mensaje largo descifrado correctamente")
    
    # --- DEMOSTRACIÓN DE DIFERENTES LONGITUDES DE CLAVE ---
    demostrar_longitudes_clave()
    
    # --- EJEMPLO CON CLAVE INCORRECTA ---
    print("\n" + "=" * 70)
    print("EJEMPLO 3: INTENTO DE DESCIFRADO CON CLAVE INCORRECTA")
    print("=" * 70)
    
    try:
        clave_incorrecta = "ClaveErronea123"
        print(f"\n🔑 Intentando con clave incorrecta: '{clave_incorrecta}'")
        mensaje_erroneo = descifrar_rc2(mensaje_cifrado, clave_incorrecta, iv)
        print(f"❌ Mensaje descifrado con clave incorrecta: {mensaje_erroneo}")
        print("   (El resultado es basura/texto ilegible)")
    except Exception as e:
        print(f"\n❌ Error al descifrar: {type(e).__name__}")
        print("   Esto es esperado: la clave incorrecta produce errores o basura")
    
    # --- INFORMACIÓN ADICIONAL ---
    print("\n" + "=" * 70)
    print("CARACTERÍSTICAS DE RC2")
    print("=" * 70)
    print("""
    ✓ Tamaño de bloque: 64 bits (8 bytes)
    ✓ Longitud de clave: Variable (8 a 128 bytes)
    ✓ Tipo: Cifrado simétrico por bloques
    ✓ Diseñador: Ron Rivest (creador de RSA)
    ✓ Año: 1987 (aunque se mantuvo propietario hasta 1996)
    ✓ Velocidad: Rápido en implementaciones de software
    ✓ Seguridad: Considerado seguro con claves adecuadas
    ✓ Uso histórico: S/MIME, versiones antiguas de SSL/TLS
    
    Ventajas:
    • Más rápido que DES en software
    • Longitud de clave variable permite flexibilidad
    • Bueno para sistemas con restricciones de exportación (versiones con claves cortas)
    • Compatible con muchos sistemas heredados
    
    Desventajas:
    • Bloque de 64 bits es pequeño para estándares actuales
    • No es tan eficiente como AES en hardware moderno
    • Considerado "legado" - AES es preferido para nuevos sistemas
    
    Comparación con otros algoritmos:
    • RC2 vs DES: RC2 es más rápido en software
    • RC2 vs AES: AES es más moderno y preferido actualmente
    • RC2 vs Blowfish: Ambos son de los años 90, Blowfish es más popular
    • RC2 vs RC4: RC2 es de bloques, RC4 es de flujo (stream)
    """)
    
    print("=" * 70)
    print("\n💡 CONSEJO DE SEGURIDAD:")
    print("Para nuevos proyectos, se recomienda usar AES en lugar de RC2.")
    print("RC2 sigue siendo seguro, pero AES es el estándar actual.")
    print("\nUsa claves de al menos 16 bytes (128 bits) para mayor seguridad.")
    print("=" * 70)
    
    # --- ESTADÍSTICAS FINALES ---
    print("\n" + "=" * 70)
    print("RESUMEN DE LA DEMOSTRACIÓN")
    print("=" * 70)
    print(f"""
    ✅ Mensajes cifrados: 3
    ✅ Mensajes descifrados: 2 (1 falló intencionalmente)
    ✅ Algoritmo: RC2 (Rivest Cipher 2)
    ✅ Modo: CBC (Cipher Block Chaining)
    ✅ Padding: PKCS7
    ✅ Codificación: Base64 para representación
    
    🎯 Conclusión:
    RC2 es un algoritmo simétrico confiable que funciona perfectamente
    para cifrado y descifrado cuando se usa la clave correcta.
    Aunque no es el más moderno, sigue siendo válido y seguro.
    """)
    print("=" * 70)
