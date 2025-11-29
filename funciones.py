import random
import os
import time
from constantes import *
import datetime
import pygame

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def crear_datos_juego() -> dict:
    datos_juego = {
        "nombre": "",
        "tiempo_pregunta": TIEMPO_TOTAL,
        "puntos_por_respuesta": PUNTUACION_ACIERTO,
        "puntos_error": PUNTUACION_ERROR,
        "tiempo_restante": TIEMPO_TOTAL,
        "puntuacion": 0,
        "cantidad_vidas": CANTIDAD_VIDAS,
        "indice": 0,
        "volumen_musica": 100,
        "bandera_texto": False
    }
    return datos_juego

def obtener_pregunta_actual(datos_juego:dict,lista_preguntas:list) -> dict | None:
    if type(datos_juego) == dict and type(lista_preguntas) == list and len(lista_preguntas) > 0 and datos_juego.get("indice") != None:
        indice = datos_juego.get("indice")
        pregunta = lista_preguntas[indice]
    else:
        pregunta = None 
    return pregunta    

def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False
    return retorno

def modificar_puntuacion(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += incremento
    else:
        retorno = False
    return retorno

def verificar_respuesta(pregunta_actual:dict,datos_juego:dict,respuesta:int):
    """
    Usa los valores almacenados en datos_juego para sumar/restar puntos y vidas.
    - puntos_por_respuesta: positivo al acertar
    - puntos_error: negativo al fallar (se resta)
    """
    if type(pregunta_actual) == dict and pregunta_actual.get("respuesta_correcta") != None:
        retorno = True
        puntos_acierto = datos_juego.get("puntos_por_respuesta", PUNTUACION_ACIERTO)
        puntos_error = datos_juego.get("puntos_error", PUNTUACION_ERROR)
        if respuesta == pregunta_actual.get("respuesta_correcta"):
            modificar_puntuacion(datos_juego, puntos_acierto)
        else:
            modificar_puntuacion(datos_juego, -abs(puntos_error))
            modificar_vida(datos_juego, -1)
    else:
        retorno = False
    return retorno

def pasar_pregunta(datos_juego:dict,lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("indice") != None:
        retorno = True
        datos_juego["indice"] += 1
        verificar_indice(datos_juego,lista_preguntas)
    else:
        retorno = False 
    return retorno

def verificar_indice(datos_juego:dict,lista_preguntas:list) -> None:
    if datos_juego["indice"] == len(lista_preguntas):
        datos_juego["indice"] = 0
        mezclar_lista(lista_preguntas)
        
def mezclar_lista(lista_preguntas:dict) -> bool:
    if type(lista_preguntas) == list and len(lista_preguntas):
        retorno = True
        random.shuffle(lista_preguntas)
    else:
        retorno = False
    return retorno

def reiniciar_estadisticas(datos_juego:dict) -> bool:
    """
    Reinicia las estadísticas antes de una partida.
    Ahora toma tiempo_restante y cantidad_vidas desde datos_juego (configuración)
    """
    if type(datos_juego) == dict:
        retorno = True
        tiempo_cfg = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
        vidas_cfg = datos_juego.get("cantidad_vidas", CANTIDAD_VIDAS)
        datos_juego.update({
            "tiempo_restante": tiempo_cfg,
            "puntuacion": 0,
            "cantidad_vidas": vidas_cfg,
            "indice": 0
        })
    else:
        retorno = False
    return retorno

# def terminar_juego(datos_juego:dict) -> bool:
#     if type(datos_juego) == dict:
#         print("GAME OVER\n")
#         datos_juego["nombre"] = input("Ingrese su nombre: ")     
#         mostrar_resultados(datos_juego)
#         reiniciar_estadisticas(datos_juego)
#         retorno = True
#     else:
#         retorno = False
#     return retorno
        
# def mostrar_resultados(datos_juego:dict) -> bool:
#     if type(datos_juego) == dict:
#         retorno = True
#         print(f"PARTIDA FINALIZADA EL DIA: {datetime.datetime.now()}")
#         print(f"NOMBRE: {datos_juego.get('nombre','No encontrado')}")
#         print(f"PUNTUACION TOTAL: {datos_juego.get('puntuacion','No encontrado')} PUNTOS")
#     else:
#         retorno = False
#     return retorno

# def actualizar_tiempo(tiempo_inicio:float,tiempo_actual:float,datos_juego:dict) -> bool:
#     """
#     Actualiza tiempo_restante usando la configuración 'tiempo_pregunta' dentro de datos_juego.
#     """
#     if type(datos_juego) == dict:
#         retorno = True
#         tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)
#         tiempo_cfg = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
#         datos_juego["tiempo_restante"] = max(0, tiempo_cfg - tiempo_transcurrido)
#     else:
#         retorno = False
#     return retorno

# FUNCIONES PYGAME
def crear_elemento_juego(textura:str,ancho_elemento:int,alto_elemento:int,x:int,y:int) -> dict | None:
    if os.path.exists(textura):
        elemento_juego = {}
        elemento_juego["superficie"] = pygame.image.load(textura)
        elemento_juego["superficie"] = pygame.transform.scale(elemento_juego["superficie"],(ancho_elemento,alto_elemento))
        elemento_juego["rectangulo"] = pygame.rect.Rect(x,y,ancho_elemento,alto_elemento)
    else:
        elemento_juego = None
    return elemento_juego

def crear_lista_respuestas(textura:str,x:int,y:int,cantidad_respuestas:int) -> list:
    lista_respuestas = []
    for i in range(cantidad_respuestas):
        cuadro_respuesta = crear_elemento_juego(textura,ANCHO_RESPUESTA,ALTO_RESPUESTA,x,y)
        lista_respuestas.append(cuadro_respuesta)
        y += 70
    return lista_respuestas

def mostrar_datos_juego_pygame(pantalla:pygame.Surface,datos_juego:dict):
    mostrar_texto(pantalla,f"Tiempo restante: {datos_juego.get('tiempo_restante')} s",(10,10),FUENTE_ARIAL_20)
    mostrar_texto(pantalla,f"Puntuacion: {datos_juego.get('puntuacion')}",(10,35),FUENTE_ARIAL_20)
    mostrar_texto(pantalla,f"Vidas: {datos_juego.get('cantidad_vidas')}",(10,60),FUENTE_ARIAL_20)
    
def responder_pregunta_pygame(lista_respuestas:list,pos_click:tuple,sonido:pygame.mixer.Sound,datos_juego:dict,lista_preguntas:list,pregunta_actual:dict) -> bool:
    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_click):
            sonido.play()
            respuesta = i + 1
            verificar_respuesta(pregunta_actual,datos_juego,respuesta)
            pasar_pregunta(datos_juego,lista_preguntas)
            
def mostrar_pregunta_pygame(pregunta_actual:dict,pantalla:pygame.Surface,cuadro_pregunta:dict,lista_respuestas:list) -> bool:
    if type(pregunta_actual) == dict:
        retorno = True
        mostrar_texto(cuadro_pregunta["superficie"],pregunta_actual.get("descripcion"),(10,10),FUENTE_ARIAL_30)
        pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])
        mostrar_texto(lista_respuestas[0]["superficie"],pregunta_actual.get("respuesta_1"),(20,20),FUENTE_ARIAL_20,COLOR_BLANCO)
        mostrar_texto(lista_respuestas[1]["superficie"],pregunta_actual.get("respuesta_2"),(20,20),FUENTE_ARIAL_20,COLOR_BLANCO)
        mostrar_texto(lista_respuestas[2]["superficie"],pregunta_actual.get("respuesta_3"),(20,20),FUENTE_ARIAL_20,COLOR_BLANCO)    
        for i in range(len(lista_respuestas)):
            pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"]) 
    else:
        retorno = False
    return retorno

