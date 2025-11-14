# Resultados de Análisis de Algoritmos Criptográficos

## Tabla Resumen de Resultados

### Algoritmo: RC2 (Cifrado Simétrico)

| #palabras | #caracteres_entrada | #caracteres_salida | T-E1 (Lectura) | T-E2 (Clave) | T-E3 (Cifrado) | T-E4 (Descifrado) | T-Total |
|-----------|--------------------|--------------------|----------------|--------------|----------------|-------------------|---------|
| 10 | 80 | 88 | 0.000103 s | 0.000011 s | 0.017250 s | 0.000054 s | 0.017418 s |
| 100 | 800 | 808 | 0.000159 s | 0.000004 s | 0.000065 s | 0.000038 s | 0.000266 s |
| 1,000 | 8,000 | 8,008 | 0.000132 s | 0.000001 s | 0.000167 s | 0.000088 s | 0.000389 s |
| 10,000 | 80,000 | 80,008 | 0.011731 s | 0.000004 s | 0.001348 s | 0.000634 s | 0.013717 s |
| 100,000 | 800,000 | 800,008 | 0.011285 s | 0.000010 s | 0.013599 s | 0.006824 s | 0.031718 s |
| 1,000,000 | 8,000,000 | 8,000,008 | 0.018370 s | 0.000010 s | 0.126751 s | 0.067015 s | 0.212146 s |
| 10,000,000 | 80,000,000 | 80,000,008 | 0.058689 s | 0.000007 s | 1.275784 s | 0.655113 s | 1.989593 s |

### Algoritmo: NTRU (Cifrado Asimétrico)

| #palabras | #caracteres_entrada | #caracteres_salida | T-E1 (Lectura) | T-E2 (Clave) | T-E3 (Cifrado) | T-E4 (Descifrado) | T-Total |
|-----------|--------------------|--------------------|----------------|--------------|----------------|-------------------|---------|
| 10 | 80 | 11 | 0.000090 s | 0.000140 s | 0.000054 s | 0.000049 s | 0.000334 s |
| 100 | 800 | 11 | 0.000092 s | 0.000056 s | 0.000032 s | 0.000028 s | 0.000207 s |
| 1,000 | 8,000 | 11 | 0.000118 s | 0.000039 s | 0.000058 s | 0.000123 s | 0.000338 s |
| 10,000 | 80,000 | 11 | 0.000149 s | 0.000048 s | 0.000028 s | 0.000038 s | 0.000263 s |
| 100,000 | 800,000 | 11 | 0.000575 s | 0.000045 s | 0.000045 s | 0.000040 s | 0.000703 s |
| 1,000,000 | 8,000,000 | 11 | 0.006236 s | 0.000123 s | 0.000057 s | 0.000073 s | 0.006489 s |
| 10,000,000 | 80,000,000 | 11 | 0.055605 s | 0.000123 s | 0.000067 s | 0.000038 s | 0.055833 s |

**Nota:** NTRU solo cifra los primeros 11 caracteres debido a la limitación del parámetro N=11 del algoritmo.

### Algoritmo: BLAKE2b (Función Hash)

| #palabras | #caracteres_entrada | #caracteres_salida | T-E1 (Lectura) | T-E2 (Clave) | T-E3 (Hash) | T-E4 (Verificación) | T-Total |
|-----------|--------------------|--------------------|----------------|--------------|-------------|---------------------|---------|
| 10 | 80 | 128 | 0.000109 s | 0.000008 s | 0.000013 s | 0.000007 s | 0.000137 s |
| 100 | 800 | 128 | 0.000109 s | 0.000005 s | 0.000005 s | 0.000003 s | 0.000123 s |
| 1,000 | 8,000 | 128 | 0.000084 s | 0.000001 s | 0.000015 s | 0.000013 s | 0.000113 s |
| 10,000 | 80,000 | 128 | 0.000162 s | 0.000004 s | 0.000075 s | 0.000086 s | 0.000328 s |
| 100,000 | 800,000 | 128 | 0.000568 s | 0.000001 s | 0.000942 s | 0.000957 s | 0.002468 s |
| 1,000,000 | 8,000,000 | 128 | 0.007108 s | 0.000005 s | 0.009147 s | 0.009313 s | 0.025573 s |
| 10,000,000 | 80,000,000 | 128 | 0.057523 s | 0.000010 s | 0.100355 s | 0.095628 s | 0.253516 s |

**Nota:** La salida de BLAKE2b es el hash de 512 bits (64 bytes) representado en hexadecimal (128 caracteres).

---

## Análisis Comparativo

### Tiempos Totales por Algoritmo (10M palabras)

| Algoritmo | Tiempo Total | Operación Principal |
|-----------|--------------|---------------------|
| RC2 | 1.989593 s | Cifrado simétrico completo |
| NTRU | 0.055833 s | Cifrado asimétrico (solo 11 caracteres) |
| BLAKE2b | 0.253516 s | Generación de hash |

### Observaciones

1. **RC2**: El tiempo de cifrado crece linealmente con el tamaño del archivo. Es el más lento para archivos grandes debido al procesamiento completo del contenido.

2. **NTRU**: Tiempos constantes independientes del tamaño de entrada porque solo procesa los primeros 11 caracteres. La lectura del archivo es la etapa dominante.

3. **BLAKE2b**: Excelente rendimiento para generar hashes de archivos grandes. Aproximadamente 8x más rápido que RC2 para 10M palabras.

### Etapas más costosas

- **RC2**: Cifrado (E3) y Descifrado (E4) dominan el tiempo total
- **NTRU**: Lectura del archivo (E1) es la etapa dominante
- **BLAKE2b**: Generación de hash (E3) y Verificación (E4) tienen tiempos similares

---

*Generado el 14 de noviembre de 2025*
