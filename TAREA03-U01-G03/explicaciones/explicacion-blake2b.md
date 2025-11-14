# BLAKE2b - Función Hash Criptográfica

## ¿Qué es BLAKE2b?

BLAKE2b es una función hash criptográfica de alta velocidad diseñada como una mejora de BLAKE, finalista del concurso SHA-3. Es más rápida que MD5, SHA-1, SHA-2 y SHA-3, mientras mantiene un nivel de seguridad equivalente a SHA-3.

## Características Principales

### 1. **Velocidad**
- Optimizado para plataformas de 64 bits
- Más rápido que SHA-256 y SHA-512
- Comparable en velocidad a MD5 sin comprometer seguridad

### 2. **Seguridad**
- Tamaño de hash: hasta 512 bits (64 bytes)
- Sin vulnerabilidades conocidas
- Resistente a colisiones, pre-imagen y segunda pre-imagen
- Diseño basado en ChaCha (cifrado de Dan Bernstein)

### 3. **Flexibilidad**
- Tamaño de salida configurable: 1 a 64 bytes
- Soporte para autenticación con clave (MAC)
- Personalización mediante salt y personalización

### 4. **Simplicidad**
- Implementación más simple que SHA-3
- Menos operaciones que SHA-2
- Sin tablas de búsqueda

## ¿Cómo Funciona BLAKE2b?

### Proceso General

```
Entrada (mensaje) → Padding → Compresión → Hash Final
```

### 1. **Inicialización**
BLAKE2b comienza con un vector de inicialización (IV) de 8 palabras de 64 bits:

```
h[0..7] = IV[0..7] XOR parámetros
```

Los parámetros incluyen:
- Tamaño del hash deseado
- Clave (si se usa)
- Salt
- Personalización

### 2. **Padding del Mensaje**
El mensaje se divide en bloques de 128 bytes:
- Si el mensaje no es múltiplo de 128, se rellena con ceros
- El último bloque se marca con una bandera especial

### 3. **Función de Compresión**
Para cada bloque, se ejecutan **12 rondas** de transformación:

```
Para cada bloque:
    Para cada ronda (0 a 11):
        - Mezcla columnas
        - Mezcla diagonales
        - Aplica rotaciones
        - Usa constantes específicas
```

#### Operaciones básicas:
- **XOR** (⊕): Suma exclusiva bit a bit
- **Adición modular** (+): Suma módulo 2^64
- **Rotación** (>>>): Rotación de bits

### 4. **Función G (Mezcla)**
La función G es el corazón de BLAKE2b:

```python
def G(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) mod 2^64
    v[d] = (v[d] ⊕ v[a]) >>> 32
    v[c] = (v[c] + v[d]) mod 2^64
    v[b] = (v[b] ⊕ v[c]) >>> 24
    v[a] = (v[a] + v[b] + y) mod 2^64
    v[d] = (v[d] ⊕ v[a]) >>> 16
    v[c] = (v[c] + v[d]) mod 2^64
    v[b] = (v[b] ⊕ v[c]) >>> 63
```

### 5. **Finalización**
Después de procesar todos los bloques:
- Se aplica XOR entre el estado interno y el IV modificado
- Se extrae el número de bytes solicitado como hash final

## Propiedades Criptográficas

### 1. **Efecto Avalancha**
Un pequeño cambio en la entrada produce un cambio drástico en la salida:

```
Entrada:  "blockchain"
Hash:     e4f5a6b7c8d9...

Entrada:  "Blockchain"  (solo una mayúscula)
Hash:     12a3b4c5d6e7...  (completamente diferente)
```

### 2. **Determinismo**
La misma entrada siempre produce el mismo hash:

```
hash("mensaje") == hash("mensaje")  // Siempre True
```

### 3. **Irreversibilidad**
Es computacionalmente imposible obtener el mensaje original desde el hash:

```
hash → mensaje  // Imposible sin fuerza bruta
```

### 4. **Resistencia a Colisiones**
Es extremadamente difícil encontrar dos mensajes con el mismo hash:

```
Probabilidad de colisión ≈ 2^(-256) para BLAKE2b-512
```

## Casos de Uso

### 1. **Verificación de Integridad**
```python
# Generar hash del archivo original
hash_original = generar_hash_archivo("documento.pdf")

# Verificar después
hash_actual = generar_hash_archivo("documento.pdf")
if hash_original == hash_actual:
    print("Archivo íntegro")
```

### 2. **Autenticación de Mensajes (MAC)**
```python
# Con clave secreta compartida
hash_mac = generar_hash_blake2b(mensaje, key="secreto")

# Solo quien conoce la clave puede verificar
```

