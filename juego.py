import pygame
from constantes import *
from preguntas import *
from funciones import *

pygame.init()

fondos = {
    "geografia": pygame.transform.scale(pygame.image.load("texturas/geografia.png"), PANTALLA),
    "entretenimiento": pygame.transform.scale(pygame.image.load("texturas/entretenimiento.png"), PANTALLA),
    "deporte": pygame.transform.scale(pygame.image.load("texturas/deporte.png"), PANTALLA),
    "ciencia": pygame.transform.scale(pygame.image.load("texturas/ciencia.png"), PANTALLA),
    "historia": pygame.transform.scale(pygame.image.load("texturas/historia.png"), PANTALLA),
    "arte": pygame.transform.scale(pygame.image.load("texturas/historia.png"), PANTALLA)
}

def iniciar_tiempo_pregunta(datos_juego):
    datos_juego["tiempo_restante"] = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
    datos_juego["inicio_pregunta"] = pygame.time.get_ticks()

def actualizar_tiempo(datos_juego):
    if "inicio_pregunta" not in datos_juego:
        iniciar_tiempo_pregunta(datos_juego)
        return
    ahora = pygame.time.get_ticks()
    transcurrido = (ahora - datos_juego["inicio_pregunta"]) // 1000
    tiempo_cfg = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
    datos_juego["tiempo_restante"] = max(0, tiempo_cfg - transcurrido)
    if datos_juego["tiempo_restante"] <= 0:
        datos_juego["cantidad_vidas"] -= 1
        pasar_pregunta(datos_juego, lista_preguntas)
        iniciar_tiempo_pregunta(datos_juego)

def mostrar_juego(pantalla: pygame.Surface, cola_eventos, datos_juego, categoria_elegida):
    ventana = "juego"
    cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
    lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 4)
    pregunta_actual = obtener_pregunta_actual(datos_juego, lista_preguntas)
    if "inicio_pregunta" not in datos_juego:
        iniciar_tiempo_pregunta(datos_juego)
    actualizar_tiempo(datos_juego)
    # EVENTOS
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            procesado = responder_pregunta_pygame(
                lista_respuestas,
                evento.pos,
                SONIDO_CLICK,
                datos_juego,
                lista_preguntas,
                pregunta_actual
            )

            if procesado:
                pregunta_actual = obtener_pregunta_actual(datos_juego, lista_preguntas)
                cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
                lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 4)
    if datos_juego.get("cantidad_vidas", 0) <= 0:
        ventana = "terminado"
    fondo_actual = fondos.get(categoria_elegida, pygame.Surface(PANTALLA))
    if isinstance(fondo_actual, pygame.Surface) and fondo_actual.get_size() != PANTALLA:
        fondo_actual = pygame.transform.scale(fondo_actual, PANTALLA)
    pantalla.blit(fondo_actual, (0, 0))
    mostrar_datos_juego_pygame(pantalla, datos_juego)
    mostrar_pregunta_pygame(pregunta_actual, pantalla, cuadro_pregunta, lista_respuestas)
    return ventana