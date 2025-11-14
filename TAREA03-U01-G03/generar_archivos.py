"""
Script para generar archivos de texto con diferentes cantidades de palabras
"""

def generar_archivo(num_palabras, nombre_archivo):
    """
    Genera un archivo de texto con la cantidad especificada de palabras
    """
    # Palabra base para repetir
    palabra = "palabra "
    
    print(f"Generando {nombre_archivo} con {num_palabras} palabras...")
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        # Escribir en bloques para eficiencia
        bloque_size = 10000
        palabras_escritas = 0
        
        while palabras_escritas < num_palabras:
            # Calcular cuántas palabras escribir en este bloque
            palabras_en_bloque = min(bloque_size, num_palabras - palabras_escritas)
            
            # Escribir el bloque
            f.write(palabra * palabras_en_bloque)
            
            palabras_escritas += palabras_en_bloque
            
            # Mostrar progreso para archivos grandes
            if num_palabras >= 100000 and palabras_escritas % 100000 == 0:
                print(f"  Progreso: {palabras_escritas}/{num_palabras} palabras")
    
    print(f"  ✓ Completado: {nombre_archivo}\n")

if __name__ == "__main__":
    print("=" * 70)
    print("GENERANDO ARCHIVOS DE PRUEBA")
    print("=" * 70)
    print()
    
    # Tamaños de archivos a generar
    tamanos = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    
    for num_palabras in tamanos:
        nombre_archivo = f"mensaje_{num_palabras}_palabras.txt"
        generar_archivo(num_palabras, nombre_archivo)
    
    print("=" * 70)
    print("TODOS LOS ARCHIVOS GENERADOS EXITOSAMENTE")
    print("=" * 70)
