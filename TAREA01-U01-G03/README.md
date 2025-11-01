# Proyecto de Cifrado Clásico

## Integrantes

- **Ariel Elizalde**
- **Mauricio López**
- **Alexis Troya**

---

## Descripción del Proyecto

Este proyecto implementa dos métodos clásicos de cifrado: **Cifrado por Permutación** y **Cifrado por Sustitución**. Ambos métodos representan técnicas fundamentales en criptografía que han sido utilizadas históricamente para proteger información sensible.

---

## Métodos Implementados

### 1. Cifrado por Permutación (Transposición de Caracteres)

El **Cifrado por Permutación**, también conocido como **Cifrado por Transposición**, reordena las posiciones de los caracteres en el texto original según una clave numérica.

#### Características:
- Las letras **permanecen iguales**, solo cambian de posición
- Utiliza una **clave numérica** que define el orden de transposición
- El texto se divide en bloques del tamaño de la clave
- La misma clave con proceso inverso permite descifrar el mensaje

#### Ejemplo:
```
Texto original:   ATAQUE
Clave:            [3, 1, 2]
Bloques:          ATA → AAT
                  QUE → EQU
Resultado:        AATEQU
```

---

### 2. Cifrado por Sustitución (Cifrado César)

El **Cifrado por Sustitución**, también conocido como **Cifrado César**, reemplaza cada letra del texto por otra letra del alfabeto según un desplazamiento fijo.

#### Características:
- Las **posiciones permanecen iguales**, pero las letras cambian
- Utiliza un **desplazamiento numérico** en el alfabeto
- Mantiene la distinción entre mayúsculas y minúsculas
- No modifica caracteres especiales (espacios, puntuación, números)
- Proceso simétrico: el desplazamiento negativo descifra el mensaje

#### Ejemplo:
```
Texto original:   HELLO
Desplazamiento:   3
Proceso:          H → K, E → H, L → O, L → O, O → R
Resultado:        KHOOR
```

---

## Archivos del Proyecto

- `Permutacion_Cifrada.ipynb` - Implementación del cifrado por permutación
- `Sustitución_Cifrada.ipynb` - Implementación del cifrado por sustitución
- `README.md` - Documentación del proyecto

---

## Uso

Cada notebook contiene:
- Explicación teórica del método
- Implementación en Python
- Ejemplos de uso
- Funciones para cifrar y descifrar

Ejecuta las celdas de código en orden para ver los ejemplos en funcionamiento.

---

## Tecnologías Utilizadas

- Python 3
- Jupyter Notebook
- Biblioteca `pycipher` (para ejemplos adicionales en Cifrado César)
