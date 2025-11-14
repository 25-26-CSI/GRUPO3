"""
Implementación de la función hash BLAKE2b
BLAKE2b es una función hash criptográfica rápida y segura
"""

import hashlib
import os
import time


def generar_hash_blake2b(mensaje, digest_size=64, key=None):
    """
    Genera un hash BLAKE2b de un mensaje.
    
    Parámetros:
    - mensaje (str o bytes): El mensaje a hashear
    - digest_size (int): Tamaño del hash en bytes (1-64, por defecto 64)
    - key (bytes): Clave opcional para hash autenticado (0-64 bytes)
    
    Retorna:
    - str: Hash en formato hexadecimal
    """
    # Convertir mensaje a bytes si es string
    if isinstance(mensaje, str):
        mensaje = mensaje.encode('utf-8')
    
    # Crear objeto hash BLAKE2b
    if key:
        if isinstance(key, str):
            key = key.encode('utf-8')
        hash_obj = hashlib.blake2b(mensaje, digest_size=digest_size, key=key)
    else:
        hash_obj = hashlib.blake2b(mensaje, digest_size=digest_size)
    
    return hash_obj.hexdigest()


def generar_hash_archivo(ruta_archivo, digest_size=64):
    """
    Genera un hash BLAKE2b de un archivo.
    
    Parámetros:
    - ruta_archivo (str): Ruta al archivo
    - digest_size (int): Tamaño del hash en bytes (1-64, por defecto 64)
    
    Retorna:
    - str: Hash en formato hexadecimal
    """
    hash_obj = hashlib.blake2b(digest_size=digest_size)
    
    # Leer archivo en bloques para eficiencia con archivos grandes
    with open(ruta_archivo, 'rb') as f:
        for bloque in iter(lambda: f.read(4096), b''):
            hash_obj.update(bloque)
    
    return hash_obj.hexdigest()


def verificar_integridad(mensaje, hash_esperado, digest_size=64, key=None):
    """
    Verifica la integridad de un mensaje comparando su hash.
    
    Parámetros:
    - mensaje (str o bytes): El mensaje a verificar
    - hash_esperado (str): Hash esperado en formato hexadecimal
    - digest_size (int): Tamaño del hash en bytes
    - key (bytes): Clave opcional
    
    Retorna:
    - bool: True si el hash coincide, False en caso contrario
    """
    hash_calculado = generar_hash_blake2b(mensaje, digest_size, key)
    return hash_calculado == hash_esperado


def demostrar_blake2b():
    """
    Función de demostración de las capacidades de BLAKE2b
    """
    print("=" * 60)
    print("DEMOSTRACIÓN DE BLAKE2b")
    print("=" * 60)
    
    # 1. Hash básico
    print("\n1. Hash básico de un mensaje:")
    mensaje1 = "Hola, este es un mensaje de prueba"
    hash1 = generar_hash_blake2b(mensaje1)
    print(f"Mensaje: {mensaje1}")
    print(f"Hash BLAKE2b (512 bits): {hash1}")
    
    # 2. Hash con tamaño personalizado
    print("\n2. Hash con tamaño personalizado (256 bits):")
    hash2 = generar_hash_blake2b(mensaje1, digest_size=32)
    print(f"Hash BLAKE2b (256 bits): {hash2}")
    
    # 3. Hash autenticado con clave (MAC)
    print("\n3. Hash autenticado con clave (MAC):")
    clave = "mi_clave_secreta"
    hash3 = generar_hash_blake2b(mensaje1, key=clave)
    print(f"Clave: {clave}")
    print(f"Hash autenticado: {hash3}")
    
    # 4. Verificación de integridad
    print("\n4. Verificación de integridad:")
    es_valido = verificar_integridad(mensaje1, hash1)
    print(f"¿Hash coincide? {es_valido}")
    
    # Modificar mensaje y verificar
    mensaje_modificado = "Hola, este es un mensaje modificado"
    es_valido_mod = verificar_integridad(mensaje_modificado, hash1)
    print(f"¿Hash coincide con mensaje modificado? {es_valido_mod}")
    
    # 5. Efecto avalancha - pequeño cambio en entrada
    print("\n5. Efecto avalancha (pequeño cambio en la entrada):")
    mensaje_a = "blockchain"
    mensaje_b = "Blockchain"  # Solo una letra mayúscula
    hash_a = generar_hash_blake2b(mensaje_a, digest_size=32)
    hash_b = generar_hash_blake2b(mensaje_b, digest_size=32)
    print(f"Mensaje A: '{mensaje_a}'")
    print(f"Hash A:    {hash_a}")
    print(f"Mensaje B: '{mensaje_b}'")
    print(f"Hash B:    {hash_b}")
    
    # 6. Comparación de velocidad - múltiples iteraciones
    print("\n6. Hash de diferentes tipos de datos:")
    import json
    
    # Hash de datos JSON
    datos = {"usuario": "admin", "timestamp": "2025-11-14", "accion": "login"}
    datos_json = json.dumps(datos, sort_keys=True)
    hash_json = generar_hash_blake2b(datos_json, digest_size=32)
    print(f"Datos: {datos_json}")
    print(f"Hash: {hash_json}")
    
    # 7. Hash de bytes aleatorios
    print("\n7. Hash de datos binarios aleatorios:")
    datos_aleatorios = os.urandom(32)
    hash_aleatorio = generar_hash_blake2b(datos_aleatorios, digest_size=32)
    print(f"Datos (hex): {datos_aleatorios.hex()}")
    print(f"Hash: {hash_aleatorio}")
    
    print("\n" + "=" * 60)
    print("CARACTERÍSTICAS DE BLAKE2b:")
    print("=" * 60)
    print("✓ Velocidad: Más rápido que MD5, SHA-1, SHA-2 y SHA-3")
    print("✓ Seguridad: Tan seguro como SHA-3")
    print("✓ Tamaño de hash: Configurable de 1 a 64 bytes")
    print("✓ Soporta clave para autenticación (MAC)")
    print("✓ Diseñado para plataformas de 64 bits")
    print("✓ Sin vulnerabilidades conocidas")
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN DE BLAKE2b")
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
        
        # 2. Generar "clave" (para BLAKE2b, usamos un parámetro salt/key opcional)
        inicio = time.time()
        key = os.urandom(32)  # Clave de 256 bits
        tiempo_clave = time.time() - inicio
        print(f"\n2. Clave generada - Tiempo: {tiempo_clave:.6f} segundos")
        print(f"   Clave (hex): {key.hex()[:40]}...")
        
        # 3. Calcular hash (equivalente a "cifrar" para funciones hash)
        inicio = time.time()
        hash_resultado = generar_hash_blake2b(mensaje, digest_size=64, key=key)
        tiempo_hash = time.time() - inicio
        print(f"\n3. Hash calculado - Tiempo: {tiempo_hash:.6f} segundos")
        print(f"   Hash BLAKE2b: {hash_resultado[:80]}...")
        
        # 4. Verificar integridad (equivalente a "descifrar")
        inicio = time.time()
        es_valido = verificar_integridad(mensaje, hash_resultado, digest_size=64, key=key)
        tiempo_verificacion = time.time() - inicio
        print(f"\n4. Verificación completada - Tiempo: {tiempo_verificacion:.6f} segundos")
        print(f"   Verificación: {'OK' if es_valido else 'ERROR'}")
        
        print(f"\nTIEMPO TOTAL: {tiempo_lectura + tiempo_clave + tiempo_hash + tiempo_verificacion:.6f} segundos")
    
    print(f"\n{'=' * 70}")
    print("PROCESO COMPLETADO")
    print(f"{'=' * 70}")
