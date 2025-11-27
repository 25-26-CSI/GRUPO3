# 🚀 INSTRUCCIONES DE EJECUCIÓN

## Inicio Rápido (5 minutos)

### Opción 1: Instalación Automática (Recomendado)

```powershell
# 1. Abrir PowerShell en el directorio del proyecto
cd C:\Proyectos\GRUPO3\TAREA04-U02-G03

# 2. Ejecutar script de instalación
.\setup.ps1

# 3. Ejecutar la aplicación
cd src
python main.py
```

### Opción 2: Instalación Manual

```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
cd src
python main.py
```

---

## 🎮 Modos de Uso

### 1. Modo Interactivo (Recomendado para Aprender)

```bash
cd src
python main.py
```

**Funcionalidades**:
- Menú interactivo con 6 opciones
- Ayuda integrada
- Flujo guiado paso a paso

**Ideal para**:
- Primera vez usando el sistema
- Aprender cómo funciona
- Explorar todas las características

### 2. Modo Demostración (Automático)

```bash
cd src
python demo.py
```

**Funcionalidades**:
- Demostración completa automática
- Genera claves para Alice y Bob
- Firma y verifica documentos
- Muestra detección de modificaciones

**Ideal para**:
- Presentaciones
- Ver el sistema en acción sin interacción
- Entender el flujo completo

---

## 📋 Primer Uso - Tutorial Paso a Paso

### Paso 1: Ejecutar la Aplicación

```bash
cd src
python main.py
```

Verás el menú principal:

```
╔══════════════════════════════════════════════════════════════╗
║        🔐 SISTEMA DE FIRMA DIGITAL DE DOCUMENTOS 🔐         ║
╚══════════════════════════════════════════════════════════════╝

MENÚ PRINCIPAL
==============================================================
1. 🔑 Generar nuevo par de claves y certificado
2. 📂 Cargar claves existentes
3. ✍️  Firmar un documento
4. ✅ Verificar una firma
5. 📋 Ver información del certificado actual
6. ℹ️  Ayuda - ¿Cómo funciona la firma digital?
0. 🚪 Salir
```

### Paso 2: Generar Tus Claves

1. Selecciona opción `1`
2. Completa tu información:
   ```
   Nombre completo: [Tu nombre]
   Organización: ESPOL
   Ciudad: Guayaquil
   Estado/Provincia: Guayas
   País: EC
   ```
3. Nombra tus claves: `mi_identidad`
4. Protege con contraseña: `s` → Ingresa una contraseña

**Resultado**: Se crean 3 archivos en `keys/`:
- `mi_identidad_private.pem` (¡MANTENER SEGURA!)
- `mi_identidad_public.pem`
- `mi_identidad_cert.pem`

### Paso 3: Preparar un Documento

Usa el documento de ejemplo o crea uno nuevo:

```bash
# El proyecto incluye un ejemplo
# Ubicación: documents/ejemplo_contrato.txt

# O crea uno nuevo:
echo "Este es mi documento importante" > documents/mi_documento.txt
```

### Paso 4: Firmar el Documento

1. Selecciona opción `3`
2. Ruta del documento: `../documents/ejemplo_contrato.txt`
3. Nombre de firma: `firma_contrato`

**Resultado**: Se crea `signatures/firma_contrato.json`

### Paso 5: Verificar la Firma

1. Selecciona opción `4`
2. Completa:
   ```
   Ruta del documento: ../documents/ejemplo_contrato.txt
   Ruta de firma: ../signatures/firma_contrato.json
   Clave pública: ../keys/mi_identidad_public.pem
   ```

**Resultado**: 
```
🎉 RESULTADO FINAL: FIRMA VÁLIDA Y AUTÉNTICA
```

---

## 🧪 Ejecutar Tests

### Todos los Tests

```bash
# Desde la raíz del proyecto
python -m pytest tests/ -v
```

### Test Específico

```bash
pytest tests/test_digital_signature.py::TestKeyManager -v
```

### Con Cobertura

```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 🔧 Solución de Problemas

### Problema: "python no se reconoce"

**Solución**:
```powershell
# Verificar que Python está instalado
python --version

# Si no está instalado, descargar de python.org
# Versión mínima: Python 3.8
```

### Problema: Error al activar entorno virtual

**Solución**:
```powershell
# Permitir ejecución de scripts (solo una vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego volver a intentar
.\venv\Scripts\Activate.ps1
```

### Problema: "ModuleNotFoundError: No module named 'cryptography'"

**Solución**:
```bash
# Asegúrate de estar en el entorno virtual
.\venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: Error de rutas en Windows

