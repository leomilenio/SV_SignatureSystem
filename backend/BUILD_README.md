# Scripts de Build y Despliegue del Frontend

Este directorio contiene scripts para automatizar el proceso de compilación y despliegue del frontend de Signance System.

## Archivos Disponibles

### Scripts Principales

1. **`build_and_deploy_frontend.py`** - Script principal en Python
   - Funcionalidad completa con retroalimentación detallada
   - Manejo de errores robusto
   - Backup automático de archivos estáticos
   - Multiplataforma (Windows, macOS, Linux)

2. **`quick_build.py`** - Script simplificado para builds rápidos
   - Versión minimalista del script principal
   - Ideal para desarrollo

### Scripts de Conveniencia

3. **`build_and_deploy_frontend.sh`** - Script shell para Unix/Linux/macOS
   - Wrapper que llama al script Python
   - Fácil de ejecutar desde terminal

4. **`build_and_deploy_frontend.bat`** - Script batch para Windows
   - Wrapper que llama al script Python
   - Fácil de ejecutar haciendo doble clic

## Uso

### Opción 1: Script Python (Recomendado)
```bash
cd backend
python build_and_deploy_frontend.py
```

### Opción 2: Script Shell (macOS/Linux)
```bash
cd backend
./build_and_deploy_frontend.sh
```

### Opción 3: Script Batch (Windows)
```cmd
cd backend
build_and_deploy_frontend.bat
```

### Opción 4: Build Rápido
```bash
cd backend
python quick_build.py
```

## ¿Qué Hace el Script?

1. **Verificación**: Comprueba que existe la estructura necesaria
2. **Dependencias**: Instala dependencias de npm si es necesario
3. **Build**: Ejecuta `npm run build` en la carpeta frontend
4. **Backup**: Crea respaldo de archivos estáticos actuales
5. **Despliegue**: Copia archivos compilados a `backend/app/static/`
6. **Limpieza**: Elimina archivos temporales

## Requisitos

- **Node.js y npm** instalados
- **Python 3.6+** 
- Estructura de proyecto:
  ```
  Signance System/
  ├── frontend/          # Proyecto Vue.js
  │   ├── package.json
  │   └── src/
  └── backend/           # Proyecto FastAPI
      ├── app/
      │   └── static/    # Destino de archivos compilados
      └── build_*.py     # Scripts de build
  ```

## Resultado

Después de ejecutar el script:

- Los archivos del frontend estarán disponibles en `backend/app/static/`
- El backend podrá servir la aplicación desde la ruta raíz (`/`)
- Se crea un backup automático de archivos anteriores
- La aplicación estará lista para producción

## Troubleshooting

### Error: npm no encontrado
```bash
# macOS con Homebrew
brew install node

# Ubuntu/Debian
sudo apt install nodejs npm

# Windows - Descargar desde nodejs.org
```

### Error: Python no encontrado
```bash
# macOS con Homebrew
brew install python

# Ubuntu/Debian
sudo apt install python3

# Windows - Descargar desde python.org
```

### Error: Permisos en scripts shell
```bash
chmod +x build_and_deploy_frontend.sh
```

## Notas de Desarrollo

- Los scripts crean backups automáticos en `static_backup_[timestamp]`
- Los builds son incrementales si ya existen `node_modules`
- Se puede ejecutar el script desde cualquier directorio
- Compatible con entornos virtuales de Python

## Integración con CI/CD

Para integrar con sistemas de CI/CD, use el script Python directamente:

```yaml
# Ejemplo GitHub Actions
- name: Build and Deploy Frontend
  run: |
    cd backend
    python build_and_deploy_frontend.py
```
