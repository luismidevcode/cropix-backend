from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={404: {"massage": "No encontrado"}})

#Entidad de usuario
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Luis Miguel", surname="luismi", url="luismiguel.com", age=25),
              User(id=2 ,name="Santiago", surname="Santi", url="santiago.com", age=30),
              User(id=3, name="Juan", surname="Juanito", url="juan.com", age=28)]
              
#Prueba manual
@router.get("/usersjson") 
async def usersjson():
    return [{"name": "Luis Miguel", "surname": "luismi","url": "luismiguel.com"}, 
            {"name": "Santiago", "surname": "Santi","url": "santiago.com"},
            {"name": "Juan", "surname": "Juanito","url": "juan.com"}]

#El que funciona
@router.get("/users")
async def users():
    return users_list

#Con el path param
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#Con el query param
@router.get("/user/")
async def user(id: int):
    return search_user(id)

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
       raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/user/")
async def user(user: User):
    found = False        
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:    
            users_list[index] = user
            found = True
    if not found:
        return {"error": "Usuario no actualizado"}        
    else:
        return user
    
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, delete_user in enumerate(users_list):
        if delete_user.id == id:    
            del users_list[index]
            return {"message": "Usuario eliminado"}  
            found = True
    # Si no se encontró el usuario, devolver un mensaje de error  
    if not found:
        return {"error": "Usuario no encontrado"}



def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Usuario no encontrado"}
    

    
  

    


