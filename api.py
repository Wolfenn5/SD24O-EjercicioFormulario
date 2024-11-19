from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os # para acceder al HOME de la pc
import uuid # para generar nombres aleatorios unicos como si fuera un hash

# el checkbox es un booleano

# http://127.0.0.1:5500/test.html poner el /test.html cuando se use live server y luego el go live

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    edad:int
    domicilio:str    
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]



# Form(...) es un operador elipsis
# si se usa un await, se debe especificar que la funcion es asincrona, por lo que se explica de read y python lo corre en un hilo
# si no entonces puede que la funcion termine y siga corriendo el hilo
@app.post("/fotos")
async def guarda_foto(titulo:str=Form(None), descripcion:str=Form(...), foto:UploadFile=File(...)):
    print("Titulo: ", titulo)
    print("Descripcion: ", descripcion)
    home_usuario = os.path.expanduser("~") # se obtiene el HOME del usuario
    nombre_archivo = uuid.uuid4() # se obtiene un nombre en formato hexadecimal
    extension_foto = os.path.splitext(foto.filename)[1] # una tupla donde el primer elemento es el nombre del archivo y el segundo es la extension del archivo -> [0] gato   [1] png
    ruta_imagen = f'{home_usuario}/fotos_ejemplo/{nombre_archivo}{extension_foto}'
    print("Guardando la foto en ", ruta_imagen)
    with open(ruta_imagen,"wb") as imagen: # objeto imagen se refiere al archivo que se esta creando justo aqui
        contenido = await foto.read() # extraer el contenido, read se hace de forma asincrona (python lo deja corriendo en un hilo)
        imagen.write(contenido)

    respuesta = {
        "Titulo": titulo,
        "Descripcion": descripcion,
        "Ruta": ruta_imagen
    }
    return respuesta
# En este caso especifico se guarda en: C:\Users\btosk\fotos_ejemplo






# Post para usuarios
@app.post("/usuarios")
async def guarda_usuarios(nombre:str=Form(None), direccion:str=Form(...), checkbox:bool=Form(False), fotografia:UploadFile=File(...)): # con checkbox:bool=Form(False) indica que si no se marca la casilla, por dafault es false
    print("Nombre: ", nombre)
    print("Direccion: ", direccion)
    home_usuario = os.path.expanduser("~") # se obtiene el HOME del usuario
    nombre_archivo = uuid.uuid4() # se obtiene un nombre en formato hexadecimal
    extension_foto = os.path.splitext(fotografia.filename)[1] # una tupla donde el primer elemento es el nombre del archivo y el segundo es la extension del archivo -> [0] nombre_foto   [1] png
      

    if checkbox: # si se marca que es vip 
        ruta_imagen = f'{home_usuario}/fotos-usuarios-vip/{nombre_archivo}{extension_foto}'
    else:
        ruta_imagen = f'{home_usuario}/fotos-usuarios/{nombre_archivo}{extension_foto}'
        

    with open(ruta_imagen,"wb") as imagen: # objeto imagen se refiere al archivo que se esta creando justo aqui
            contenido = await fotografia.read() # extraer el contenido, read se hace de forma asincrona (python lo deja corriendo en un hilo)
            imagen.write(contenido)

    respuesta = {
        "Nombre": nombre,
        "Direccion": direccion,
        "Ruta": ruta_imagen
    }
    return respuesta





# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


@app.get("/usuarios/{id}")
def usuario_por_id(id: int):
    print("buscando usuario por id:", id)
    # simulamos consulta a la base:
    return usuarios[id]


@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }

    return compra

@app.get("/usuarios")
def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
    print("lote:",lote, " pag:", pag, " orden:", orden)
    #simulamos la consulta
    return usuarios

@app.post("/usuarios")
def guardar_usuario(usuario:UsuarioBase, parametro1:str):
    print("usuario a guardar:", usuario, ", parametro1:", parametro1)
    #simulamos guardado en la base.
    
    usr_nuevo = {}
    usr_nuevo["id"] = len(usuarios)
    usr_nuevo["nombre"] = usuario.nombre
    usr_nuevo["edad"] = usuario.edad
    usr_nuevo["domicilio"] = usuario.domicilio

    usuarios.append(usuario)

    return usr_nuevo

@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int):
    #simulamos una consulta
    if id>=0 and id< len(usuarios):
        usuario = usuarios[id]
    else:
        usuario = None
    
    if usuario is not None:
        usuarios.remove(usuario)
    
    return {"status_borrado", "ok"}
