import pygame
from constantes import *
from funciones import *
from personalizada import *

pygame.init()

boton_suma = crear_elemento_juego("texturas/mas.webp",60,60,420,200)
boton_resta = crear_elemento_juego("texturas/menos.webp",60,60,20,200)
boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)
boton_personalizada = crear_elemento_juego("texturas/textura_respuesta.jpg",300,60,150,300)

# Botones de audio ON/OFF (mute/unmute)
boton_audio_on = crear_elemento_juego("texturas/mas.webp",60,60,350,400)
boton_audio_off = crear_elemento_juego("texturas/menos.webp",60,60,150,400)

def administrar_botones(boton_suma:dict,boton_resta:dict,boton_volver:dict,boton_personalizada:dict,boton_audio_on:dict,boton_audio_off:dict,datos_juego:dict,pos_mouse:tuple) -> str:
    ventana = "ajustes"
    vol_musica = datos_juego.get("volumen_musica",0)
    
    if boton_suma and boton_suma["rectangulo"].collidepoint(pos_mouse):
        if vol_musica <= 95:
            datos_juego["volumen_musica"] += 5
            if datos_juego.get("estado_musica", "activo") == "activo":
                pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
            SONIDO_CLICK.play()
        else:
            SONIDO_ERROR.play()
    
    elif boton_resta and boton_resta["rectangulo"].collidepoint(pos_mouse):
        if vol_musica > 0:
            datos_juego["volumen_musica"] -= 5
            if datos_juego.get("estado_musica", "activo") == "activo":
                pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
            SONIDO_CLICK.play()
        else:
            SONIDO_ERROR.play()
    
    elif boton_audio_on and boton_audio_on["rectangulo"].collidepoint(pos_mouse):
        # Unmute - Activar música
        if datos_juego.get("estado_musica", "inactivo") != "activo":
            SONIDO_CLICK.play()
            pygame.mixer.music.unpause()
            datos_juego["estado_musica"] = "activo"
            pygame.mixer.music.set_volume(datos_juego.get("volumen_musica", 100) / 100)
    
    elif boton_audio_off and boton_audio_off["rectangulo"].collidepoint(pos_mouse):
        # Mute - Silenciar música
        if datos_juego.get("estado_musica", "activo") != "inactivo":
            SONIDO_CLICK.play()
            pygame.mixer.music.pause()
            datos_juego["estado_musica"] = "inactivo"
    
    elif boton_personalizada and boton_personalizada["rectangulo"].collidepoint(pos_mouse):
        SONIDO_CLICK.play()
        ventana = "personalizada"
    
    elif boton_volver and boton_volver["rectangulo"].collidepoint(pos_mouse):
        SONIDO_CLICK.play()
        ventana = "menu"
    
    return ventana

def dibujar_elementos(pantalla:pygame.Surface,boton_suma:dict,boton_resta:dict,boton_volver:dict,boton_personalizada:dict,boton_audio_on:dict,boton_audio_off:dict,datos_juego:dict) -> None:
    pantalla.fill(COLOR_BLANCO)
    
    # Botones de volumen originales
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    mostrar_texto(pantalla,f"{datos_juego.get('volumen_musica',0)} %",(200,200),FUENTE_ARIAL_50,COLOR_NEGRO)
    
    # Botones de mute/unmute
    pantalla.blit(boton_audio_on["superficie"], boton_audio_on["rectangulo"])
    pantalla.blit(boton_audio_off["superficie"], boton_audio_off["rectangulo"])
    
    # Textos debajo de los botones
    mostrar_texto(pantalla, "UNMUTE", (340, 470), FUENTE_ARIAL_20, COLOR_NEGRO)
    mostrar_texto(pantalla, "MUTE", (155, 470), FUENTE_ARIAL_20, COLOR_NEGRO)
    
    # Indicador visual del estado (opcional)
    estado_musica = datos_juego.get("estado_musica", "activo")
    color_indicador = COLOR_VERDE if estado_musica == "activo" else COLOR_ROJO
    pygame.draw.circle(pantalla, color_indicador, (300, 430), 10)
    
    # Botón volver
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)
    
    # Botón dificultad personalizada
    if boton_personalizada:
        pantalla.blit(boton_personalizada["superficie"], boton_personalizada["rectangulo"])
        mostrar_texto(boton_personalizada["superficie"], "DIFICULTAD PERSONALIZADA", (10,15), FUENTE_ARIAL_25, COLOR_BLANCO)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    ventana = "ajustes"
    
    # Inicializar estado de música si no existe
    if "estado_musica" not in datos_juego:
        datos_juego["estado_musica"] = "activo"
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            ventana = administrar_botones(boton_suma,boton_resta,boton_volver,boton_personalizada,boton_audio_on,boton_audio_off,datos_juego,evento.pos)
    
    dibujar_elementos(pantalla,boton_suma,boton_resta,boton_volver,boton_personalizada,boton_audio_on,boton_audio_off,datos_juego)
    
    return ventana