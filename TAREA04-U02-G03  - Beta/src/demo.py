"""
Script de demostración del Sistema de Firma Digital
====================================================

Este script demuestra automáticamente las capacidades del sistema
sin necesidad de interacción manual.

Ejecutar:
    python demo.py
"""

import os
import sys

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from key_manager import KeyManager
from digital_signature import DigitalSignature
from verification import SignatureVerifier


def print_section(title):
    """Imprime un separador de sección."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def demo():
    """Ejecuta la demostración completa."""
    
    print_section("🔐 DEMOSTRACIÓN DEL SISTEMA DE FIRMA DIGITAL")
    
    # Configuración
    keys_dir = "../keys/demo"
    docs_dir = "../documents"
    sigs_dir = "../signatures/demo"
    
    # Crear directorios si no existen
    os.makedirs(keys_dir, exist_ok=True)
    os.makedirs(sigs_dir, exist_ok=True)
    
    # Inicializar componentes
    key_manager = KeyManager(keys_directory=keys_dir)
    signature_manager = DigitalSignature(signatures_directory=sigs_dir)
    verifier = SignatureVerifier()
    
    # =========================================================================
    # PARTE 1: Generar Claves y Certificado
    # =========================================================================
    print_section("PARTE 1: Generación de Claves y Certificado")
    
    print("Generando par de claves RSA de 2048 bits para Alice...")
    alice_private, alice_public = key_manager.generate_key_pair(key_size=2048)
    
    print("\nInformación del propietario:")
    alice_info = {
        "name": "Alice Rodríguez",
        "organization": "ESPOL - Grupo 3",
        "city": "Guayaquil",
        "state": "Guayas",
        "country": "EC"
    }
    for key, value in alice_info.items():
        print(f"  {key}: {value}")
    
    print("\nCreando certificado digital para Alice...")
    alice_cert = key_manager.create_certificate(alice_private, alice_info, days_valid=365)
    
    print("\nGuardando claves y certificado...")
    key_manager.save_private_key(alice_private, "alice", password="demo123")
    key_manager.save_public_key(alice_public, "alice")
    key_manager.save_certificate(alice_cert, "alice")
    
    print("\n✅ Claves y certificado de Alice generados exitosamente")
    
    # Mostrar información del certificado
    cert_info = key_manager.get_certificate_info(alice_cert)
    print("\n📜 Información del Certificado:")
    for key, value in cert_info.items():
        print(f"  {key}: {value}")
    
    # =========================================================================
    # PARTE 2: Crear y Firmar Documento
    # =========================================================================
    print_section("PARTE 2: Creación y Firma de Documento")
    
    # Crear un documento de prueba
    doc_path = os.path.join(docs_dir, "demo_documento.txt")
    print(f"Creando documento de prueba: {doc_path}")
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("""
ACUERDO DE CONFIDENCIALIDAD

Entre las partes:

EMPRESA ABC S.A. (en adelante "La Empresa")
y
Alice Rodríguez (en adelante "El Colaborador")

Acuerdan mantener la confidencialidad de toda información
compartida durante la duración del proyecto.

Fecha: 26 de Noviembre de 2025
Lugar: Guayaquil, Ecuador
        """)
    
    print("✓ Documento creado")
    
    print("\nFirmando el documento con la clave privada de Alice...")
    signature_data = signature_manager.sign_document(
        doc_path,
        alice_private,
        alice_cert
    )
    
    # Guardar la firma
    sig_path = signature_manager.save_signature(signature_data, "demo_acuerdo")
    
    # Mostrar información de la firma
    signature_manager.display_signature_info(signature_data)
    
    # =========================================================================
    # PARTE 3: Verificar Firma (Documento Original)
    # =========================================================================
    print_section("PARTE 3: Verificación de Firma - Documento Original")
    
    print("Verificando la firma del documento original...")
    
    is_valid, message = verifier.verify_signature(
        doc_path,
        signature_data,
        alice_public
    )
    
    if is_valid:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")
    
    # Verificación completa incluyendo certificado
    print("\nRealizando verificación completa (con certificado)...")
    results = verifier.full_verification(
        doc_path,
        signature_data,
        alice_public,
        alice_cert
    )
    
    verifier.display_verification_results(results)
    
    # =========================================================================
    # PARTE 4: Detectar Modificación (Demostración de Seguridad)
    # =========================================================================
    print_section("PARTE 4: Detección de Modificaciones")
    
    # Crear una versión modificada del documento
    modified_doc_path = os.path.join(docs_dir, "demo_documento_modificado.txt")
    print(f"Creando versión modificada del documento...")
    
    with open(modified_doc_path, 'w', encoding='utf-8') as f:
        f.write("""
