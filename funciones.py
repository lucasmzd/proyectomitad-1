import random
import os
import time
from constantes import *
import datetime
import json
import pygame

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in str(text).splitlines()]
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
        "bandera_texto": False,
        "racha": 0,
    }
    return datos_juego

def obtener_pregunta_actual(datos_juego:dict, lista_preguntas:list) -> dict | None:
    if type(datos_juego) == dict and type(lista_preguntas) == list and len(lista_preguntas) > 0 and datos_juego.get("indice") != None:
        indice = datos_juego.get("indice")
        if 0 <= indice < len(lista_preguntas):
            return lista_preguntas[indice]
    return None

def modificar_vida(datos_juego:dict, incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        datos_juego["cantidad_vidas"] += incremento
        return True
    return False

def modificar_puntuacion(datos_juego:dict, incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        datos_juego["puntuacion"] += incremento
        return True
    return False

def verificar_respuesta(pregunta_actual:dict, datos_juego:dict, respuesta:int):
    if not isinstance(pregunta_actual, dict):
        return None
    correcta = pregunta_actual.get("respuesta_correcta")
    if correcta is None:
        return None
    puntos_acierto = datos_juego.get("puntos_por_respuesta", PUNTUACION_ACIERTO)
    puntos_error = datos_juego.get("puntos_error", PUNTUACION_ERROR)
    if respuesta == correcta:
        modificar_puntuacion(datos_juego, puntos_acierto)
        datos_juego["racha"] += 1
        datos_juego["racha"] = sumar_bonus(datos_juego, datos_juego["racha"])
        return True
    else:
        modificar_puntuacion(datos_juego, -abs(puntos_error))
        modificar_vida(datos_juego, -1)
        datos_juego["racha"] = 0
        return False

def pasar_pregunta(datos_juego:dict, lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("indice") != None:
        datos_juego["indice"] += 1
        verificar_indice(datos_juego, lista_preguntas)
        return True
    return False

def verificar_indice(datos_juego:dict, lista_preguntas:list) -> None:
    if len(lista_preguntas) == 0:
        datos_juego["indice"] = 0
        return
    if datos_juego["indice"] >= len(lista_preguntas):
        datos_juego["indice"] = 0
        mezclar_lista(lista_preguntas)

def mezclar_lista(lista_preguntas:list) -> bool:
    if type(lista_preguntas) == list and len(lista_preguntas):
        random.shuffle(lista_preguntas)
        return True
    return False

def reiniciar_estadisticas(datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        tiempo_cfg = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
        vidas_cfg = datos_juego.get("cantidad_vidas", CANTIDAD_VIDAS)
        datos_juego.update({
            "tiempo_restante": tiempo_cfg,
            "puntuacion": 0,
            "cantidad_vidas": vidas_cfg,
            "indice": 0,
            "racha": 0
        })
        if "inicio_pregunta" in datos_juego:
            del datos_juego["inicio_pregunta"]
        if "comodines" in datos_juego:
            del datos_juego["comodines"]
        if "preguntas_filtradas" in datos_juego:
            del datos_juego["preguntas_filtradas"]
        return True
    return False

def crear_elemento_juego(textura:str, ancho_elemento:int, alto_elemento:int, x:int, y:int) -> dict | None:
    if os.path.exists(textura):
        elemento_juego = {}
        elemento_juego["superficie"] = pygame.image.load(textura)
        elemento_juego["superficie"] = pygame.transform.scale(elemento_juego["superficie"], (ancho_elemento, alto_elemento))
        elemento_juego["rectangulo"] = pygame.rect.Rect(x, y, ancho_elemento, alto_elemento)
        return elemento_juego
    return None

def crear_lista_respuestas(textura:str, x:int, y:int, cantidad_respuestas:int) -> list:
    lista_respuestas = []
    for i in range(cantidad_respuestas):
        cuadro_respuesta = crear_elemento_juego(textura, ANCHO_RESPUESTA, ALTO_RESPUESTA, x, y)
        if cuadro_respuesta is not None:
            cuadro_respuesta["texto"] = f"resp_{i+1}"
        lista_respuestas.append(cuadro_respuesta)
        y += ALTO_RESPUESTA + 10
    return lista_respuestas

def mostrar_datos_juego_pygame(pantalla:pygame.Surface, datos_juego:dict):
    mostrar_texto(pantalla, f"Tiempo restante: {datos_juego.get('tiempo_restante')} s", (10,10), FUENTE_ARIAL_20)
    mostrar_texto(pantalla, f"Puntuacion: {datos_juego.get('puntuacion')}", (10,35), FUENTE_ARIAL_20)
    mostrar_texto(pantalla, f"Vidas: {datos_juego.get('cantidad_vidas')}", (10,60), FUENTE_ARIAL_20)

def responder_pregunta_pygame(lista_respuestas, posicion_click, sonido_click, datos_juego, lista_preguntas, pregunta_actual):
    if lista_respuestas is None or pregunta_actual is None:
        return False

    for i, respuesta in enumerate(lista_respuestas):
        if respuesta and respuesta["rectangulo"].collidepoint(posicion_click):
            sonido_click.play()
            indice_respuesta = i + 1
            verificar_respuesta(pregunta_actual, datos_juego, indice_respuesta)
            pasar_pregunta(datos_juego, lista_preguntas)
            datos_juego["inicio_pregunta"] = pygame.time.get_ticks()
            datos_juego["tiempo_restante"] = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
            return True
    return False

def mostrar_pregunta_pygame(pregunta_actual:dict, pantalla:pygame.Surface, cuadro_pregunta:dict, lista_respuestas:list) -> bool:
    if not isinstance(pregunta_actual, dict):
        return False
    mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual.get("descripcion"), (10,10), FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"], cuadro_pregunta["rectangulo"])
    respuestas_keys = ["respuesta_1", "respuesta_2", "respuesta_3", "respuesta_4"]

    COLOR_GRIS_OSCURO = (100, 100, 100)
    for i in range(4):
        if lista_respuestas[i]:
            # No limpiar si está eliminada por la bomba
            if not lista_respuestas[i].get("eliminada", False):
                lista_respuestas[i]["superficie"].fill((0,0,0,0))
            
            # Color del texto: gris si está eliminada, blanco si no
            color_texto = COLOR_GRIS_OSCURO if lista_respuestas[i].get("eliminada", False) else COLOR_BLANCO
            
            mostrar_texto(
                lista_respuestas[i]["superficie"],
                pregunta_actual.get(respuestas_keys[i], ""),
                (20,20),
                FUENTE_ARIAL_20,
                color_texto
            )
            pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])
    return True

def crear_lista_botones(textura:str, x:int, y:int, cantidad_botones:int) -> list:
    lista_botones = []
    for i in range(cantidad_botones):
        boton = crear_elemento_juego(textura, ANCHO_BOTON, ALTO_BOTON, x, y)
        lista_botones.append(boton)
        y += ALTO_BOTON + 15
    return lista_botones

def cambiar_musica_fondo(musica:str, datos_juego:dict) -> bool:
    if os.path.exists(musica):
        pygame.mixer.init()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musica)
        volumen = datos_juego.get("volumen_musica", 0)
        pygame.mixer.music.set_volume(volumen / 100)
        pygame.mixer.music.play(-1)
        return True
    return False

def establecer_dificultad(datos_juego: dict, dificultad: str) -> None:
    if type(datos_juego) != dict or type(dificultad) != str:
        return None
    if dificultad == "facil":
        datos_juego["tiempo_pregunta"] = 30
        datos_juego["puntos_por_respuesta"] = 50
        datos_juego["cantidad_vidas"] = 5
        datos_juego["puntos_error"] = 10
    elif dificultad == "normal":
        datos_juego["tiempo_pregunta"] = 20
        datos_juego["puntos_por_respuesta"] = 25
        datos_juego["cantidad_vidas"] = 3
        datos_juego["puntos_error"] = 15
    elif dificultad == "dificil":
        datos_juego["tiempo_pregunta"] = 10
        datos_juego["puntos_por_respuesta"] = 10
        datos_juego["cantidad_vidas"] = 1
        datos_juego["puntos_error"] = 20
    datos_juego["tiempo_restante"] = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
    return None

def sumar_bonus(datos_juego: dict, contador_correctas: int) -> int:
    if contador_correctas >= 5:
        datos_juego["cantidad_vidas"] += 1
        return 0
    return contador_correctas

def generar_json(nombre_archivo: str, lista: list) -> bool:
    if type(lista) == list and len(lista) > 0:
        retorno = True
        with open(nombre_archivo,"w",encoding="utf-8") as archivo:
            json.dump(lista,archivo,indent=4)
        del archivo
    else:
        retorno = False

    return retorno

def leer_json(nombre_archivo: str) -> any:
    if type(nombre_archivo) == str and os.path.exists(nombre_archivo):
        with open(nombre_archivo,"r",encoding="utf-8") as archivo:
            retorno = json.load(archivo)
        del archivo
    else:
        retorno = False

    return retorno

def guardar_partida(nombre: str, puntuacion: int, archivo: str = "puntajes.json"):
    lista_partidas = leer_json(archivo)

    if lista_partidas == False:
        lista_partidas = []

    lista_partidas.append({
        "nombre": nombre,
        "puntuacion": puntuacion,
        "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
    })

    generar_json(archivo, lista_partidas)

def obtener_top_10(archivo: str = "puntajes.json",) -> list:
    lista_partidas = leer_json(archivo)

    if lista_partidas == False:
        return []

    top_10 = []
    lista_partidas = lista_partidas.copy()

    for i in range(10):
        if len(lista_partidas) == 0:
            break

        max_puntuacion = -1 
        indice_mejor = -1
        for j in range(len(lista_partidas)):
            partida_actual = lista_partidas[j]
            puntuacion_actual = partida_actual.get("puntuacion", 0)

            if puntuacion_actual > max_puntuacion:
                max_puntuacion = puntuacion_actual
                indice_mejor = j

        if indice_mejor != -1:
            mejor_partida = lista_partidas[indice_mejor]
            top_10.append(mejor_partida)
            del lista_partidas[indice_mejor]
    return top_10