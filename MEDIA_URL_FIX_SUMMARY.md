# Corrección de URLs de Media - Signance System

## Problemas Identificados y Solucionados

### 1. **URLs Hardcodeadas en el Frontend**
- ❌ **Problema**: URLs como `http://127.0.0.1:8002` estaban hardcodeadas
- ✅ **Solución**: Creado composable `useMediaUrl` para detección automática

### 2. **Función async en Template**
- ❌ **Problema**: `getMediaUrl` era async pero se usaba en template sin await
- ✅ **Solución**: Composable reactivo que maneja URLs automáticamente

### 3. **Inconsistencia en Detección del Backend**
- ❌ **Problema**: Múltiples sistemas de detección duplicados
- ✅ **Solución**: Sistema centralizado con `useMediaUrl`

## Cambios Realizados

### 1. **Nuevo Composable: `useMediaUrl.js`**
```javascript
// Maneja automáticamente:
- Detección del backend
- Construcción de URLs de media
- Fallback a localhost:8000
- Reactive updates
```

### 2. **PlayerView.vue Actualizado**
- Usa `useMediaUrl` composable
- Función `getMediaUrl` simplificada
- URLs dinámicas basadas en detección automática

### 3. **AdminView.vue Actualizado**
- Usa `useMediaUrl` composable
- Eliminada lógica duplicada de detección
- URLs consistentes en toda la aplicación

### 4. **API.js Mejorado**
- Mejor manejo de errores
- Fallback más robusto
- Logging mejorado para debugging

## URLs Correctas del Sistema

### Backend Monta Archivos Como:
```
app.mount("/uploads", StaticFiles(directory="media/uploads"))
```

### Frontend Accede Como:
```
http://[IP_BACKEND]:[PUERTO]/uploads/[ARCHIVO]
```

### Ejemplo:
```
http://192.168.100.186:8000/uploads/ejemplo.jpg
```

## Testing

### Para probar conectividad usar en consola del navegador:
```javascript
// Función global disponible
window.debugSignanceConnection()
```

### Verificar URLs de media:
```javascript
// En PlayerView, verificar URLs generadas en console.log
```

## Solución del Error Original

El error `/uploads/` vs `/media/uploads/` era porque:
- Backend monta `/uploads` → `media/uploads` (correcto)
- Frontend usaba URLs hardcodeadas incorrectas
- Ahora usa detección automática + URLs correctas

## Resultado Esperado

✅ **Frontend desde localhost**: `http://127.0.0.1:8000/uploads/archivo.jpg`
✅ **Frontend desde IP de red**: `http://192.168.100.186:8000/uploads/archivo.jpg`
✅ **Detección automática**: Sin configuración manual
✅ **Fallback robusto**: Si falla detección, usa localhost:8000
