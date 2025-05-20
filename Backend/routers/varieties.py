from fastapi import APIRouter

router = APIRouter(prefix="/varieties", 
                   tags=["varieties"],
                   responses={404: {"massage": "No encontrado"}})

@router.get("/")
async def varieties():
    return {"Variedades": "Pantalla de Variedades"}

@router.get("/{id}")
async def varieties(id: int):
    return {"Variedades": "Pantalla de Variedades"}