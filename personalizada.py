import pygame
from constantes import *
from funciones import *

pygame.init()

btn_correcta_suma = crear_elemento_juego("texturas/mas.webp",60,60, 420,100)
btn_correcta_resta = crear_elemento_juego("texturas/menos.webp",60,60, 20,100)
btn_incorrecta_suma = crear_elemento_juego("texturas/mas.webp",60,60, 420,200)
btn_incorrecta_resta = crear_elemento_juego("texturas/menos.webp",60,60, 20,200)
btn_vidas_suma = crear_elemento_juego("texturas/mas.webp",60,60, 420,300)
btn_vidas_resta = crear_elemento_juego("texturas/menos.webp",60,60, 20,300)
btn_tiempo_suma = crear_elemento_juego("texturas/mas.webp",60,60, 420,400)
btn_tiempo_resta = crear_elemento_juego("texturas/menos.webp",60,60, 20,400)
boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)

def administrar_botones(pos_mouse:tuple, datos_juego:dict) -> str:
    ventana = "personalizada"
    pts_ok = datos_juego.get("puntos_por_respuesta",100)
    pts_err = datos_juego.get("puntos_error",25)
    vidas = datos_juego.get("cantidad_vidas",3)
    tiempo = datos_juego.get("tiempo_pregunta",30)

    if btn_correcta_suma["rectangulo"].collidepoint(pos_mouse):
        datos_juego["puntos_por_respuesta"] = pts_ok + 10
        datos_juego["dificultad_actual"] = "custom"
        SONIDO_CLICK.play()
    elif btn_correcta_resta["rectangulo"].collidepoint(pos_mouse):
        if pts_ok > 10:
            datos_juego["puntos_por_respuesta"] = pts_ok - 10
            datos_juego["dificultad_actual"] = "custom"
            SONIDO_CLICK.play()
        else:
            SONIDO_ERROR.play()
    elif btn_incorrecta_suma["rectangulo"].collidepoint(pos_mouse):
        datos_juego["puntos_error"] = pts_err + 5
        datos_juego["dificultad_actual"] = "custom"
        SONIDO_CLICK.play()
    elif btn_incorrecta_resta["rectangulo"].collidepoint(pos_mouse):
        if pts_err > 5:
            datos_juego["puntos_error"] = pts_err - 5
            datos_juego["dificultad_actual"] = "custom"
            SONIDO_CLICK.play()
        else:
            SONIDO_ERROR.play()
    elif btn_vidas_suma["rectangulo"].collidepoint(pos_mouse):
        datos_juego["cantidad_vidas"] = vidas + 1
        datos_juego["dificultad_actual"] = "custom"
        SONIDO_CLICK.play()
    elif btn_vidas_resta["rectangulo"].collidepoint(pos_mouse):
        if vidas > 1:
            datos_juego["cantidad_vidas"] = vidas - 1
            datos_juego["dificultad_actual"] = "custom"
            SONIDO_CLICK.play()
        else:
            SONIDO_ERROR.play()
    elif btn_tiempo_suma["rectangulo"].collidepoint(pos_mouse):
        datos_juego["tiempo_pregunta"] = tiempo + 5
        datos_juego["dificultad_actual"] = "custom"
        SONIDO_CLICK.play()
    elif btn_tiempo_resta["rectangulo"].collidepoint(pos_mouse):
        if tiempo > 5:
            datos_juego["tiempo_pregunta"] = tiempo - 5
            datos_juego["dificultad_actual"] = "custom"
            SONIDO_CLICK.play()
        else:
            SONIDO_ERROR.play()
    elif boton_volver["rectangulo"].collidepoint(pos_mouse):
        SONIDO_CLICK.play()
        ventana = "ajustes"

    return ventana

def dibujar_elementos(pantalla:pygame.Surface, datos_juego:dict):
    pantalla.fill(COLOR_BLANCO)
    mostrar_texto(pantalla,"DIFICULTAD PERSONALIZADA",(120,20),FUENTE_ARIAL_20,COLOR_NEGRO)
    mostrar_texto(pantalla,"Puntos Correcta:",(120,110),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,str(datos_juego.get("puntos_por_respuesta",100)),(260,110),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,"Puntos Incorrecta:",(120,210),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,str(datos_juego.get("puntos_error",25)),(260,210),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,"Vidas:",(120,310),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,str(datos_juego.get("cantidad_vidas",3)),(260,310),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,"Tiempo (seg):",(120,410),FUENTE_ARIAL_30,COLOR_NEGRO)
    mostrar_texto(pantalla,str(datos_juego.get("tiempo_pregunta",30)),(260,410),FUENTE_ARIAL_30,COLOR_NEGRO)

    for boton in [
        btn_correcta_suma,btn_correcta_resta,
        btn_incorrecta_suma,btn_incorrecta_resta,
        btn_vidas_suma,btn_vidas_resta,
        btn_tiempo_suma,btn_tiempo_resta,
        boton_volver
    ]:
        pantalla.blit(boton["superficie"],boton["rectangulo"])
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)

def mostrar_dificultad_personalizada(pantalla:pygame.Surface, cola_eventos:list, datos_juego:dict) -> str:
    ventana = "personalizada"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            ventana = administrar_botones(evento.pos, datos_juego)
    dibujar_elementos(pantalla, datos_juego)
    return ventana