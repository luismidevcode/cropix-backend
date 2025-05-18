from fastapi import APIRouter

router = APIRouter(prefix="/variedades", 
                   tags=["Variedades"],
                   responses={404: {"massage": "No encontrado"}})

@router.get("/")
async def variedades():
    return {"Variedades": "Pantalla de Variedades"}

@router.get("/{id}")
async def variedades(id: int):
    return {"Variedades": "Pantalla de Variedades"}