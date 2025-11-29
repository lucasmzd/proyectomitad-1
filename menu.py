import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_menu = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"),PANTALLA)
lista_botones = crear_lista_botones("texturas/textura_respuesta.jpg",150,125,5)
lista_texto_botones = ["JUGAR","DIFICULTAD","RANKING","AJUSTES","SALIR"]

def mostrar_menu(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event]) -> str:
    ventana = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    return lista_texto_botones[i].lower()
    pantalla.blit(fondo_menu,(0,0))
    for i in range(len(lista_botones)):
        mostrar_texto(lista_botones[i]["superficie"], lista_texto_botones[i],
                      (90,10), FUENTE_ARIAL_30_NEGRITA, COLOR_BLANCO)
        pantalla.blit(lista_botones[i]["superficie"], lista_botones[i]["rectangulo"])
    return ventana