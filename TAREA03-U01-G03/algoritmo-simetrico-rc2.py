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
import time
import os

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
    
    # Tamaños de archivos a probar (número de palabras)
    tamanos = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    
    for num_palabras in tamanos:
        nombre_archivo = f"mensaje_{num_palabras}_palabras.txt"
        
        print(f"\n{'=' * 70}")
        print(f"PROCESANDO ARCHIVO: {nombre_archivo}")
        print(f"{'=' * 70}")
        
        # 1. Leer archivo
        inicio = time.time()
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                mensaje = f.read()
            tiempo_lectura = time.time() - inicio
            print(f"1. Lectura completada - Tiempo: {tiempo_lectura:.6f} segundos")
            print(f"   Caracteres leídos: {len(mensaje)}")
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo {nombre_archivo}")
            continue
        
        # 2. Generar clave
        inicio = time.time()
        clave = get_random_bytes(16)  # 128 bits
        tiempo_clave = time.time() - inicio
        print(f"\n2. Clave generada - Tiempo: {tiempo_clave:.6f} segundos")
        print(f"   Clave (hex): {clave.hex()[:40]}...")
        
        # 3. Cifrar
        inicio = time.time()
        mensaje_bytes = mensaje.encode('utf-8')
        iv = get_random_bytes(8)
        cipher = ARC2.new(clave, ARC2.MODE_CBC, iv)
        mensaje_padded = pad(mensaje_bytes, ARC2.block_size)
        mensaje_cifrado = cipher.encrypt(mensaje_padded)
        tiempo_cifrado = time.time() - inicio
        print(f"\n3. Cifrado completado - Tiempo: {tiempo_cifrado:.6f} segundos")
        print(f"   Bytes cifrados: {len(mensaje_cifrado)}")
        print(f"   Cifrado (hex): {mensaje_cifrado.hex()[:40]}...")
        
        # 4. Descifrar
        inicio = time.time()
        cipher = ARC2.new(clave, ARC2.MODE_CBC, iv)
        mensaje_descifrado_padded = cipher.decrypt(mensaje_cifrado)
        mensaje_descifrado = unpad(mensaje_descifrado_padded, ARC2.block_size).decode('utf-8')
        tiempo_descifrado = time.time() - inicio
        print(f"\n4. Descifrado completado - Tiempo: {tiempo_descifrado:.6f} segundos")
        print(f"   Verificación: {'OK' if mensaje == mensaje_descifrado else 'ERROR'}")
        
        print(f"\nTIEMPO TOTAL: {tiempo_lectura + tiempo_clave + tiempo_cifrado + tiempo_descifrado:.6f} segundos")
    
    print(f"\n{'=' * 70}")
    print("PROCESO COMPLETADO")
    print(f"{'=' * 70}")
