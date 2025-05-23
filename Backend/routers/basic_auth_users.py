from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="Login")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disebled: bool

class UserDB(User):
    password: str

users_db = {
    "luismiguel": {
        "username": "luismiguel",
        "fullname": "Luis Miguel",
        "email": "luismiguel@gmail.com",
        "disebled": True,
        "password": "luismiguel123"
    },
    "luismiguel2": {
        "username": "luismiguel2",
        "fullname": "Luis Miguel2",
        "email": "luismiguel@gmail.com",
        "disebled": True,
        "password": "luismiguel12345"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
  
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación no válidas", 
            headers={"WWW-Authenticate": "Bearer"})
    if user.disebled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario deshabilitado")
    return user
    
@app.post("/login")
async def Login(form: OAuth2PasswordRequestForm = Depends()):
   user_db = users_db.get(form.username)
   if not user_db:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")  
   
   user = search_user_db(form.username)
   if not form.password == user.password:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta") 

   return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user