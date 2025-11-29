import pygame
from constantes import *
from funciones import *

pygame.init()

boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
    ventana = "rankings"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                ventana = "menu"
    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,f"RANKING",(150,200),FUENTE_ARIAL_50,COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)
    return ventana