def crear_lista_botones(textura:str,x:int,y:int,cantidad_botones:int) -> list:
    lista_botones = []
    for i in range(cantidad_botones):
        boton = crear_elemento_juego(textura,ANCHO_BOTON,ALTO_BOTON,x,y)
        lista_botones.append(boton)
        y += 85
    return lista_botones

def cambiar_musica_fondo(musica:str,datos_juego:dict) -> bool:
    if os.path.exists(musica):
        retorno = True
        pygame.mixer.init()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musica)
        volumen = datos_juego.get("volumen_musica",0)            
        pygame.mixer.music.set_volume(volumen / 100)
        pygame.mixer.music.play(-1)
    else:
        retorno = False
    return retorno

def establecer_dificultad(datos_juego: dict, dificultad: str) -> None:
    if type(datos_juego) != dict or type(dificultad) != str:
        return None
    d = dificultad.lower()
    if d == "facil":
        datos_juego["tiempo_pregunta"] = 30
        datos_juego["puntos_por_respuesta"] = 50
        datos_juego["cantidad_vidas"] = 5
        datos_juego["puntos_error"] = 10
    elif d == "normal":
        datos_juego["tiempo_pregunta"] = 20
        datos_juego["puntos_por_respuesta"] = 25
        datos_juego["cantidad_vidas"] = 3
        datos_juego["puntos_error"] = 15
    elif d == "dificil":
        datos_juego["tiempo_pregunta"] = 10
        datos_juego["puntos_por_respuesta"] = 10
        datos_juego["cantidad_vidas"] = 1
        datos_juego["puntos_error"] = 20
    datos_juego["tiempo_restante"] = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
    return None