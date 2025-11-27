"""
Aplicación Principal de Firma Digital
======================================

Interfaz de línea de comandos (CLI) para interactuar con el sistema
de firma digital de documentos.

Este programa permite:
1. Generar pares de claves y certificados
2. Firmar documentos
3. Verificar firmas existentes
4. Visualizar información de certificados

Autor: Grupo 3
Fecha: Noviembre 2025
"""

import os
import sys
from pathlib import Path

# Añadir el directorio src al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from key_manager import KeyManager
from digital_signature import DigitalSignature
from verification import SignatureVerifier

# Importar colorama para colores en la terminal (opcional)
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


class DigitalSignatureApp:
    """
    Aplicación principal que orquesta todas las funcionalidades
    del sistema de firma digital.
    """
    
    def __init__(self):
        """Inicializa los componentes de la aplicación."""
        self.key_manager = KeyManager()
        self.signature_manager = DigitalSignature()
        self.verifier = SignatureVerifier()
        
        # Estado de la aplicación
        self.current_private_key = None
        self.current_public_key = None
        self.current_certificate = None
        self.current_key_name = None
    
    def print_header(self):
        """Muestra el encabezado de la aplicación."""
        header = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🔐 SISTEMA DE FIRMA DIGITAL DE DOCUMENTOS 🔐         ║
