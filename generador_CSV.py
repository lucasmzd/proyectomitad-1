# def guardar_csv(nombre_archivo: str, lista_diccionarios: list, separador: str = ";") -> bool:
#     if type(lista_diccionarios) != list or len(lista_diccionarios) == 0:
#         return False
#     diccionario = lista_diccionarios[0]
#     if type(diccionario) != dict:
#         return False
#     cabecera = crear_cabecera(diccionario, separador)
#     with open(nombre_archivo, "w", encoding="utf-8") as archivo:
#         archivo.write(f"{cabecera}\n")
#         indice = 0
#         while indice < len(lista_diccionarios):
#             dato = crear_dato_csv(lista_diccionarios[indice], separador)
#             archivo.write(dato)
#             if indice < len(lista_diccionarios) - 1:
#                 archivo.write("\n")
#             indice += 1

#     return True

# def leer_csv_preguntas(nombre_archivo:str, separador: str = ";") -> list | None:
#     lista_preguntas = []

#     if not os.path.exists(nombre_archivo):
#         return None

#     with open(nombre_archivo, "r", encoding="utf-8") as archivo:
#         lineas = archivo.readlines()  

#     if len(lineas) == 0:
#         return None
    
#     cabecera = separar_cadena(reemplazar_caracteres(lineas[0], "\n", ""), separador)
#     indice = 1
    
#     while indice < len(lineas):
#         fila = reemplazar_caracteres(lineas[indice], "\n", "")
#         if unir_cadena(separar_cadena(fila, " "), "") == "":
#             indice += 1
#             continue
#         valores = separar_cadena(fila, separador)
#         pregunta = {}
#         i = 0
#         while i < len(cabecera):
#             clave = cabecera[i]
#             valor = valores[i]
#             if clave == "respuesta_correcta":
#                 valor = int(valor)
#             pregunta[clave] = valor
#             i += 1
#         lista_preguntas.append(pregunta)
#         indice += 1

#     return lista_preguntas


# def crear_cabecera(diccionario: dict, separador: str = ",") -> str:
#     if type(diccionario) == dict:
#         lista_claves = list(diccionario.keys())
#         cabecera = unir_cadena(lista_claves, separador)
#     else:
#         cabecera = ""
#     return cabecera
       
# def crear_dato_csv(diccionario :dict, separador: str = ",") -> str:
#     if type(diccionario) == dict:
#         lista_valores = list(diccionario.values())
#         dato = unir_cadena(lista_valores, separador)
#     else:
#         dato = ""
#     return dato

# def reemplazar_caracteres(cadena:str,caracter_viejo:str,caracter_nuevo:str) -> str:
#     cadena_nueva = ""
    
#     for i in range(len(cadena)):
#         if cadena[i] == caracter_viejo:
#             cadena_nueva += caracter_nuevo
#         else:
#             cadena_nueva += cadena[i]
            
#     return cadena_nueva
            
# def separar_cadena(cadena:str,separador:str) -> list:
#     lista_separada = []
#     cadena_nueva = ""
#     if type(cadena) == str and (type(separador) == str and len(separador) == 1):
#         for i in range(len(cadena)):
#             if cadena[i] == separador:
#                 lista_separada.append(cadena_nueva)
#                 cadena_nueva = ""
#             else:
#                 cadena_nueva += cadena[i]
#         lista_separada.append(cadena_nueva)
    
#     return lista_separada

# def unir_cadena(lista:list,separador:str) -> str:
#     if type(lista) != list or type(separador) != str:
#         return ""
    
#     cadena_nueva = ""
#     for i in range(len(lista)):
#         if i == len(lista) - 1:
#             cadena_nueva += f"{str(lista[i])}"
#         else:
#             cadena_nueva += f"{str(lista[i])}{separador}"
        
#     return cadena_nueva