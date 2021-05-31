# Como correr la aplicación móvil

---
## Requerimientos

1. Tener instalado python 3, pip y virtualenv

Asi se instala virtualenv
```
python3 -m pip install --user virtualenv
```

2. Estar en la terminal dentro de la carpeta de MobileApp (hacer algo como cd MobileApp)

---
## Pasos


1. Crear un virtual environment dentro de esta carpeta
```
virtualenv env
```
2. Activar env
```
source env/bin/activate
```
3. Instalar kivy y sus ejemplos
```
python3 -m pip install kivy[base] kivy_examples 
```

4. Correr aplicacion
```
python3 main.py 
```