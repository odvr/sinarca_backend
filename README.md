# Sinarca 


Sinarca es un software diseñado para ayudar a las ganaderías a mejorar la eficiencia y productividad de sus operaciones. Con esta aplicación, los ganaderos pueden automatizar tareas repetitivas y manuales, llevar un registro preciso y actualizado de los animales y sus actividades veterinarias, tomar decisiones informadas basadas en datos precisos y actualizados. La aplicación también puede ayudar a mejorar la comunicación y colaboración entre los diferentes departamentos y personas involucradas en la ganadería, así como facilitar el cumplimiento de las regulaciones y normativas relacionadas con la ganadería en Colombia. Con esta aplicación de gestión de ganadería los ganaderos pueden optimizar los procesos, mejorar la rentabilidad y aumentar la eficiencia en la gestión de su ganadería.


<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://reactjs.org/" target="_blank" rel="noreferrer"> 
 <a href="https://mariadb.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/mariadb/mariadb-icon.svg" alt="mariadb" width="40" height="40"/> </a>




# Librerias requeridas

Pip install sqlalchemy    --->  recibe los pasos de como instalar   [sqlalchemy](https://pypi.org/project/SQLAlchemy/).

Pip install uvicorn --->  recibe los pasos de como instalar  [uvicorn](https://pypi.org/project/uvicorn/).

pip3 install mariadb  --->  recibe los pasos de como instalar [mariadb](https://pypi.org/project/mariadb/ ).

pip install fastapi  --->  recibe los pasos de como instalar [fastapi](https://pypi.org/project/fastapi/).


pip install python-multipart

pip install python-jose
pip install passlib
bcrypt

## Crea la Base de datos :

CREATE DATABASE `sinarca` /*!40100 COLLATE 'latin1_bin' */;

## Inicia el Backend 
uvicorn app:app –reload permite reinicar con cada cambio en el código 



