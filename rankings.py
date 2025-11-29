import pygame
from constantes import *
from funciones import *

pygame.init()

boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg", 100, 40, 10, 10)

def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], lista_rankings=None) -> str:
    ventana = "rankings"
    if lista_rankings is None:
        lista_partidas = leer_json("puntajes.json")
        if lista_partidas == False:
            lista_partidas = []
        lista_rankings = lista_partidas
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver and boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                return "menu"
    pantalla.fill(COLOR_BLANCO)
    if boton_volver:
        boton_volver["superficie"].fill(COLOR_NEGRO)
        mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_ARIAL_20, COLOR_BLANCO)
        pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(pantalla, "TOP 10", (200, 50), FUENTE_ARIAL_50, COLOR_NEGRO)
    lista_rankings.sort(key=lambda x: x["puntuacion"], reverse=True)
    top_10 = lista_rankings[:10]
    y = 120
    for i, partida in enumerate(top_10):
        texto = f"{i+1}. {partida['nombre']} - {partida['puntuacion']} pts - {partida['fecha']}"
        mostrar_texto(pantalla, texto, (50, y), FUENTE_ARIAL_25, COLOR_NEGRO)
        y += 40
    return ventana