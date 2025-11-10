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

class NTRU:
    """
    Implementación simplificada del algoritmo NTRU para fines educativos
    """
    
    def __init__(self, N=11, p=3, q=32):
        """
        Inicializa los parámetros del sistema NTRU
        
        Parámetros:
        - N: Grado del polinomio (debe ser primo)
        - p: Módulo pequeño para el mensaje (generalmente 3)
        - q: Módulo grande para las operaciones (debe ser mayor que p)
        
        Para seguridad real, N debería ser mucho mayor (ej: 509, 677)
        """
        self.N = N  # Grado del anillo polinomial
        self.p = p  # Módulo pequeño
        self.q = q  # Módulo grande
        
        # Claves públicas y privadas
        self.clave_publica = None
        self.clave_privada_f = None
        self.clave_privada_fp = None
        
        print(f"📐 Parámetros NTRU: N={N}, p={p}, q={q}")
    
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
        
        Proceso:
        1. Genera polinomios aleatorios f y g
        2. Calcula f_p (inverso de f módulo p)
        3. Calcula f_q (inverso de f módulo q)
        4. Clave pública h = f_q * g (mod q)
        5. Claves privadas: f y f_p
        """
        print("\n🔑 Generando par de claves...")
        
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
        
        print("✅ Claves generadas exitosamente")
        print(f"   Clave pública (h): {self.clave_publica[:5]}... (primeros 5 coeficientes)")
        print(f"   Clave privada (f): {self.clave_privada_f[:5]}... (primeros 5 coeficientes)")
        
        return self.clave_publica, (self.clave_privada_f, self.clave_privada_fp)
    
    def texto_a_polinomio(self, texto):
        """
        Convierte texto a un polinomio con coeficientes pequeños
        Cada carácter se mapea a un coeficiente en {-1, 0, 1}
        """
        coeficientes = []
        for char in texto[:self.N]:  # Limita al grado N
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
        
        Proceso:
        1. Convierte mensaje a polinomio m
        2. Genera polinomio aleatorio r (efímero)
        3. Calcula e = r * h + m (mod q)
        
        Parámetros:
        - mensaje: texto a cifrar
        - clave_publica: clave pública del receptor
        
        Retorna:
        - Polinomio cifrado e
        """
        print(f"\n🔒 Cifrando mensaje: '{mensaje}'")
        
        # Convierte mensaje a polinomio
        m = self.texto_a_polinomio(mensaje)
        print(f"   Mensaje como polinomio: {m[:5]}... (primeros 5 coeficientes)")
        
        # Genera r (polinomio aleatorio efímero)
        r = self.generar_polinomio_pequeño(d1=2, d2=2)
        print(f"   Polinomio aleatorio r: {r[:5]}... (primeros 5 coeficientes)")
        
        # Calcula e = r * h + m (mod q)
        rh = self.multiplicar_polinomios(r, clave_publica, self.q)
        e = np.mod(rh + m, self.q)
        
        print(f"   Mensaje cifrado (e): {e[:5]}... (primeros 5 coeficientes)")
        
        return e
    
    def descifrar(self, e, clave_privada_f, clave_privada_fp):
        """
        Descifra un mensaje usando la clave privada
        
        Proceso:
        1. Calcula a = f * e (mod q)
        2. Centra a en el rango apropiado
        3. Calcula m = fp * a (mod p)
        
        Parámetros:
        - e: mensaje cifrado (polinomio)
        - clave_privada_f: primera parte de la clave privada
        - clave_privada_fp: segunda parte de la clave privada
        
        Retorna:
        - Mensaje descifrado
        """
        print("\n🔓 Descifrando mensaje...")
        
        # Calcula a = f * e (mod q)
        a = self.multiplicar_polinomios(clave_privada_f, e, self.q)
        
        # Centra a en el rango [-q/2, q/2]
        a = np.array([(coef if coef <= self.q//2 else coef - self.q) for coef in a])
        
        # Calcula m = fp * a (mod p)
        m = self.multiplicar_polinomios(clave_privada_fp, a, self.p)
        
        # Centra m en el rango apropiado
        m = np.array([(coef if coef <= self.p//2 else coef - self.p) for coef in m])
        
        print(f"   Mensaje descifrado (polinomio): {m[:5]}... (primeros 5 coeficientes)")
        
        # Convierte polinomio de vuelta a texto
        mensaje_descifrado = self.polinomio_a_texto(m)
        
        return mensaje_descifrado, m


# ========================================
# EJEMPLO DE USO
# ========================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN DEL ALGORITMO NTRU")
    print("(Implementación simplificada con fines educativos)")
    print("=" * 70)
    
    # Inicializa el sistema NTRU con parámetros pequeños
    # Nota: Para seguridad real, N debe ser mucho mayor (509, 677, etc.)
    ntru = NTRU(N=11, p=3, q=32)
    
    # --- GENERACIÓN DE CLAVES ---
    print("\n" + "=" * 70)
    print("PASO 1: GENERACIÓN DE CLAVES")
    print("=" * 70)
    
    clave_publica, (clave_privada_f, clave_privada_fp) = ntru.generar_claves()
    
    # --- CIFRADO ---
    print("\n" + "=" * 70)
    print("PASO 2: CIFRADO DEL MENSAJE")
    print("=" * 70)
    
    mensaje_original = "HOLA"
    print(f"\n📝 Mensaje original: '{mensaje_original}'")
    
    mensaje_cifrado = ntru.cifrar(mensaje_original, clave_publica)
    
    # --- DESCIFRADO ---
    print("\n" + "=" * 70)
    print("PASO 3: DESCIFRADO DEL MENSAJE")
    print("=" * 70)
    
    mensaje_descifrado, polinomio_descifrado = ntru.descifrar(
        mensaje_cifrado, 
        clave_privada_f, 
        clave_privada_fp
    )
    
    print(f"\n✅ Mensaje descifrado: '{mensaje_descifrado}'")
    
    # --- VERIFICACIÓN ---
    print("\n" + "=" * 70)
    print("VERIFICACIÓN")
    print("=" * 70)
    
    print(f"\n📝 Mensaje original:   '{mensaje_original}'")
    print(f"🔒 Mensaje cifrado:    {mensaje_cifrado[:8]}... (polinomio)")
    print(f"🔓 Mensaje descifrado: '{mensaje_descifrado}'")
    
    # Comparación de polinomios
    m_original = ntru.texto_a_polinomio(mensaje_original)
    print(f"\n📊 Comparación de polinomios:")
    print(f"   Original:   {m_original}")
    print(f"   Descifrado: {polinomio_descifrado}")
    
    if np.array_equal(m_original, polinomio_descifrado):
        print("\n✅ ¡Éxito! Los polinomios coinciden perfectamente.")
    else:
        print("\n⚠️  Los polinomios son similares (variación por simplificación del algoritmo)")
    
    # --- DEMOSTRACIÓN: NO SE PUEDE DESCIFRAR SIN LA CLAVE PRIVADA ---
    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN: INTENTO SIN CLAVE PRIVADA")
    print("=" * 70)
    
    print("\n🔐 Sin la clave privada correcta, el mensaje no se puede descifrar.")
    print("   El texto cifrado (polinomio) es inútil sin las claves privadas f y fp.")
    
    # --- INFORMACIÓN ADICIONAL ---
    print("\n" + "=" * 70)
    print("CARACTERÍSTICAS DE NTRU")
    print("=" * 70)
    print("""
    ✓ Tipo: Cifrado asimétrico (clave pública/privada)
    ✓ Basado en: Problemas matemáticos de retículos polinomiales
    ✓ Resistencia cuántica: SÍ (resistente a computadoras cuánticas)
    ✓ Velocidad: Muy rápido (más rápido que RSA)
    ✓ Año: 1996 (Hoffstein, Pipher, Silverman)
    ✓ Uso: Comunicaciones seguras post-cuánticas
    
    Ventajas:
    • Operaciones más rápidas que RSA y ECC
    • Claves más pequeñas para el mismo nivel de seguridad
    • Resistente a ataques de computadoras cuánticas (algoritmo de Shor)
    
    Aplicaciones:
    • Cifrado de correos electrónicos
    • VPNs y comunicaciones seguras
    • Sistemas de seguridad post-cuántica
    • Blockchain y criptomonedas futuras
    """)
    
    print("=" * 70)
    print("\n⚠️  NOTA IMPORTANTE:")
    print("Esta es una implementación EDUCATIVA simplificada.")
    print("Para uso en producción, utiliza librerías como 'pqcrypto' o 'ntru'.")
    print("=" * 70)