ACUERDO DE CONFIDENCIALIDAD

Entre las partes:

EMPRESA ABC S.A. (en adelante "La Empresa")
y
Alice Rodríguez (en adelante "El Colaborador")

Acuerdan mantener la confidencialidad de toda información
compartida durante la duración del proyecto.

*** TEXTO ADICIONAL MALICIOSO AÑADIDO ***

Fecha: 26 de Noviembre de 2025
Lugar: Guayaquil, Ecuador
        """)
    
    print("✓ Documento modificado creado")
    
    print("\nIntentando verificar la firma con el documento modificado...")
    
    is_valid_modified, message_modified = verifier.verify_signature(
        modified_doc_path,
        signature_data,
        alice_public
    )
    
    if not is_valid_modified:
        print(f"\n✅ ¡Modificación detectada correctamente!")
        print(f"   {message_modified}")
    else:
        print(f"\n❌ ERROR: La modificación NO fue detectada (esto no debería pasar)")
    
    # =========================================================================
    # PARTE 5: Generar Segundo Firmante (Bob)
    # =========================================================================
    print_section("PARTE 5: Segundo Firmante - Demostración de Identidades Múltiples")
    
    print("Generando claves para Bob...")
    bob_private, bob_public = key_manager.generate_key_pair(key_size=2048)
    
    bob_info = {
        "name": "Bob Martínez",
        "organization": "ESPOL - Grupo 3",
        "city": "Guayaquil",
        "state": "Guayas",
        "country": "EC"
    }
    
    bob_cert = key_manager.create_certificate(bob_private, bob_info)
    
    key_manager.save_private_key(bob_private, "bob", password="bob456")
    key_manager.save_public_key(bob_public, "bob")
    key_manager.save_certificate(bob_cert, "bob")
    
    print("✅ Claves de Bob generadas")
    
    # Bob firma el mismo documento
    print("\nBob firma el mismo documento...")
    bob_signature = signature_manager.sign_document(
        doc_path,
        bob_private,
        bob_cert
    )
    
    signature_manager.save_signature(bob_signature, "demo_acuerdo_bob")
    
    print("\n✓ Ahora tenemos DOS firmas del mismo documento:")
    print(f"  - Firma de Alice: {signature_data['signature'][:32]}...")
    print(f"  - Firma de Bob:   {bob_signature['signature'][:32]}...")
    print("\nObserva que son DIFERENTES aunque firmaron el mismo documento.")
    print("Esto se debe a que cada uno usó su clave privada única.")
    
    # =========================================================================
    # PARTE 6: Comparar Hashes
    # =========================================================================
    print_section("PARTE 6: Comparación de Hashes")
    
    print("Comparando hashes entre documentos...")
    print("\nDocumento original vs documento original:")
    verifier.compare_hashes(doc_path, doc_path)
    
    print("\nDocumento original vs documento modificado:")
    verifier.compare_hashes(doc_path, modified_doc_path)
    
    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    print_section("✅ DEMOSTRACIÓN COMPLETADA")
    
    print("Se han demostrado los siguientes conceptos:")
    print("  ✓ Generación de pares de claves RSA")
    print("  ✓ Creación de certificados digitales X.509")
    print("  ✓ Firma digital de documentos con RSA-PSS y SHA-256")
    print("  ✓ Verificación de firmas válidas")
    print("  ✓ Detección de modificaciones en documentos")
    print("  ✓ Identidades múltiples (Alice y Bob)")
    print("  ✓ Comparación de hashes criptográficos")
    
    print("\n📁 Archivos generados:")
    print(f"  Claves: {keys_dir}/")
    print(f"  Firmas: {sigs_dir}/")
    print(f"  Documentos: {docs_dir}/")
    
    print("\n🎓 Conceptos criptográficos demostrados:")
    print("  • Criptografía asimétrica (RSA)")
    print("  • Funciones hash (SHA-256)")
    print("  • Firmas digitales (RSA-PSS)")
    print("  • Certificados digitales (X.509)")
    print("  • Integridad de datos")
    print("  • Autenticación")
    print("  • No repudio")
    
    print("\n" + "="*70)
    print("  Gracias por usar el Sistema de Firma Digital - Grupo 3")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {str(e)}")
        import traceback
        traceback.print_exc()
