import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_categoria = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"),PANTALLA)
lista_botones_categoria = crear_lista_botones("texturas/textura_respuesta.jpg", 150, 60, 6)
lista_texto_categoria = ["ENTRETENIMIENTO","DEPORTE","CIENCIA","HISTORIA", "GEOGRAFIA", "ARTE"]

def mostrar_categoria(pantalla: pygame.Surface, cola_eventos) -> str:
    ventana = "categoria"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones_categoria)):
                if lista_botones_categoria[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    return lista_texto_categoria[i].lower()  
    pantalla.blit(fondo_categoria, (0, 0))
    for i in range(len(lista_botones_categoria)):
        mostrar_texto(lista_botones_categoria[i]["superficie"], lista_texto_categoria[i], (90, 10), FUENTE_ARIAL_30_NEGRITA, COLOR_BLANCO)
        pantalla.blit(lista_botones_categoria[i]["superficie"], lista_botones_categoria[i]["rectangulo"])
    return ventana