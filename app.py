from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos la ruta /scan
@app.get("/scan")
def scan_headers(url: str):
    return {
        "url": url,
        "security_score": 75,
        "vulnerabilities": ["Falta cabecera X-Frame-Options"]
    }

# Manejo de React (Static Files)
BASE_DIR = Path(__file__).resolve().parent
frontend_dist = BASE_DIR / "dist"  # Tu dist está en la raíz según la barra lateral

if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        # AQUÍ ESTÁ EL CAMBIO: Excluimos 'scan' para que no devuelva index.html
        if full_path.startswith("api/") or full_path == "scan":
            return {"error": "Endpoint no encontrado"}
        
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(frontend_dist / "index.html"))
