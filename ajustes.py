import pygame
from constantes import *
from funciones import *

pygame.init()

boton_suma = crear_elemento_juego("texturas/mas.webp",60,60,420,200)
boton_resta = crear_elemento_juego("texturas/menos.webp",60,60,20,200)
boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)

def administrar_botones(boton_suma:dict,boton_resta:dict,boton_volver:dict,datos_juego:dict,pos_mouse:tuple) -> str:
    ventana = "ajustes"
    vol_musica = datos_juego.get("volumen_musica",0)
    if boton_suma["rectangulo"].collidepoint(pos_mouse):
        if vol_musica <= 95:
            datos_juego["volumen_musica"] += 5
            SONIDO_CLICK.play()
        else: SONIDO_ERROR.play()
    elif boton_resta["rectangulo"].collidepoint(pos_mouse):
        if vol_musica > 0:
            datos_juego["volumen_musica"] -= 5
            SONIDO_CLICK.play()
        else: SONIDO_ERROR.play()
    elif boton_volver["rectangulo"].collidepoint(pos_mouse):
        SONIDO_CLICK.play()
        ventana = "menu"
    return ventana

def dibujar_elementos(pantalla:pygame.Surface,boton_suma:dict,boton_resta:dict,boton_volver:dict,datos_juego:dict) -> None:
    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,f"{datos_juego.get("volumen_musica",0)} %",(200,200),FUENTE_ARIAL_50,COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    ventana = "ajustes"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            ventana = administrar_botones(boton_suma,boton_resta,boton_volver,datos_juego,evento.pos)
    dibujar_elementos(pantalla,boton_suma,boton_resta,boton_volver,datos_juego)
    return ventana