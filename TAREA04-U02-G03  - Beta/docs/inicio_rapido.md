# Guía de Inicio Rápido

## ⚡ Instalación Rápida

```powershell
# Opción 1: Script automático
.\setup.ps1

# Opción 2: Manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 🚀 Uso Básico en 3 Pasos

### Paso 1: Ejecutar la aplicación
```bash
cd src
python main.py
```

### Paso 2: Generar tus claves
1. Selecciona opción **1** (Generar claves)
2. Ingresa tu información
3. Define un nombre (ej: "mi_identidad")

### Paso 3: Firmar un documento
1. Coloca tu documento en `documents/`
2. Selecciona opción **3** (Firmar)
3. Ingresa la ruta del documento
4. ¡Listo! Tu firma está en `signatures/`

---

## 📝 Ejemplos Prácticos

### Ejemplo 1: Firma Simple

```
1. Ejecutar: python main.py
2. Opción 1 → Generar claves
   - Nombre: Juan Pérez
   - Organización: Mi Empresa
   - Nombre de claves: juan
   
3. Opción 3 → Firmar documento
   - Documento: ../documents/ejemplo_contrato.txt
   - Nombre firma: contrato_firmado
   
4. Resultado:
   ✓ keys/juan_private.pem
   ✓ keys/juan_public.pem
   ✓ keys/juan_cert.pem
   ✓ signatures/contrato_firmado.json
```

### Ejemplo 2: Verificar Firma

```
1. Ejecutar: python main.py
2. Opción 4 → Verificar firma
   - Documento: documents/ejemplo_contrato.txt
   - Firma: signatures/contrato_firmado.json
   - Clave pública: keys/juan_public.pem
   
3. Resultado:
   ✅ FIRMA VÁLIDA - Documento auténtico
```

### Ejemplo 3: Detectar Modificación

```
1. Modificar el documento firmado
2. Intentar verificar la firma
3. Resultado:
   ❌ FIRMA INVÁLIDA - Documento modificado
```

---

## 🎯 Casos de Uso

### Caso 1: Firmar Contrato
**Escenario**: Necesitas firmar digitalmente un contrato.

```
Archivo: contrato_servicios.docx
Firmante: Ana García (Gerente)

Pasos:
1. Generar claves de Ana
2. Firmar contrato
3. Enviar: contrato + firma + clave pública
4. Receptor verifica con clave pública
```

### Caso 2: Verificar Autenticidad
**Escenario**: Recibiste un documento firmado.

```
Recibiste:
- documento.pdf
- documento_signature.json  
- emisor_public.pem

Pasos:
1. Cargar archivos
2. Verificar firma
3. Confirmar autenticidad
```

### Caso 3: Múltiples Firmantes
**Escenario**: Varias personas firman el mismo documento.

```
Documento: acta_reunion.txt

1. Ana firma → acta_firma_ana.json
2. Bob firma → acta_firma_bob.json
3. Carol firma → acta_firma_carol.json

Cada uno usa su clave privada.
Cada firma se verifica independientemente.
```

---

## 🔍 Comandos Útiles

### Ver archivos generados
```powershell
# Ver claves
Get-ChildItem keys\

# Ver firmas
Get-ChildItem signatures\

# Ver documentos
Get-ChildItem documents\
```

### Verificar hash de archivo
```python
import hashlib

def get_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Comparar
hash1 = get_hash("documento_original.txt")
hash2 = get_hash("documento_copia.txt")
print(hash1 == hash2)  # True si son idénticos
```

---

## ⚠️ Problemas Comunes

### Error: "No se encontró el módulo cryptography"
**Solución**:
```bash
pip install cryptography
```

### Error: "Archivo no encontrado"
**Solución**: Usar rutas relativas correctas
```
Correcto: ../documents/archivo.txt
Incorrecto: documents/archivo.txt (si estás en src/)
```

### Error: "Contraseña incorrecta"
**Solución**: Verificar que usas la misma contraseña con la que protegiste la clave

### La firma no verifica
**Posibles causas**:
1. Documento fue modificado
2. Clave pública incorrecta
3. Archivo de firma corrupto

---

## 🎓 Ejercicios Prácticos

### Ejercicio 1: Primera Firma
1. Genera tu par de claves
2. Crea un documento de texto simple
3. Fírmalo
4. Verifica la firma

### Ejercicio 2: Detectar Cambios
1. Firma un documento
2. Modifica UNA letra del documento
3. Intenta verificar
4. Observa que la verificación falla

### Ejercicio 3: Intercambio de Firmas
1. Persona A genera claves
2. Persona A firma documento
3. Persona B recibe documento + firma + clave pública de A
4. Persona B verifica la firma

### Ejercicio 4: Ver Información
1. Genera un certificado
2. Usa opción 5 para ver detalles
3. Identifica: nombre, organización, validez

---

## 📚 Recursos Adicionales

- **Guía Técnica**: Ver `docs/guia_tecnica.md`
- **README Completo**: Ver `README.md`
- **Tests**: Ver `tests/test_digital_signature.py`

---

## 💡 Tips

✅ **Siempre** protege tu clave privada con contraseña
✅ Haz backup de tus claves en lugar seguro
✅ Verifica firmas ANTES de confiar en documentos
✅ Usa nombres descriptivos para tus archivos

❌ **Nunca** compartas tu clave privada
❌ No uses claves de prueba en producción
❌ No confíes en documentos sin verificar la firma

---

## 🆘 Soporte

¿Necesitas ayuda?
1. Revisa la opción **6** (Ayuda) en el menú
2. Consulta `README.md`
3. Revisa `docs/guia_tecnica.md`
4. Ejecuta los tests: `pytest tests/ -v`
