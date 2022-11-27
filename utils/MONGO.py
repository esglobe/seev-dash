# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

import yaml 
import os

# Definiendo variables
# with open('./config.yml') as stream:
#     config = yaml.safe_load(stream)

print(os.environ['MONGO_USER'])

# Objeto para la conexión
class CONEXION:
    """
    Calse para la conexión a mongo DB
    """
    username = os.environ['MONGO_USER']
    password = os.environ['MONGO_PASSWORD']
    cluster = os.environ['MONGO_CLUSTER']

    @classmethod
    def conexion(cls):
      
      import pymongo

      conn_str = f"mongodb+srv://{CONEXION.username}:{CONEXION.password}@{CONEXION.cluster}.wsg1gnp.mongodb.net/?retryWrites=true&w=majority"
      cliente = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

      return cliente['SSEV']

