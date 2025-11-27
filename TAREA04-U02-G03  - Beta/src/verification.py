"""
Módulo de Verificación de Firmas Digitales
===========================================

Este módulo proporciona funcionalidades para:
- Verificar la autenticidad de firmas digitales
- Validar la integridad de documentos firmados
- Comprobar certificados digitales

Proceso de Verificación:
------------------------
1. Recalcular el hash del documento original
2. "Descifrar" la firma con la clave pública
3. Comparar ambos valores: si coinciden, la firma es válida
"""

import os
import hashlib
from typing import Dict, Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography import x509
from datetime import datetime


class SignatureVerifier:
    """
    Gestiona la verificación de firmas digitales.
    
    La verificación confirma:
    - El documento NO ha sido modificado (integridad)
    - La firma fue creada por el propietario de la clave privada (autenticidad)
    - El certificado es válido (si aplica)
    """
    
    def __init__(self):
        """Inicializa el verificador de firmas."""
        pass
    
    def calculate_hash(self, file_path: str) -> str:
        """
        Calcula el hash SHA-256 de un archivo.
        
        Este método debe producir el MISMO hash que se usó al firmar
        si el archivo no ha sido modificado.
        
        Args:
            file_path: Ruta del archivo
        
        Returns:
            Hash hexadecimal del archivo
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def verify_signature(self, document_path: str, signature_data: Dict,
                        public_key: rsa.RSAPublicKey) -> Tuple[bool, str]:
        """
        Verifica si una firma digital es válida para un documento.
        
        Proceso:
        1. Recalcula el hash del documento actual
        2. Compara con el hash almacenado en la firma
        3. Verifica criptográficamente la firma con la clave pública
        
        Args:
            document_path: Ruta del documento a verificar
            signature_data: Datos de la firma (diccionario)
            public_key: Clave pública del firmante
        
        Returns:
            Tupla (es_válida: bool, mensaje: str)
        
        Security:
            - Si el documento fue modificado, los hashes NO coincidirán
            - Si la firma fue alterada o es falsa, la verificación criptográfica fallará
            - Solo la clave pública correspondiente a la privada que firmó puede verificar
        """
        print(f"\n🔍 Verificando firma del documento: {os.path.basename(document_path)}")
        
        # 1. Verificar que el archivo existe
        if not os.path.exists(document_path):
            return False, "ERROR: El archivo no existe"
        
        # 2. Calcular el hash actual del documento
        current_hash = self.calculate_hash(document_path)
        original_hash = signature_data.get('document_hash', '')
        
        print(f"Hash original: {original_hash[:32]}...")
        print(f"Hash actual:   {current_hash[:32]}...")
        
        # 3. Comparar hashes (verificación de integridad)
        if current_hash != original_hash:
            return False, "FALLO: El documento ha sido modificado. Los hashes no coinciden."
        
        print("✓ Integridad verificada: los hashes coinciden")
        
        # 4. Verificar la firma criptográficamente
        try:
            signature_bytes = bytes.fromhex(signature_data['signature'])
            
            # Intentar verificar la firma con la clave pública
            # Si falla, lanzará una excepción InvalidSignature
            public_key.verify(
                signature_bytes,
                current_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            print("✓ Firma criptográfica verificada")
            return True, "ÉXITO: La firma es válida y el documento es auténtico"
            
        except Exception as e:
            return False, f"FALLO: Firma inválida. Error: {str(e)}"
    
    def verify_certificate(self, certificate: x509.Certificate) -> Tuple[bool, str]:
        """
        Verifica la validez temporal de un certificado.
        
        Args:
            certificate: Certificado X.509 a verificar
        
        Returns:
            Tupla (es_válido: bool, mensaje: str)
        
        Note:
            En un sistema real, también se verificaría:
            - La cadena de confianza (CA)
            - El estado de revocación (CRL/OCSP)
            - Las extensiones del certificado
        """
        print("\n🔐 Verificando certificado digital...")
        
        now = datetime.utcnow()
        not_before = certificate.not_valid_before
        not_after = certificate.not_valid_after
        
        print(f"Válido desde: {not_before}")
        print(f"Válido hasta: {not_after}")
        print(f"Fecha actual: {now}")
        
        if now < not_before:
            return False, "FALLO: El certificado aún no es válido"
        
        if now > not_after:
            return False, "FALLO: El certificado ha expirado"
        
        print("✓ Certificado válido temporalmente")
        return True, "ÉXITO: El certificado es válido"
    
    def full_verification(self, document_path: str, signature_data: Dict,
                         public_key: rsa.RSAPublicKey,
                         certificate: x509.Certificate = None) -> Dict[str, any]:
        """
        Realiza una verificación completa de firma y certificado.
        
        Args:
            document_path: Ruta del documento
            signature_data: Datos de la firma
            public_key: Clave pública
            certificate: Certificado opcional
        
        Returns:
            Diccionario con resultados detallados de la verificación
        """
        results = {
            "documento": os.path.basename(document_path),
            "verificaciones": {},
            "valida": False
        }
        
        # Verificar la firma
        sig_valid, sig_msg = self.verify_signature(document_path, signature_data, public_key)
        results["verificaciones"]["firma"] = {
            "valida": sig_valid,
            "mensaje": sig_msg
        }
        
        # Verificar el certificado si está disponible
        if certificate:
            cert_valid, cert_msg = self.verify_certificate(certificate)
            results["verificaciones"]["certificado"] = {
                "valido": cert_valid,
                "mensaje": cert_msg
            }
            # Solo es válido si AMBOS son válidos
            results["valida"] = sig_valid and cert_valid
        else:
            results["valida"] = sig_valid
        
        return results
    
    def display_verification_results(self, results: Dict) -> None:
        """
        Muestra los resultados de la verificación de forma legible.
        
        Args:
            results: Diccionario con resultados de verificación
        """
        print("\n" + "="*60)
        print("RESULTADOS DE LA VERIFICACIÓN")
        print("="*60)
        print(f"Documento: {results['documento']}")
        print()
        
        for verificacion, datos in results['verificaciones'].items():
            print(f"{verificacion.upper()}:")
            
            # Mostrar símbolo de estado
            if datos.get('valida') or datos.get('valido'):
                print("  Estado: ✓ VÁLIDA")
            else:
                print("  Estado: ✗ INVÁLIDA")
            
            print(f"  Mensaje: {datos['mensaje']}")
            print()
        
        print("-" * 60)
        if results['valida']:
            print("🎉 RESULTADO FINAL: FIRMA VÁLIDA Y AUTÉNTICA")
            print("\nEsto significa que:")
            print("  ✓ El documento NO ha sido modificado")
            print("  ✓ La firma fue creada por el propietario de la clave")
            print("  ✓ Puedes confiar en la autenticidad del documento")
        else:
            print("⚠️  RESULTADO FINAL: FIRMA NO VÁLIDA")
            print("\nAdvertencia:")
            print("  ✗ El documento puede haber sido alterado")
            print("  ✗ La firma puede ser fraudulenta")
            print("  ✗ NO se puede confiar en este documento")
        
        print("="*60 + "\n")
    
    def compare_hashes(self, file1_path: str, file2_path: str) -> bool:
        """
        Compara los hashes de dos archivos.
        
        Útil para verificar si dos archivos son idénticos.
        
        Args:
            file1_path: Ruta del primer archivo
            file2_path: Ruta del segundo archivo
        
        Returns:
            True si los hashes son iguales (archivos idénticos)
        """
        hash1 = self.calculate_hash(file1_path)
        hash2 = self.calculate_hash(file2_path)
        
        print(f"\nArchivo 1: {hash1}")
        print(f"Archivo 2: {hash2}")
        
        if hash1 == hash2:
            print("✓ Los archivos son idénticos")
            return True
        else:
            print("✗ Los archivos son diferentes")
            return False
