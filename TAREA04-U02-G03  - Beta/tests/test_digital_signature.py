"""
Tests Unitarios para el Sistema de Firma Digital
=================================================

Este módulo contiene tests para verificar el correcto funcionamiento
de los componentes del sistema de firma digital.

Ejecutar tests:
    python -m pytest test_digital_signature.py -v
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from key_manager import KeyManager
from digital_signature import DigitalSignature
from verification import SignatureVerifier


class TestKeyManager:
    """Tests para el módulo KeyManager."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.key_manager = KeyManager(keys_directory=self.temp_dir)
    
    def teardown_method(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_generate_key_pair(self):
        """Test: Generar par de claves RSA."""
        private_key, public_key = self.key_manager.generate_key_pair(key_size=2048)
        
        assert private_key is not None
        assert public_key is not None
        assert private_key.key_size == 2048
    
    def test_save_and_load_private_key(self):
        """Test: Guardar y cargar clave privada."""
        private_key, _ = self.key_manager.generate_key_pair()
        
        # Guardar
        filepath = self.key_manager.save_private_key(private_key, "test")
        assert os.path.exists(filepath)
        
        # Cargar
        loaded_key = self.key_manager.load_private_key(filepath)
        assert loaded_key is not None
        assert loaded_key.key_size == private_key.key_size
    
    def test_save_and_load_public_key(self):
        """Test: Guardar y cargar clave pública."""
        _, public_key = self.key_manager.generate_key_pair()
        
        # Guardar
        filepath = self.key_manager.save_public_key(public_key, "test")
        assert os.path.exists(filepath)
        
        # Cargar
        loaded_key = self.key_manager.load_public_key(filepath)
        assert loaded_key is not None
    
    def test_create_certificate(self):
        """Test: Crear certificado digital."""
        private_key, _ = self.key_manager.generate_key_pair()
        
        owner_info = {
            "name": "Test User",
            "organization": "Test Org",
            "city": "Test City",
            "state": "Test State",
            "country": "EC"
        }
        
        cert = self.key_manager.create_certificate(private_key, owner_info)
        assert cert is not None
        
        # Verificar información
        cert_info = self.key_manager.get_certificate_info(cert)
        assert cert_info["nombre"] == "Test User"
        assert cert_info["organizacion"] == "Test Org"


class TestDigitalSignature:
    """Tests para el módulo DigitalSignature."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.signature_manager = DigitalSignature(signatures_directory=self.temp_dir)
        self.key_manager = KeyManager(keys_directory=self.temp_dir)
        
        # Crear documento de prueba
        self.test_doc = os.path.join(self.temp_dir, "test.txt")
        with open(self.test_doc, 'w') as f:
            f.write("Este es un documento de prueba para firma digital.")
        
        # Generar claves
        self.private_key, self.public_key = self.key_manager.generate_key_pair()
    
    def teardown_method(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_calculate_hash(self):
        """Test: Calcular hash SHA-256 de archivo."""
        hash_value = self.signature_manager.calculate_hash(self.test_doc)
        
        assert hash_value is not None
        assert len(hash_value) == 64  # SHA-256 produce 64 caracteres hex
        assert isinstance(hash_value, str)
    
    def test_sign_document(self):
        """Test: Firmar un documento."""
        signature_data = self.signature_manager.sign_document(
            self.test_doc,
            self.private_key
        )
        
        assert signature_data is not None
        assert "document_hash" in signature_data
        assert "signature" in signature_data
        assert "timestamp" in signature_data
        assert signature_data["algorithm"] == "RSA-PSS with SHA-256"
    
    def test_save_and_load_signature(self):
        """Test: Guardar y cargar firma."""
        signature_data = self.signature_manager.sign_document(
            self.test_doc,
            self.private_key
        )
        
        # Guardar
        filepath = self.signature_manager.save_signature(signature_data, "test_sig")
        assert os.path.exists(filepath)
        
        # Cargar
        loaded_sig = self.signature_manager.load_signature(filepath)
        assert loaded_sig["document_hash"] == signature_data["document_hash"]


class TestSignatureVerifier:
    """Tests para el módulo SignatureVerifier."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.verifier = SignatureVerifier()
        self.signature_manager = DigitalSignature(signatures_directory=self.temp_dir)
        self.key_manager = KeyManager(keys_directory=self.temp_dir)
        
        # Crear documento de prueba
        self.test_doc = os.path.join(self.temp_dir, "test.txt")
        with open(self.test_doc, 'w') as f:
            f.write("Documento original para verificación.")
        
        # Generar claves y firmar
        self.private_key, self.public_key = self.key_manager.generate_key_pair()
        self.signature_data = self.signature_manager.sign_document(
            self.test_doc,
            self.private_key
        )
    
    def teardown_method(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_verify_valid_signature(self):
        """Test: Verificar firma válida."""
        is_valid, message = self.verifier.verify_signature(
            self.test_doc,
            self.signature_data,
            self.public_key
        )
        
        assert is_valid == True
        assert "ÉXITO" in message
    
    def test_verify_modified_document(self):
        """Test: Detectar documento modificado."""
        # Modificar el documento
        with open(self.test_doc, 'w') as f:
            f.write("Documento MODIFICADO maliciosamente.")
        
        is_valid, message = self.verifier.verify_signature(
            self.test_doc,
            self.signature_data,
            self.public_key
        )
        
        assert is_valid == False
        assert "modificado" in message.lower()
    
    def test_compare_identical_files(self):
        """Test: Comparar archivos idénticos."""
        # Crear copia idéntica
        test_doc2 = os.path.join(self.temp_dir, "test2.txt")
        shutil.copy(self.test_doc, test_doc2)
        
        are_equal = self.verifier.compare_hashes(self.test_doc, test_doc2)
        assert are_equal == True
    
    def test_compare_different_files(self):
        """Test: Comparar archivos diferentes."""
        # Crear archivo diferente
        test_doc2 = os.path.join(self.temp_dir, "test2.txt")
        with open(test_doc2, 'w') as f:
            f.write("Contenido completamente diferente.")
        
        are_equal = self.verifier.compare_hashes(self.test_doc, test_doc2)
        assert are_equal == False


class TestIntegration:
    """Tests de integración del sistema completo."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.key_manager = KeyManager(keys_directory=self.temp_dir)
        self.signature_manager = DigitalSignature(signatures_directory=self.temp_dir)
        self.verifier = SignatureVerifier()
    
    def teardown_method(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_complete_workflow(self):
        """Test: Flujo completo de firma y verificación."""
        # 1. Generar claves
        private_key, public_key = self.key_manager.generate_key_pair()
        
        # 2. Crear certificado
        owner_info = {
            "name": "Alice",
            "organization": "ESPOL",
            "city": "Guayaquil",
            "state": "Guayas",
            "country": "EC"
        }
        certificate = self.key_manager.create_certificate(private_key, owner_info)
        
        # 3. Crear documento
        doc_path = os.path.join(self.temp_dir, "contrato.txt")
        with open(doc_path, 'w') as f:
            f.write("Contrato importante entre partes.")
        
        # 4. Firmar documento
        signature_data = self.signature_manager.sign_document(
            doc_path,
            private_key,
            certificate
        )
        
        # 5. Verificar firma
        is_valid, message = self.verifier.verify_signature(
            doc_path,
            signature_data,
            public_key
        )
        
        assert is_valid == True
        
        # 6. Verificar certificado
        cert_valid, cert_msg = self.verifier.verify_certificate(certificate)
        assert cert_valid == True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
