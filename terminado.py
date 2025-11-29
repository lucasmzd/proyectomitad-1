import pygame
from constantes import *
from funciones import *

pygame.init()

def mostrar_game_over(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    datos_juego["bandera_texto"] = not datos_juego["bandera_texto"]
    ventana = "terminado"
    cuadro_texto = crear_elemento_juego("texturas/textura_respuesta.jpg",300,50,150,275)
    for evento in cola_eventos:
        if evento.type == pygame.TEXTINPUT:
            datos_juego["nombre"] += evento.text
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                datos_juego["nombre"] = datos_juego["nombre"][0:-1]
    pantalla.fill(COLOR_BLANCO)
    mostrar_texto(pantalla,f"PERDISTE EL JUEGO: {datos_juego.get("puntuacion")}",(200,50),FUENTE_ARIAL_50,COLOR_NEGRO)
    if len(datos_juego.get("nombre","")) > 0:
        if datos_juego["bandera_texto"]:
            mostrar_texto(cuadro_texto["superficie"],f"{datos_juego.get("nombre","")}|",(10,10),FUENTE_ARIAL_30,COLOR_BLANCO)
        else: mostrar_texto(cuadro_texto["superficie"],f"{datos_juego.get("nombre","")}",(10,10),FUENTE_ARIAL_30,COLOR_BLANCO)
    else: mostrar_texto(cuadro_texto["superficie"],f"Ingrese su nombre",(10,10),FUENTE_ARIAL_25,"#6F6B6B")
    pantalla.blit(cuadro_texto["superficie"],cuadro_texto["rectangulo"])
    return ventana