║                                                              ║
║              Proyecto de Criptografía - Grupo 3              ║
║              Tema: Firma Digital y Electrónica              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(header)
    
    def print_menu(self):
        """Muestra el menú principal."""
        print("\n" + "="*60)
        print("MENÚ PRINCIPAL")
        print("="*60)
        print("1. 🔑 Generar nuevo par de claves y certificado")
        print("2. 📂 Cargar claves existentes")
        print("3. ✍️  Firmar un documento")
        print("4. ✅ Verificar una firma")
        print("5. 📋 Ver información del certificado actual")
        print("6. ℹ️  Ayuda - ¿Cómo funciona la firma digital?")
        print("0. 🚪 Salir")
        print("="*60)
        
        # Mostrar estado actual
        if self.current_key_name:
            print(f"\n[Estado] Claves cargadas: {self.current_key_name}")
        else:
            print("\n[Estado] No hay claves cargadas")
    
    def generate_keys(self):
        """Opción 1: Generar nuevo par de claves y certificado."""
        print("\n" + "="*60)
        print("GENERAR NUEVO PAR DE CLAVES")
        print("="*60)
        
        # Solicitar información del propietario
        print("\nIngrese la información del propietario del certificado:")
        owner_info = {
            "name": input("Nombre completo: ").strip() or "Usuario",
            "organization": input("Organización: ").strip() or "ESPOL",
            "city": input("Ciudad: ").strip() or "Guayaquil",
            "state": input("Estado/Provincia: ").strip() or "Guayas",
            "country": input("País (código de 2 letras): ").strip().upper() or "EC"
        }
        
        # Solicitar nombre para guardar las claves
        key_name = input("\nNombre para identificar estas claves: ").strip() or "mi_clave"
        
        # Preguntar si quiere proteger con contraseña
        protect = input("\n¿Proteger la clave privada con contraseña? (s/n): ").lower()
        password = None
        if protect == 's':
            password = input("Ingrese la contraseña: ")
        
        print("\n" + "-"*60)
        
        # Generar el par de claves
        private_key, public_key = self.key_manager.generate_key_pair(key_size=2048)
        
        # Crear el certificado
        certificate = self.key_manager.create_certificate(
            private_key, 
            owner_info, 
            days_valid=365
        )
        
        # Guardar las claves y certificado
        self.key_manager.save_private_key(private_key, key_name, password)
        self.key_manager.save_public_key(public_key, key_name)
        self.key_manager.save_certificate(certificate, key_name)
        
        # Cargar en memoria
        self.current_private_key = private_key
        self.current_public_key = public_key
        self.current_certificate = certificate
        self.current_key_name = key_name
        
        print("\n✅ ¡Claves y certificado generados exitosamente!")
        print(f"   Archivos guardados con el nombre: {key_name}")
        print("\n" + "="*60)
        
        input("\nPresione Enter para continuar...")
    
    def load_keys(self):
        """Opción 2: Cargar claves existentes."""
        print("\n" + "="*60)
        print("CARGAR CLAVES EXISTENTES")
        print("="*60)
        
        # Listar archivos disponibles en el directorio de claves
        keys_dir = Path("keys")
        if keys_dir.exists():
            pem_files = list(keys_dir.glob("*_private.pem"))
            if pem_files:
                print("\nClaves disponibles:")
                for i, file in enumerate(pem_files, 1):
                    name = file.stem.replace("_private", "")
                    print(f"{i}. {name}")
        
        # Solicitar el nombre base de las claves
        key_name = input("\nIngrese el nombre de las claves a cargar: ").strip()
        
        if not key_name:
            print("❌ Nombre inválido")
            input("\nPresione Enter para continuar...")
            return
        
        # Verificar si necesita contraseña
        password = None
        needs_password = input("¿La clave privada está protegida con contraseña? (s/n): ").lower()
        if needs_password == 's':
            password = input("Ingrese la contraseña: ")
        
        try:
            # Cargar claves
            private_path = os.path.join("keys", f"{key_name}_private.pem")
            public_path = os.path.join("keys", f"{key_name}_public.pem")
            cert_path = os.path.join("keys", f"{key_name}_cert.pem")
            
            self.current_private_key = self.key_manager.load_private_key(private_path, password)
            self.current_public_key = self.key_manager.load_public_key(public_path)
            
            # Cargar certificado si existe
            if os.path.exists(cert_path):
                self.current_certificate = self.key_manager.load_certificate(cert_path)
            
            self.current_key_name = key_name
            
            print("\n✅ ¡Claves cargadas exitosamente!")
            
        except Exception as e:
            print(f"\n❌ Error al cargar las claves: {str(e)}")
        
        print("="*60)
        input("\nPresione Enter para continuar...")
    
    def sign_document(self):
        """Opción 3: Firmar un documento."""
        print("\n" + "="*60)
        print("FIRMAR UN DOCUMENTO")
        print("="*60)
        
        # Verificar que hay claves cargadas
        if not self.current_private_key:
            print("\n❌ Error: Primero debe generar o cargar un par de claves")
            input("\nPresione Enter para continuar...")
            return
        
        # Solicitar la ruta del documento
        doc_path = input("\nIngrese la ruta del documento a firmar: ").strip()
        
        # Verificar que el archivo existe
        if not os.path.exists(doc_path):
            print(f"\n❌ Error: El archivo '{doc_path}' no existe")
            input("\nPresione Enter para continuar...")
            return
        
        # Nombre para la firma
        output_name = input("Nombre para el archivo de firma (o Enter para usar el predeterminado): ").strip()
        
        print("\n" + "-"*60)
        
        try:
            # Firmar el documento
            if output_name:
                signature_path = self.signature_manager.sign_and_save(
                    doc_path,
                    self.current_private_key,
                    self.current_certificate,
                    output_name
                )
            else:
                signature_path = self.signature_manager.sign_and_save(
                    doc_path,
                    self.current_private_key,
                    self.current_certificate
                )
            
            # Cargar y mostrar la firma
            signature_data = self.signature_manager.load_signature(signature_path)
            self.signature_manager.display_signature_info(signature_data)
            
            print("✅ ¡Documento firmado exitosamente!")
            
        except Exception as e:
            print(f"\n❌ Error al firmar el documento: {str(e)}")
        
        print("="*60)
        input("\nPresione Enter para continuar...")
    
    def verify_signature(self):
        """Opción 4: Verificar una firma."""
        print("\n" + "="*60)
        print("VERIFICAR UNA FIRMA")
        print("="*60)
        
        # Solicitar rutas
        doc_path = input("\nIngrese la ruta del documento: ").strip()
        sig_path = input("Ingrese la ruta del archivo de firma (.json): ").strip()
        
        # Verificar que los archivos existen
        if not os.path.exists(doc_path):
            print(f"\n❌ Error: El documento '{doc_path}' no existe")
            input("\nPresione Enter para continuar...")
            return
        
        if not os.path.exists(sig_path):
            print(f"\n❌ Error: El archivo de firma '{sig_path}' no existe")
            input("\nPresione Enter para continuar...")
            return
        
        # Solicitar la clave pública
        pub_key_path = input("Ingrese la ruta de la clave pública (.pem): ").strip()
        
        if not os.path.exists(pub_key_path):
            print(f"\n❌ Error: La clave pública '{pub_key_path}' no existe")
            input("\nPresione Enter para continuar...")
            return
        
        print("\n" + "-"*60)
        
        try:
            # Cargar la clave pública
            public_key = self.key_manager.load_public_key(pub_key_path)
            
            # Cargar la firma
            signature_data = self.signature_manager.load_signature(sig_path)
            
            # Mostrar información de la firma
            self.signature_manager.display_signature_info(signature_data)
            
            # Cargar certificado si existe
            cert_path = pub_key_path.replace("_public.pem", "_cert.pem")
            certificate = None
            if os.path.exists(cert_path):
                certificate = self.key_manager.load_certificate(cert_path)
            
            # Verificar
            results = self.verifier.full_verification(
                doc_path,
                signature_data,
                public_key,
                certificate
            )
            
            # Mostrar resultados
            self.verifier.display_verification_results(results)
            
        except Exception as e:
            print(f"\n❌ Error durante la verificación: {str(e)}")
        
        print("="*60)
        input("\nPresione Enter para continuar...")
    
    def show_certificate_info(self):
        """Opción 5: Mostrar información del certificado actual."""
        print("\n" + "="*60)
        print("INFORMACIÓN DEL CERTIFICADO")
        print("="*60)
        
        if not self.current_certificate:
            print("\n❌ No hay certificado cargado")
            print("   Primero debe generar o cargar un par de claves")
        else:
            cert_info = self.key_manager.get_certificate_info(self.current_certificate)
            
            print("\n📜 Detalles del Certificado:")
            print("-" * 60)
            for key, value in cert_info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("-" * 60)
        
        print("="*60)
        input("\nPresione Enter para continuar...")
    
    def show_help(self):
        """Opción 6: Mostrar ayuda sobre firma digital."""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║              ¿CÓMO FUNCIONA LA FIRMA DIGITAL?               ║
