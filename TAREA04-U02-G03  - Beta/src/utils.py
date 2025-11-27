"""
Utilidades del Sistema de Firma Digital
========================================

Funciones auxiliares y herramientas de utilidad.
"""

import os
import json
from datetime import datetime
from typing import List, Dict


def format_bytes(bytes_value: int) -> str:
    """
    Formatea un tamaño en bytes a una representación legible.
    
    Args:
        bytes_value: Tamaño en bytes
    
    Returns:
        String formateado (ej: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"


def get_file_info(filepath: str) -> Dict[str, any]:
    """
    Obtiene información detallada de un archivo.
    
    Args:
        filepath: Ruta del archivo
    
    Returns:
        Diccionario con información del archivo
    """
    if not os.path.exists(filepath):
        return {"error": "Archivo no encontrado"}
    
    stat = os.stat(filepath)
    
    return {
        "nombre": os.path.basename(filepath),
        "ruta": os.path.abspath(filepath),
        "tamaño": format_bytes(stat.st_size),
        "tamaño_bytes": stat.st_size,
        "modificado": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "creado": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    }


def list_files_in_directory(directory: str, extension: str = None) -> List[str]:
    """
    Lista archivos en un directorio con filtro opcional.
    
    Args:
        directory: Directorio a listar
        extension: Extensión para filtrar (ej: ".pem", ".json")
    
    Returns:
        Lista de nombres de archivo
    """
    if not os.path.exists(directory):
        return []
    
    files = os.listdir(directory)
    
    if extension:
        files = [f for f in files if f.endswith(extension)]
    
    return sorted(files)


def print_table(headers: List[str], rows: List[List[str]]) -> None:
    """
    Imprime una tabla formateada en consola.
    
    Args:
        headers: Lista de encabezados
        rows: Lista de filas (cada fila es una lista de strings)
    """
    # Calcular anchos de columna
    col_widths = [len(h) for h in headers]
    
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Imprimir encabezados
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))
    
    # Imprimir filas
    for row in rows:
        print(" | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)))


def export_signature_summary(signature_files: List[str], output_file: str) -> None:
    """
    Exporta un resumen de múltiples firmas a un archivo JSON.
    
    Args:
        signature_files: Lista de rutas de archivos de firma
        output_file: Archivo de salida
    """
    summary = {
        "fecha_generacion": datetime.now().isoformat(),
        "total_firmas": len(signature_files),
        "firmas": []
    }
    
    for sig_file in signature_files:
        try:
            with open(sig_file, 'r', encoding='utf-8') as f:
                sig_data = json.load(f)
                
            summary["firmas"].append({
                "archivo": os.path.basename(sig_file),
                "documento": sig_data.get("document_name"),
                "timestamp": sig_data.get("timestamp"),
                "firmante": sig_data.get("signer", {}).get("nombre", "Desconocido")
            })
        except Exception as e:
            summary["firmas"].append({
                "archivo": os.path.basename(sig_file),
                "error": str(e)
            })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    
    print(f"Resumen exportado a: {output_file}")


def validate_key_pair(private_key_path: str, public_key_path: str) -> bool:
    """
    Valida que un par de claves correspondan entre sí.
    
    Args:
        private_key_path: Ruta de la clave privada
        public_key_path: Ruta de la clave pública
    
    Returns:
        True si son un par válido
    """
    try:
        from key_manager import KeyManager
        
        km = KeyManager()
        private_key = km.load_private_key(private_key_path)
        public_key = km.load_public_key(public_key_path)
        
        # Comparar la clave pública derivada de la privada con la cargada
        derived_public = private_key.public_key()
        
        # Serializar ambas para comparar
        from cryptography.hazmat.primitives import serialization
        
        derived_bytes = derived_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        loaded_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return derived_bytes == loaded_bytes
        
    except Exception as e:
        print(f"Error validando par de claves: {e}")
        return False


def create_backup(source_dir: str, backup_dir: str = "backup") -> None:
    """
    Crea un backup de claves y firmas.
    
    Args:
        source_dir: Directorio a respaldar
        backup_dir: Directorio de destino
    """
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    
    os.makedirs(backup_path, exist_ok=True)
    
    try:
        shutil.copytree(source_dir, os.path.join(backup_path, os.path.basename(source_dir)))
        print(f"✓ Backup creado en: {backup_path}")
    except Exception as e:
        print(f"✗ Error creando backup: {e}")


if __name__ == "__main__":
    # Pruebas de utilidades
    print("Probando utilidades...")
    
    # Test format_bytes
    print(f"\n1024 bytes = {format_bytes(1024)}")
    print(f"1048576 bytes = {format_bytes(1048576)}")
    
    # Test list_files
    print(f"\nArchivos .pem en keys/: {list_files_in_directory('../keys', '.pem')}")
    
    # Test tabla
    print("\nTabla de ejemplo:")
    print_table(
        ["Nombre", "Tamaño", "Tipo"],
        [
            ["documento1.txt", "1.5 KB", "Texto"],
            ["imagen.png", "245 KB", "Imagen"],
            ["video.mp4", "12.3 MB", "Video"]
        ]
    )
