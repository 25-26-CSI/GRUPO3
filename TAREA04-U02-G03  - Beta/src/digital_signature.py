"""
Módulo de Firma Digital de Documentos
======================================

Este módulo implementa las funcionalidades principales de firma digital:
- Firma de documentos usando RSA y hashing SHA-256
- Generación de metadatos de firma
- Serialización de firmas en formato JSON

Conceptos Criptográficos:
------------------------
- Hash SHA-256: Genera un resumen único del documento (256 bits)
- Firma RSA: Cifra el hash con la clave privada del firmante
- Padding PSS: Esquema de relleno probabilístico para mayor seguridad
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography import x509


class DigitalSignature:
    """
    Gestiona la creación y manipulación de firmas digitales.
    
    Una firma digital proporciona:
    - Autenticidad: Verifica quién firmó el documento
    - Integridad: Detecta cualquier modificación del documento
    - No repudio: El firmante no puede negar haber firmado
    """
    
    def __init__(self, signatures_directory: str = "signatures"):
        """
        Inicializa el gestor de firmas digitales.
        
        Args:
            signatures_directory: Directorio donde se guardarán las firmas
        """
        self.signatures_directory = signatures_directory
        os.makedirs(signatures_directory, exist_ok=True)
    
    def calculate_hash(self, file_path: str) -> str:
        """
        Calcula el hash SHA-256 de un archivo.
        
        El hash es una "huella digital" única del archivo:
        - Cualquier cambio en el archivo produce un hash completamente diferente
        - Es prácticamente imposible encontrar dos archivos con el mismo hash
        - Tiene longitud fija (256 bits) independiente del tamaño del archivo
        
        Args:
            file_path: Ruta del archivo a hashear
        
        Returns:
            Hash hexadecimal del archivo
        
        Note:
            SHA-256 es el estándar de la industria para firmas digitales
        """
        sha256_hash = hashlib.sha256()
        
        # Leer el archivo en bloques para manejar archivos grandes
        with open(file_path, "rb") as f:
            # Leer en bloques de 64KB
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        
        hash_hex = sha256_hash.hexdigest()
        print(f"✓ Hash calculado: {hash_hex[:16]}...")
        return hash_hex
    
    def sign_document(self, document_path: str, private_key: rsa.RSAPrivateKey,
                     certificate: Optional[x509.Certificate] = None,
                     signer_info: Optional[Dict[str, str]] = None) -> Dict:
        """
        Firma un documento digitalmente.
        
        Proceso de firma digital:
        1. Calcular el hash SHA-256 del documento
        2. "Cifrar" el hash con la clave privada (esto es la firma)
        3. Guardar la firma junto con metadatos
        
        Args:
            document_path: Ruta del documento a firmar
            private_key: Clave privada del firmante
            certificate: Certificado opcional del firmante
            signer_info: Información adicional del firmante
        
        Returns:
            Diccionario con los datos de la firma
        
        Security:
            - Solo el propietario de la clave privada puede crear esta firma
            - La firma es única para este documento específico
        """
        print(f"\n📝 Firmando documento: {os.path.basename(document_path)}")
        
        # 1. Calcular el hash del documento
        document_hash = self.calculate_hash(document_path)
        
        # 2. Firmar el hash con la clave privada
        # PSS (Probabilistic Signature Scheme) es más seguro que PKCS1v15
        signature_bytes = private_key.sign(
            document_hash.encode(),  # Convertir hash a bytes
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),  # Función de generación de máscara
                salt_length=padding.PSS.MAX_LENGTH  # Longitud máxima de sal
            ),
            hashes.SHA256()
        )
        
        # 3. Preparar metadatos de la firma
        signature_data = {
            "document_name": os.path.basename(document_path),
            "document_hash": document_hash,
            "signature": signature_bytes.hex(),  # Convertir bytes a hexadecimal
            "timestamp": datetime.now().isoformat(),
            "algorithm": "RSA-PSS with SHA-256",
            "key_size": private_key.key_size
        }
        
        # Añadir información del certificado si está disponible
        if certificate:
            subject = certificate.subject
            signature_data["signer"] = {
                "nombre": subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value,
                "organizacion": subject.get_attributes_for_oid(x509.oid.NameOID.ORGANIZATION_NAME)[0].value,
                "certificado_serie": str(certificate.serial_number)
            }
        elif signer_info:
            signature_data["signer"] = signer_info
        
        print(f"✓ Documento firmado exitosamente")
        print(f"  Algoritmo: {signature_data['algorithm']}")
        print(f"  Tamaño de clave: {signature_data['key_size']} bits")
        
        return signature_data
    
    def save_signature(self, signature_data: Dict, output_filename: str) -> str:
        """
        Guarda la firma digital en un archivo JSON.
        
        Args:
            signature_data: Datos de la firma
            output_filename: Nombre del archivo de firma (sin extensión)
        
        Returns:
            Ruta del archivo de firma guardado
        """
        filepath = os.path.join(self.signatures_directory, f"{output_filename}.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(signature_data, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Firma guardada en: {filepath}")
        return filepath
    
    def load_signature(self, signature_path: str) -> Dict:
        """
        Carga una firma digital desde un archivo JSON.
        
        Args:
            signature_path: Ruta del archivo de firma
        
        Returns:
            Diccionario con los datos de la firma
        """
        with open(signature_path, 'r', encoding='utf-8') as f:
            signature_data = json.load(f)
        
        print(f"✓ Firma cargada desde: {signature_path}")
        return signature_data
    
    def display_signature_info(self, signature_data: Dict) -> None:
        """
        Muestra información detallada de una firma digital.
        
        Args:
            signature_data: Datos de la firma
        """
        print("\n" + "="*60)
        print("INFORMACIÓN DE LA FIRMA DIGITAL")
        print("="*60)
        print(f"Documento: {signature_data['document_name']}")
        print(f"Hash del documento: {signature_data['document_hash']}")
        print(f"Fecha y hora: {signature_data['timestamp']}")
        print(f"Algoritmo: {signature_data['algorithm']}")
        print(f"Tamaño de clave: {signature_data['key_size']} bits")
        
        if 'signer' in signature_data:
            print("\nInformación del Firmante:")
            for key, value in signature_data['signer'].items():
                print(f"  {key.capitalize()}: {value}")
        
        print(f"\nFirma (primeros 64 caracteres): {signature_data['signature'][:64]}...")
        print("="*60 + "\n")
    
    def sign_and_save(self, document_path: str, private_key: rsa.RSAPrivateKey,
                     certificate: Optional[x509.Certificate] = None,
                     output_name: Optional[str] = None) -> str:
        """
        Método de conveniencia que firma y guarda en un solo paso.
        
        Args:
            document_path: Ruta del documento a firmar
            private_key: Clave privada del firmante
            certificate: Certificado opcional
            output_name: Nombre personalizado para el archivo de firma
        
        Returns:
            Ruta del archivo de firma guardado
        """
        # Generar nombre de salida si no se proporciona
        if not output_name:
            doc_name = os.path.splitext(os.path.basename(document_path))[0]
            output_name = f"{doc_name}_signature"
        
        # Firmar el documento
        signature_data = self.sign_document(document_path, private_key, certificate)
        
        # Guardar la firma
        signature_path = self.save_signature(signature_data, output_name)
        
        return signature_path
