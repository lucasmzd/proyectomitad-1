import pygame
from constantes import *
from funciones import *

pygame.init()

def nombre_valido(nombre: str) -> bool:
    if not (3 <= len(nombre) <= 15):
        return False
    for char in nombre:
        if not (
            ('a' <= char <= 'z') or
            ('A' <= char <= 'Z') or
            ('0' <= char <= '9')
        ):
            return False
    return True

def mostrar_game_over(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    ventana = "terminado"
    datos_juego["bandera_texto"] = not datos_juego.get("bandera_texto", False)
    cuadro_texto = crear_elemento_juego("texturas/textura_respuesta.jpg", 300, 50, 150, 275)
    for evento in cola_eventos:
        if evento.type == pygame.TEXTINPUT:
            texto = evento.text
            if len(texto) == 1 and (
                ('a' <= texto <= 'z') or
                ('A' <= texto <= 'Z') or
                ('0' <= texto <= '9')
            ):
                if len(datos_juego.get("nombre", "")) < 15:
                    datos_juego["nombre"] += texto
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                nombre = datos_juego.get("nombre", "").strip()

                if nombre_valido(nombre):
                    guardar_partida(nombre, datos_juego.get("puntuacion", 0))
                    ventana = "menu"
                else:
                    datos_juego["error_nombre"] = "Solo letras y números (3 a 15 caracteres)"
            elif evento.key == pygame.K_BACKSPACE:
                datos_juego["nombre"] = datos_juego.get("nombre", "")[:-1]
    pantalla.fill(COLOR_BLANCO)
    mostrar_texto(
        pantalla,
        f"PERDISTE EL JUEGO: {datos_juego.get('puntuacion', 0)}",
        (200, 50),
        FUENTE_ARIAL_50,
        COLOR_NEGRO
    )
    texto_ingreso = datos_juego.get("nombre", "")
    if len(texto_ingreso) == 0:
        mostrar_texto(cuadro_texto["superficie"], "Ingrese su nombre", (10, 10), FUENTE_ARIAL_25, "#6F6B6B")
    else:
        if datos_juego.get("bandera_texto", False):
            mostrar_texto(cuadro_texto["superficie"], f"{texto_ingreso}|", (10, 10), FUENTE_ARIAL_30, COLOR_BLANCO)
        else:
            mostrar_texto(cuadro_texto["superficie"], texto_ingreso, (10, 10), FUENTE_ARIAL_30, COLOR_BLANCO)
    pantalla.blit(cuadro_texto["superficie"], cuadro_texto["rectangulo"])
    if datos_juego.get("error_nombre"):
        mostrar_texto(
            pantalla,
            datos_juego["error_nombre"],
            (150, 340),
            FUENTE_ARIAL_25,
            (200, 0, 0)
        )
    return ventana