**Solución**:
```python
# Usar rutas absolutas o relativas correctamente
# Desde src/, usar: ../documents/archivo.txt
# No usar: documents/archivo.txt
```

---

## 📁 Estructura de Directorios Después de Usar

```
TAREA04-U02-G03/
│
├── keys/
│   ├── mi_identidad_private.pem    ← Tu clave privada
│   ├── mi_identidad_public.pem     ← Tu clave pública
│   └── mi_identidad_cert.pem       ← Tu certificado
│
├── signatures/
│   └── firma_contrato.json         ← Firma generada
│
├── documents/
│   ├── ejemplo_contrato.txt        ← Documento de ejemplo
│   └── mi_documento.txt            ← Tus documentos
│
└── venv/                            ← Entorno virtual Python
```

---

## 💻 Comandos Útiles

### Ver Contenido de Archivos

```powershell
# Ver clave pública (PEM)
Get-Content keys\mi_identidad_public.pem

# Ver firma (JSON - más legible)
Get-Content signatures\firma_contrato.json | ConvertFrom-Json | ConvertTo-Json
```

### Limpiar Archivos Generados

```powershell
# Eliminar todas las claves generadas (¡CUIDADO!)
Remove-Item keys\*.pem

# Eliminar todas las firmas
Remove-Item signatures\*.json
```

### Verificar Instalación de Dependencias

```python
python -c "import cryptography; print('cryptography OK')"
python -c "import PyPDF2; print('PyPDF2 OK')"
python -c "import colorama; print('colorama OK')"
python -c "import pydantic; print('pydantic OK')"
```

---

## 🎯 Escenarios de Uso Comunes

### Escenario 1: Firma Rápida

```bash
# Iniciar aplicación
python main.py

# Opción 1 → Generar claves
# Opción 3 → Firmar documento
# ¡Listo en 2 minutos!
```

### Escenario 2: Solo Verificar

```bash
# Si alguien te envió un documento firmado
python main.py

# Opción 4 → Verificar firma
# Proporciona: documento, firma, clave pública
```

### Escenario 3: Múltiples Firmas

```bash
# Generar claves para cada persona
python main.py
# Opción 1 → Guardar como "persona1"

# Cada persona firma el mismo documento
# Opción 3 → Cada uno con su clave privada

# Resultado: Múltiples archivos de firma
# firma_persona1.json
# firma_persona2.json
```

---

## 📖 Recursos de Ayuda

### Dentro de la Aplicación

```
Opción 6 del menú principal
→ Explicación completa de firma digital
→ Conceptos criptográficos
→ Flujo de trabajo
```

### Documentación

```
README.md              → Guía completa
docs/inicio_rapido.md  → Tutorial rápido
docs/guia_tecnica.md   → Detalles técnicos
RESUMEN_PROYECTO.md    → Resumen ejecutivo
```

### Demostración

```bash
cd src
python demo.py
```

---

## ⚡ Atajos Rápidos

### Workflow Completo en 3 Comandos

```powershell
# 1. Instalar
.\setup.ps1

# 2. Ejecutar demo
cd src; python demo.py

# 3. Usar interactivamente
python main.py
```

### Solo Instalar y Probar

```powershell
pip install -r requirements.txt
cd src
python demo.py
```

---

## 🎓 Para Presentaciones/Demostraciones

### Preparación (antes de la presentación)

```powershell
# 1. Asegurarse de que todo está instalado
.\setup.ps1

# 2. Limpiar archivos previos (opcional)
Remove-Item keys\*.pem
Remove-Item signatures\*.json
```

### Durante la Presentación

**Opción A: Demostración Automática (más rápido)**
```bash
cd src
python demo.py
# Se ejecuta solo, muestra todo el proceso
```

**Opción B: Demostración Interactiva (más control)**
```bash
python main.py
# Seguir los pasos manualmente explicando cada uno
```

---

## 📊 Verificar que Todo Funciona

### Checklist de Verificación

```bash
# ✓ Python instalado
python --version  # Debe mostrar 3.8+

# ✓ Dependencias instaladas
pip list | findstr cryptography  # Debe aparecer

# ✓ Aplicación arranca
cd src
python main.py  # Debe mostrar el menú

# ✓ Demo funciona
python demo.py  # Debe completar sin errores

# ✓ Tests pasan
cd ..
pytest tests/ -v  # Todos deben pasar
```

---

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa** la sección de solución de problemas arriba
2. **Consulta** README.md y la documentación en docs/
3. **Ejecuta** los tests para verificar el sistema
4. **Verifica** que Python 3.8+ está instalado

---

**¡Listo para usar! 🎉**

El sistema está completamente funcional y documentado.
Comienza con `python main.py` o `python demo.py`