### 3. **Identificación de Datos**
```python
# Hash único para identificar contenido
hash_id = generar_hash_blake2b(contenido, digest_size=16)
# Usar como ID único de 128 bits
```

### 4. **Blockchain y Criptomonedas**
- Verificación de bloques
- Prueba de trabajo (menos común, pero posible)
- Merkle trees

### 5. **Almacenamiento de Contraseñas**
```python
# Nunca guardar contraseñas en texto plano
hash_password = generar_hash_blake2b(password, key=salt)
```

## Ventajas de BLAKE2b

| Característica | BLAKE2b | SHA-256 | SHA-3 | MD5 |
|---------------|---------|---------|-------|-----|
| Velocidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Seguridad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Flexibilidad | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| Simplicidad | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

### Por qué elegir BLAKE2b:
✅ **Más rápido** que SHA-2 y SHA-3  
✅ **Igualmente seguro** que SHA-3  
✅ **Configurable** en tamaño y con soporte MAC  
✅ **Sin patentes** ni restricciones  
✅ **Ampliamente adoptado** (Argon2, WireGuard, etc.)

## Comparación con Otras Funciones Hash

### BLAKE2b vs SHA-256
- **Velocidad**: BLAKE2b es ~2-3x más rápido
- **Seguridad**: Ambos seguros, BLAKE2b más moderno
- **Uso**: SHA-256 más común en blockchain, BLAKE2b en aplicaciones nuevas

### BLAKE2b vs MD5
- **Seguridad**: MD5 está roto, BLAKE2b seguro
- **Velocidad**: Comparable
- **Uso**: Nunca usar MD5 para seguridad

### BLAKE2b vs SHA-3
- **Velocidad**: BLAKE2b más rápido
- **Seguridad**: Ambos seguros
- **Diseño**: Diferentes arquitecturas (ARX vs. Esponja)

## Implementación en Python

### Uso Básico
```python
import hashlib

# Hash simple
mensaje = "Hola mundo"
hash_obj = hashlib.blake2b(mensaje.encode())
print(hash_obj.hexdigest())
```

### Con Tamaño Personalizado
```python
# Hash de 256 bits (32 bytes)
hash_obj = hashlib.blake2b(mensaje.encode(), digest_size=32)
```

### Con Clave (MAC)
```python
# Hash autenticado
clave = b"mi_clave_secreta"
hash_obj = hashlib.blake2b(mensaje.encode(), key=clave)
```

## Variantes de BLAKE2

### BLAKE2b
- Optimizado para **plataformas de 64 bits**
- Tamaño de bloque: 128 bytes
- Hash máximo: 512 bits (64 bytes)
- Ideal para: servidores, escritorio

### BLAKE2s
- Optimizado para **plataformas de 8-32 bits**
- Tamaño de bloque: 64 bytes
- Hash máximo: 256 bits (32 bytes)
- Ideal para: IoT, móviles, sistemas embebidos

## Parámetros Configurables

```python
hashlib.blake2b(
    data,              # Datos a hashear
    digest_size=64,    # Tamaño del hash (1-64 bytes)
    key=b'',          # Clave para MAC (0-64 bytes)
    salt=b'',         # Salt (0-16 bytes)
    person=b'',       # Personalización (0-16 bytes)
    fanout=1,         # Para hashing en árbol
    depth=1,          # Profundidad del árbol
    leaf_size=0,      # Tamaño de hoja
    node_offset=0,    # Offset del nodo
    node_depth=0,     # Profundidad del nodo
    inner_size=0,     # Tamaño interno
    last_node=False   # Bandera de último nodo
)
```

## Seguridad y Mejores Prácticas

### ✅ Hacer:
- Usar BLAKE2b para nuevas aplicaciones
- Configurar tamaño apropiado según necesidad
- Usar clave para autenticación
- Actualizar regularmente implementaciones

### ❌ Evitar:
- Usar tamaños muy pequeños (< 16 bytes) para seguridad
- Reutilizar claves en diferentes contextos
- Asumir que hash = encriptación
- Usar solo hash para almacenar contraseñas (usar también KDF)

## Recursos Adicionales

- **RFC 7693**: Especificación oficial de BLAKE2
- **BLAKE2 Website**: https://www.blake2.net/
- **Código fuente**: https://github.com/BLAKE2/BLAKE2
- **Paper original**: "BLAKE2: simpler, smaller, fast as MD5"

## Conclusión

BLAKE2b representa el estado del arte en funciones hash criptográficas, combinando:
- **Velocidad excepcional**
- **Seguridad robusta**
- **Flexibilidad sin precedentes**
- **Simplicidad de implementación**

Es la elección ideal para aplicaciones modernas que requieren hashing rápido y seguro, desde verificación de integridad hasta autenticación de mensajes y más allá.
