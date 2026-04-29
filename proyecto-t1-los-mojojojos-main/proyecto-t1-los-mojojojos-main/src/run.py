"""
Script para iniciar el servidor FastAPI.
EJECUTAR DESDE LA RAÍZ DEL PROYECTO, no desde src/
"""
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Asegurar que estamos en el directorio correcto
    # Si estamos en src/, subir un nivel
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent if current_dir.name == "src" else current_dir
    
    # Añadir la raíz del proyecto al path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    import uvicorn
    
    # Ejecutar desde la raíz del proyecto
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )