import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_dificultad = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"), PANTALLA)
lista_botones_dificultad = crear_lista_botones("texturas/textura_respuesta.jpg", 150, 125, 3)
lista_texto_dificultad = ["FACIL", "NORMAL", "DIFICIL"]

def mostrar_dificultad(pantalla: pygame.Surface, cola_eventos, datos_juego: dict) -> str:
    ventana = "dificultad"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones_dificultad)):
                if lista_botones_dificultad[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    datos_juego["dificultad_actual"] = lista_texto_dificultad[i].lower()
                    return lista_texto_dificultad[i].lower()
    pantalla.blit(fondo_dificultad, (0, 0))
    for i in range(len(lista_botones_dificultad)):
        mostrar_texto(
            lista_botones_dificultad[i]["superficie"],
            lista_texto_dificultad[i],
            (90, 10),
            FUENTE_ARIAL_30_NEGRITA,
            COLOR_BLANCO
        )
        pantalla.blit(lista_botones_dificultad[i]["superficie"], lista_botones_dificultad[i]["rectangulo"])
    return ventana