╚══════════════════════════════════════════════════════════════╝

📚 CONCEPTOS FUNDAMENTALES:

1️⃣  CRIPTOGRAFÍA ASIMÉTRICA (RSA)
   • Se genera un PAR de claves matemáticamente relacionadas
   • Clave PRIVADA: Secreta, solo tú la conoces (para firmar)
   • Clave PÚBLICA: Puede compartirse libremente (para verificar)

2️⃣  HASH CRIPTOGRÁFICO (SHA-256)
   • Genera una "huella digital" única del documento
   • Cualquier cambio mínimo produce un hash completamente diferente
   • Tamaño fijo de 256 bits, sin importar el tamaño del documento

3️⃣  PROCESO DE FIRMA:
   a) Se calcula el hash SHA-256 del documento
   b) El hash se "cifra" con tu clave PRIVADA (esto es la firma)
   c) La firma se guarda junto con metadatos

4️⃣  PROCESO DE VERIFICACIÓN:
   a) Se recalcula el hash del documento recibido
   b) La firma se "descifra" con la clave PÚBLICA
   c) Si ambos hashes coinciden = FIRMA VÁLIDA

🔒 GARANTÍAS DE SEGURIDAD:

✓ AUTENTICIDAD: Solo el dueño de la clave privada pudo crear la firma
✓ INTEGRIDAD: Cualquier cambio en el documento se detecta
✓ NO REPUDIO: El firmante no puede negar haber firmado

⚠️  IMPORTANTE:
   • NUNCA compartas tu clave privada
   • Protégela con contraseña
   • La clave pública SÍ puede compartirse

═══════════════════════════════════════════════════════════════

📖 FLUJO DE TRABAJO TÍPICO:

1. Alice genera su par de claves y certificado
2. Alice firma un contrato con su clave privada
3. Alice envía a Bob: contrato + firma + clave pública
4. Bob verifica la firma con la clave pública de Alice
5. Bob confirma que el contrato es auténtico y no fue alterado

═══════════════════════════════════════════════════════════════
        """
        print(help_text)
        input("\nPresione Enter para continuar...")
    
    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        while True:
            # Limpiar pantalla (compatible con Windows y Unix)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            self.print_header()
            self.print_menu()
            
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.generate_keys()
            elif choice == '2':
                self.load_keys()
            elif choice == '3':
                self.sign_document()
            elif choice == '4':
                self.verify_signature()
            elif choice == '5':
                self.show_certificate_info()
            elif choice == '6':
                self.show_help()
            elif choice == '0':
                print("\n👋 ¡Gracias por usar el Sistema de Firma Digital!")
                print("   Desarrollado por Grupo 3\n")
                break
            else:
                print("\n❌ Opción inválida. Intente nuevamente.")
                input("\nPresione Enter para continuar...")


def main():
    """Función principal de entrada."""
    try:
        app = DigitalSignatureApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
