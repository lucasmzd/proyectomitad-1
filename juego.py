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
}

def mostrar_juego(pantalla: pygame.Surface, cola_eventos, datos_juego, categoria_elegida) -> str:
    ventana = "juego"
    cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
    lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 3)
    pregunta_actual = obtener_pregunta_actual(datos_juego, lista_preguntas)
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            responder_pregunta_pygame(lista_respuestas, evento.pos, SONIDO_CLICK, datos_juego, lista_preguntas, pregunta_actual)
            pregunta_actual = obtener_pregunta_actual(datos_juego, lista_preguntas)
            cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
            lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 3)
    if datos_juego.get("cantidad_vidas") == 0:
        return "terminado"
    fondo_actual = fondos[categoria_elegida]
    pantalla.blit(fondo_actual, (0, 0))
    mostrar_datos_juego_pygame(pantalla, datos_juego)
    mostrar_pregunta_pygame(pregunta_actual, pantalla, cuadro_pregunta, lista_respuestas)
    return ventana