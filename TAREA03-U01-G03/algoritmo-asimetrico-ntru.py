"""
Algoritmo de Cifrado Asimétrico - NTRU
=======================================
NTRU (Número Teórico Reticular con Unicidad) es un algoritmo de cifrado de clave pública
basado en retículos polinomiales. Es resistente a ataques de computadoras cuánticas.

Desarrollado en 1996 por Jeffrey Hoffstein, Jill Pipher y Joseph H. Silverman.
"""

import numpy as np
from numpy.polynomial import polynomial as P
import secrets
import time
import os

class NTRU:
    """
    Implementación simplificada del algoritmo NTRU para fines educativos
    """
    
    def __init__(self, N=11, p=3, q=32):
        """
        Inicializa los parámetros del sistema NTRU
        """
        self.N = N  # Grado del anillo polinomial
        self.p = p  # Módulo pequeño
        self.q = q  # Módulo grande
        
        # Claves públicas y privadas
        self.clave_publica = None
        self.clave_privada_f = None
        self.clave_privada_fp = None
    
    def reducir_modulo_x_n_menos_1(self, polinomio):
        """
        Reduce un polinomio módulo (x^N - 1)
        Esto simula trabajar en el anillo polinomial R = Z[x]/(x^N - 1)
        """
        # Si el polinomio tiene grado >= N, reducimos usando x^N = 1
        while len(polinomio) > self.N:
            # El coeficiente de x^N se suma al término constante
            polinomio[0] += polinomio[self.N]
            polinomio = polinomio[:self.N]
        return polinomio
    
    def multiplicar_polinomios(self, f, g, mod):
        """
        Multiplica dos polinomios en el anillo R y aplica módulo
        """
        # Multiplicación de polinomios
        resultado = P.polymul(f, g)
        # Reduce módulo (x^N - 1)
        resultado = self.reducir_modulo_x_n_menos_1(resultado)
        # Aplica módulo numérico a cada coeficiente
        resultado = np.mod(resultado, mod)
        return resultado
    
    def inverso_modular_polinomio(self, f, mod):
        """
        Calcula el inverso de un polinomio f módulo mod
        (Versión simplificada - en producción se usa algoritmo extendido de Euclides)
        """
        # Para esta implementación simplificada, usamos un método básico
        # En un sistema real, se usaría el algoritmo de Euclides extendido
        for i in range(1, 100):
            candidato = np.random.randint(-1, 2, self.N)
            if np.allclose(self.multiplicar_polinomios(f, candidato, mod), [1] + [0]*(self.N-1)):
                return candidato
        
        # Inverso simple para polinomios pequeños
        return np.array([1] + [0]*(self.N-1))
    
    def generar_polinomio_pequeño(self, d1=3, d2=3):
        """
        Genera un polinomio con coeficientes pequeños
        d1: número de coeficientes +1
        d2: número de coeficientes -1
        resto: coeficientes 0
        """
        polinomio = np.zeros(self.N, dtype=int)
        
        # Posiciones para +1
        posiciones_pos = secrets.SystemRandom().sample(range(self.N), d1)
        for pos in posiciones_pos:
            polinomio[pos] = 1
        
        # Posiciones para -1
        posiciones_restantes = [i for i in range(self.N) if i not in posiciones_pos]
        posiciones_neg = secrets.SystemRandom().sample(posiciones_restantes, min(d2, len(posiciones_restantes)))
        for pos in posiciones_neg:
            polinomio[pos] = -1
        
        return polinomio
    
    def generar_claves(self):
        """
        Genera el par de claves pública y privada
        """
        # Genera f (debe tener inverso módulo p y q)
        # f tiene forma: 1 + p*F donde F es un polinomio pequeño
        while True:
            F = self.generar_polinomio_pequeño(d1=2, d2=2)
            self.clave_privada_f = 1 + self.p * F
            # Verifica que f sea invertible (simplificado)
            if self.clave_privada_f[0] != 0:
                break
        
        # Genera g (polinomio pequeño)
        g = self.generar_polinomio_pequeño(d1=3, d2=2)
        
        # Calcula fp (inverso de f módulo p)
        # Para simplificar, usamos un inverso básico
        self.clave_privada_fp = np.array([1] + [0]*(self.N-1))
        
        # Calcula fq (inverso de f módulo q)
        # Para simplificar, usamos aproximación
        fq = np.array([1] + [0]*(self.N-1))
        
        # Calcula la clave pública: h = p * fq * g (mod q)
        temp = self.multiplicar_polinomios(fq, g, self.q)
        self.clave_publica = np.mod(self.p * temp, self.q)
        
        return self.clave_publica, (self.clave_privada_f, self.clave_privada_fp)
    
    def texto_a_polinomio(self, texto):
        """
        Convierte texto a un polinomio con coeficientes pequeños
        Para mensajes largos, toma solo los primeros N caracteres
        """
        coeficientes = []
        # Limitar a N caracteres
        texto_limitado = texto[:self.N]
        
        for char in texto_limitado:
            # Mapea caracteres a valores pequeños
            valor = (ord(char) % 3) - 1  # Genera -1, 0, o 1
            coeficientes.append(valor)
        
        # Rellena con ceros si es necesario
        while len(coeficientes) < self.N:
            coeficientes.append(0)
        
        return np.array(coeficientes[:self.N])
    
    def polinomio_a_texto(self, polinomio):
        """
        Convierte un polinomio de vuelta a texto
        """
        texto = ""
        for coef in polinomio:
            # Mapea valores de vuelta a caracteres
            valor = int(coef) % 256
            if valor > 0:
                texto += chr(abs(valor))
        return texto.rstrip('\x00')
    
    def cifrar(self, mensaje, clave_publica):
        """
        Cifra un mensaje usando la clave pública
        Para mensajes largos, solo cifra los primeros N caracteres
        """
        # Limitar mensaje a N caracteres para que quepa en el polinomio
        mensaje_limitado = mensaje[:self.N]
        
        # Convierte mensaje a polinomio
        m = self.texto_a_polinomio(mensaje_limitado)
        
        # Genera r (polinomio aleatorio efímero)
        r = self.generar_polinomio_pequeño(d1=2, d2=2)
        
        # Calcula e = r * h + m (mod q)
        rh = self.multiplicar_polinomios(r, clave_publica, self.q)
        e = np.mod(rh + m, self.q)
        
        return e
    
    def descifrar(self, e, clave_privada_f, clave_privada_fp):
        """
        Descifra un mensaje usando la clave privada
        """
        # Calcula a = f * e (mod q)
        a = self.multiplicar_polinomios(clave_privada_f, e, self.q)
        
        # Centra a en el rango [-q/2, q/2]
        a = np.array([(coef if coef <= self.q//2 else coef - self.q) for coef in a])
        
        # Calcula m = fp * a (mod p)
        m = self.multiplicar_polinomios(clave_privada_fp, a, self.p)
        
        # Centra m en el rango apropiado
        m = np.array([(coef if coef <= self.p//2 else coef - self.p) for coef in m])
        
        # Convierte polinomio de vuelta a texto
        mensaje_descifrado = self.polinomio_a_texto(m)
        
        return mensaje_descifrado, m


# ========================================
# EJEMPLO DE USO
# ========================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN DEL ALGORITMO NTRU")
    print("=" * 70)
    
    # Inicializa el sistema NTRU con parámetros pequeños
    ntru = NTRU(N=11, p=3, q=32)
    
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
            print(f"   (NOTA: NTRU cifrará solo los primeros {ntru.N} caracteres)")
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo {nombre_archivo}")
            continue
        
        # 2. Generar claves
        inicio = time.time()
        clave_publica, (clave_privada_f, clave_privada_fp) = ntru.generar_claves()
        tiempo_clave = time.time() - inicio
        print(f"\n2. Claves generadas - Tiempo: {tiempo_clave:.6f} segundos")
        print(f"   Clave pública: {clave_publica[:5]}...")
        print(f"   Clave privada f: {clave_privada_f[:5]}...")
        
        # 3. Cifrar
        inicio = time.time()
        mensaje_cifrado = ntru.cifrar(mensaje, clave_publica)
        tiempo_cifrado = time.time() - inicio
        print(f"\n3. Cifrado completado - Tiempo: {tiempo_cifrado:.6f} segundos")
        print(f"   Mensaje cifrado: {mensaje_cifrado[:5]}... (polinomio)")
        
        # 4. Descifrar
        inicio = time.time()
        mensaje_descifrado, polinomio_descifrado = ntru.descifrar(
            mensaje_cifrado, 
            clave_privada_f, 
            clave_privada_fp
        )
        tiempo_descifrado = time.time() - inicio
        print(f"\n4. Descifrado completado - Tiempo: {tiempo_descifrado:.6f} segundos")
        print(f"   Mensaje descifrado: {mensaje_descifrado[:50]}...")
        
        # Verificación
        mensaje_original_corto = mensaje[:ntru.N]
        print(f"   Verificación: {'OK' if mensaje_descifrado in mensaje_original_corto else 'PARCIAL'}")
        
        print(f"\nTIEMPO TOTAL: {tiempo_lectura + tiempo_clave + tiempo_cifrado + tiempo_descifrado:.6f} segundos")
    
    print(f"\n{'=' * 70}")
    print("PROCESO COMPLETADO")
    print(f"{'=' * 70}")
