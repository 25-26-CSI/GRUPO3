"""
Módulo de Gestión de Claves Criptográficas
===========================================

Este módulo proporciona funcionalidades para:
- Generar pares de claves RSA (pública y privada)
- Guardar y cargar claves en formato PEM
- Crear certificados digitales con información del propietario
- Gestionar la infraestructura de claves

Conceptos Criptográficos:
------------------------
- RSA: Algoritmo de criptografía asimétrica (clave pública/privada)
- PEM: Formato de codificación para claves y certificados
- Key Size: 2048 bits para balance seguridad/rendimiento
"""

import os
import json
from datetime import datetime, timedelta
from typing import Tuple, Dict, Optional
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID


class KeyManager:
    """
    Gestiona la generación, almacenamiento y recuperación de claves criptográficas.
    
    Esta clase implementa las operaciones necesarias para trabajar con
    criptografía de clave pública (RSA) en el contexto de firmas digitales.
    """
    
    def __init__(self, keys_directory: str = "keys"):
        """
        Inicializa el gestor de claves.
        
        Args:
            keys_directory: Directorio donde se almacenarán las claves
        """
        self.keys_directory = keys_directory
        # Crear el directorio si no existe
        os.makedirs(keys_directory, exist_ok=True)
    
    def generate_key_pair(self, key_size: int = 2048) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """
        Genera un par de claves RSA (privada y pública).
        
        Proceso:
        1. Genera una clave privada RSA de tamaño especificado
        2. Deriva la clave pública correspondiente
        
        Args:
            key_size: Tamaño de la clave en bits (2048 recomendado, 4096 para más seguridad)
        
        Returns:
            Tupla (clave_privada, clave_pública)
        
        Note:
            - 2048 bits: Seguridad estándar, buen rendimiento
            - 4096 bits: Mayor seguridad, menor rendimiento
        """
        print(f"Generando par de claves RSA de {key_size} bits...")
        
        # Generar clave privada RSA
        # La clave privada contiene tanto la información privada como pública
        private_key = rsa.generate_private_key(
            public_exponent=65537,  # Exponente público estándar (2^16 + 1)
            key_size=key_size,
            backend=default_backend()
        )
        
        # Extraer la clave pública de la privada
        public_key = private_key.public_key()
        
        print("✓ Par de claves generado exitosamente")
        return private_key, public_key
    
    def save_private_key(self, private_key: rsa.RSAPrivateKey, filename: str, 
                        password: Optional[str] = None) -> str:
        """
        Guarda la clave privada en un archivo PEM.
        
        Args:
            private_key: Clave privada RSA a guardar
            filename: Nombre del archivo (sin extensión)
            password: Contraseña opcional para cifrar la clave privada
        
        Returns:
            Ruta completa del archivo guardado
        
        Security:
            - Si se proporciona contraseña, la clave se cifra con AES-256
            - El archivo debe mantenerse SEGURO y PRIVADO
        """
        filepath = os.path.join(self.keys_directory, f"{filename}_private.pem")
        
        # Configurar el cifrado si hay contraseña
        encryption_algorithm = (
            serialization.BestAvailableEncryption(password.encode()) 
            if password else serialization.NoEncryption()
        )
        
        # Serializar la clave privada a formato PEM
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )
        
        # Guardar en archivo
        with open(filepath, 'wb') as f:
            f.write(pem)
        
        print(f"✓ Clave privada guardada en: {filepath}")
        return filepath
    
    def save_public_key(self, public_key: rsa.RSAPublicKey, filename: str) -> str:
        """
        Guarda la clave pública en un archivo PEM.
        
        Args:
            public_key: Clave pública RSA a guardar
            filename: Nombre del archivo (sin extensión)
        
        Returns:
            Ruta completa del archivo guardado
        
        Note:
            La clave pública puede compartirse libremente
        """
        filepath = os.path.join(self.keys_directory, f"{filename}_public.pem")
        
        # Serializar la clave pública a formato PEM
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Guardar en archivo
        with open(filepath, 'wb') as f:
            f.write(pem)
        
        print(f"✓ Clave pública guardada en: {filepath}")
        return filepath
    
    def load_private_key(self, filepath: str, password: Optional[str] = None) -> rsa.RSAPrivateKey:
        """
        Carga una clave privada desde un archivo PEM.
        
        Args:
            filepath: Ruta del archivo PEM
            password: Contraseña si la clave está cifrada
        
        Returns:
            Objeto de clave privada RSA
        """
        with open(filepath, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=password.encode() if password else None,
                backend=default_backend()
            )
        
        print(f"✓ Clave privada cargada desde: {filepath}")
        return private_key
    
    def load_public_key(self, filepath: str) -> rsa.RSAPublicKey:
        """
        Carga una clave pública desde un archivo PEM.
        
        Args:
            filepath: Ruta del archivo PEM
        
        Returns:
            Objeto de clave pública RSA
        """
        with open(filepath, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        
        print(f"✓ Clave pública cargada desde: {filepath}")
        return public_key
    
    def create_certificate(self, private_key: rsa.RSAPrivateKey, 
                          owner_info: Dict[str, str], 
                          days_valid: int = 365) -> x509.Certificate:
        """
        Crea un certificado digital autofirmado.
        
        Un certificado digital vincula una clave pública con la identidad
        del propietario, proporcionando autenticación.
        
        Args:
            private_key: Clave privada para firmar el certificado
            owner_info: Información del propietario (nombre, organización, etc.)
            days_valid: Días de validez del certificado
        
        Returns:
            Certificado X.509 autofirmado
        
        Note:
            Este es un certificado autofirmado (self-signed).
            En producción, se usaría una Autoridad Certificadora (CA).
        """
        public_key = private_key.public_key()
        
        # Construir el "subject" (información del propietario)
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, owner_info.get("country", "EC")),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, owner_info.get("state", "Guayas")),
            x509.NameAttribute(NameOID.LOCALITY_NAME, owner_info.get("city", "Guayaquil")),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, owner_info.get("organization", "ESPOL")),
            x509.NameAttribute(NameOID.COMMON_NAME, owner_info.get("name", "Usuario")),
        ])
        
        # El "issuer" es igual al "subject" porque es autofirmado
        issuer = subject
        
        # Crear el certificado
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.utcnow())
            .not_valid_after(datetime.utcnow() + timedelta(days=days_valid))
            .sign(private_key, hashes.SHA256(), default_backend())
        )
        
        print("✓ Certificado digital creado")
        return cert
    
    def save_certificate(self, certificate: x509.Certificate, filename: str) -> str:
        """
        Guarda un certificado en formato PEM.
        
        Args:
            certificate: Certificado X.509 a guardar
            filename: Nombre del archivo (sin extensión)
        
        Returns:
            Ruta completa del archivo guardado
        """
        filepath = os.path.join(self.keys_directory, f"{filename}_cert.pem")
        
        # Serializar el certificado a formato PEM
        pem = certificate.public_bytes(serialization.Encoding.PEM)
        
        with open(filepath, 'wb') as f:
            f.write(pem)
        
        print(f"✓ Certificado guardado en: {filepath}")
        return filepath
    
    def load_certificate(self, filepath: str) -> x509.Certificate:
        """
        Carga un certificado desde un archivo PEM.
        
        Args:
            filepath: Ruta del archivo PEM
        
        Returns:
            Certificado X.509
        """
        with open(filepath, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
        
        print(f"✓ Certificado cargado desde: {filepath}")
        return cert
    
    def get_certificate_info(self, certificate: x509.Certificate) -> Dict[str, str]:
        """
        Extrae información legible de un certificado.
        
        Args:
            certificate: Certificado X.509
        
        Returns:
            Diccionario con información del certificado
        """
        subject = certificate.subject
        
        info = {
            "nombre": subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,
            "organizacion": subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value,
            "ciudad": subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value,
            "estado": subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value,
            "pais": subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value,
            "valido_desde": certificate.not_valid_before.strftime("%Y-%m-%d %H:%M:%S"),
            "valido_hasta": certificate.not_valid_after.strftime("%Y-%m-%d %H:%M:%S"),
            "numero_serie": str(certificate.serial_number)
        }
        
        return info
