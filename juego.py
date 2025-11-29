import pygame
from constantes import *
from preguntas import *
from funciones import *

pygame.init()

fondos = {
    "geografia": pygame.transform.scale(pygame.image.load("texturas/geografia.png"), PANTALLA),
    "entretenimiento": pygame.transform.scale(pygame.image.load("texturas/entretenimiento.png"), PANTALLA),
    "deporte": pygame.transform.scale(pygame.image.load("texturas/deporte.png"), PANTALLA),
    "ciencia": pygame.transform.scale(pygame.image.load("texturas/ciencia.png"), PANTALLA),
    "historia": pygame.transform.scale(pygame.image.load("texturas/historia.png"), PANTALLA),
    "arte": pygame.transform.scale(pygame.image.load("texturas/historia.png"), PANTALLA)
}

# Botones de comodines (usando mas.webp temporalmente)
# Posicionados en la parte superior derecha para no interferir
boton_bomba = crear_elemento_juego("texturas/mas.webp", 50, 50, 450, 10)
boton_x2 = crear_elemento_juego("texturas/mas.webp", 50, 50, 510, 10)
boton_doble_chance = crear_elemento_juego("texturas/mas.webp", 50, 50, 450, 70)
boton_pasar = crear_elemento_juego("texturas/mas.webp", 50, 50, 510, 70)

def inicializar_comodines():
    """Inicializa el estado de los comodines para una nueva partida"""
    return {
        "bomba_disponible": True,
        "x2_disponible": True,
        "doble_chance_disponible": True,
        "pasar_disponible": True,
        "doble_chance_activa": False,
        "doble_chance_usada": False,
        "x2_activo": False,
        "comodin_activo": False
    }

def iniciar_tiempo_pregunta(datos_juego):
    datos_juego["tiempo_restante"] = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
    datos_juego["inicio_pregunta"] = pygame.time.get_ticks()

def actualizar_tiempo(datos_juego):
    if "inicio_pregunta" not in datos_juego:
        iniciar_tiempo_pregunta(datos_juego)
        return
    ahora = pygame.time.get_ticks()
    transcurrido = (ahora - datos_juego["inicio_pregunta"]) // 1000
    tiempo_cfg = datos_juego.get("tiempo_pregunta", TIEMPO_TOTAL)
    datos_juego["tiempo_restante"] = max(0, tiempo_cfg - transcurrido)
    if datos_juego["tiempo_restante"] <= 0:
        datos_juego["cantidad_vidas"] -= 1
        pasar_pregunta(datos_juego, datos_juego["preguntas_filtradas"])
        iniciar_tiempo_pregunta(datos_juego)

def activar_comodin_bomba(lista_respuestas, pregunta_actual, estado_comodines):
    """Elimina 2 respuestas incorrectas visualmente"""
    import random
    incorrectas = []
    for i in range(4):
        if (i + 1) != pregunta_actual["respuesta_correcta"]:
            incorrectas.append(i)
    
    # Elegir 2 respuestas incorrectas al azar
    eliminar = random.sample(incorrectas, 2)
    
    # Marcar visualmente las eliminadas (gris oscuro)
    COLOR_GRIS_OSCURO = (100, 100, 100)
    for idx in eliminar:
        if lista_respuestas[idx]:
            lista_respuestas[idx]["superficie"].fill(COLOR_GRIS_OSCURO)
            lista_respuestas[idx]["bloqueada"] = True
            lista_respuestas[idx]["eliminada"] = True  # Marcar como eliminada
    
    estado_comodines["bomba_disponible"] = False
    estado_comodines["comodin_activo"] = True
    SONIDO_CLICK.play()

def activar_comodin_x2(estado_comodines):
    """Activa el duplicador de puntos para la siguiente respuesta correcta"""
    estado_comodines["x2_disponible"] = False
    estado_comodines["x2_activo"] = True
    SONIDO_CLICK.play()

def activar_comodin_doble_chance(estado_comodines):
    """Activa la doble oportunidad"""
    estado_comodines["doble_chance_disponible"] = False
    estado_comodines["doble_chance_activa"] = True
    estado_comodines["comodin_activo"] = True
    SONIDO_CLICK.play()

def activar_comodin_pasar(datos_juego, cuadro_pregunta, lista_respuestas):
    """Pasa a la siguiente pregunta sin penalización"""
    estado_comodines["pasar_disponible"] = False
    pasar_pregunta(datos_juego, datos_juego["preguntas_filtradas"])
    iniciar_tiempo_pregunta(datos_juego)
    
    # Limpiar respuestas
    for respuesta in lista_respuestas:
        if respuesta:
            respuesta["superficie"] = pygame.image.load("texturas/textura_respuesta.jpg")
            respuesta["superficie"] = pygame.transform.scale(respuesta["superficie"], (ANCHO_RESPUESTA, ALTO_RESPUESTA))
            if "bloqueada" in respuesta:
                del respuesta["bloqueada"]
    
    SONIDO_CLICK.play()
    return obtener_pregunta_actual(datos_juego, datos_juego["preguntas_filtradas"])

def manejar_respuesta_con_comodines(respuesta_idx, pregunta_actual, datos_juego, lista_respuestas, estado_comodines):
    """Maneja la lógica de respuesta considerando los comodines activos"""
    correcta = pregunta_actual.get("respuesta_correcta")
    
    if respuesta_idx == correcta:
        # Respuesta correcta
        puntos = datos_juego.get("puntos_por_respuesta", PUNTUACION_ACIERTO)
        if estado_comodines["x2_activo"]:
            puntos *= 2
            estado_comodines["x2_activo"] = False
        
        modificar_puntuacion(datos_juego, puntos)
        datos_juego["racha"] += 1
        datos_juego["racha"] = sumar_bonus(datos_juego, datos_juego["racha"])
        
        # Pintar verde
        lista_respuestas[respuesta_idx - 1]["superficie"].fill(COLOR_VERDE)
        
        # Resetear doble chance si estaba activa
        if estado_comodines["doble_chance_activa"]:
            estado_comodines["doble_chance_activa"] = False
            estado_comodines["doble_chance_usada"] = False
        
        return True
    else:
        # Respuesta incorrecta
        if estado_comodines["doble_chance_activa"] and not estado_comodines["doble_chance_usada"]:
            # Primera oportunidad fallida - solo pintar de rojo
            lista_respuestas[respuesta_idx - 1]["superficie"].fill(COLOR_ROJO)
            lista_respuestas[respuesta_idx - 1]["bloqueada"] = True
            estado_comodines["doble_chance_usada"] = True
            SONIDO_ERROR.play()
            return None  # No avanzar pregunta
        else:
            # Sin doble chance o segunda oportunidad fallida
            puntos_error = datos_juego.get("puntos_error", PUNTUACION_ERROR)
            modificar_puntuacion(datos_juego, -abs(puntos_error))
            modificar_vida(datos_juego, -1)
            datos_juego["racha"] = 0
            
            # Pintar correcta en verde, incorrectas en rojo
            for i in range(4):
                if (i + 1) == correcta:
                    lista_respuestas[i]["superficie"].fill(COLOR_VERDE)
                else:
                    lista_respuestas[i]["superficie"].fill(COLOR_ROJO)
            
            # Resetear doble chance
            if estado_comodines["doble_chance_activa"]:
                estado_comodines["doble_chance_activa"] = False
                estado_comodines["doble_chance_usada"] = False
            
            SONIDO_ERROR.play()
            return False

def mostrar_juego(pantalla: pygame.Surface, cola_eventos, datos_juego, categoria_elegida):
    global estado_comodines
    ventana = "juego"
    
    # Inicializar comodines si es la primera vez
    if "comodines" not in datos_juego:
        datos_juego["comodines"] = inicializar_comodines()
    
    estado_comodines = datos_juego["comodines"]
    
    if "preguntas_filtradas" not in datos_juego:
        datos_juego["preguntas_filtradas"] = [
            p for p in lista_preguntas if p["categoria"] == categoria_elegida.lower()]
        datos_juego["pregunta_actual"] = 0
    
    cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
    lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 4)
    pregunta_actual = obtener_pregunta_actual(datos_juego, datos_juego["preguntas_filtradas"])
    
    if "inicio_pregunta" not in datos_juego:
        iniciar_tiempo_pregunta(datos_juego)
    
    actualizar_tiempo(datos_juego)

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Verificar comodines
            if boton_bomba["rectangulo"].collidepoint(evento.pos) and estado_comodines["bomba_disponible"]:
                activar_comodin_bomba(lista_respuestas, pregunta_actual, estado_comodines)
            
            elif boton_x2["rectangulo"].collidepoint(evento.pos) and estado_comodines["x2_disponible"]:
                activar_comodin_x2(estado_comodines)
            
            elif boton_doble_chance["rectangulo"].collidepoint(evento.pos) and estado_comodines["doble_chance_disponible"]:
                activar_comodin_doble_chance(estado_comodines)
            
            elif boton_pasar["rectangulo"].collidepoint(evento.pos) and estado_comodines["pasar_disponible"]:
                pregunta_actual = activar_comodin_pasar(datos_juego, cuadro_pregunta, lista_respuestas)
                cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
                lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 4)
            
            else:
                # Verificar click en respuestas
                for i, respuesta in enumerate(lista_respuestas):
                    if respuesta and respuesta["rectangulo"].collidepoint(evento.pos):
                        # Verificar si la respuesta está bloqueada
                        if not respuesta.get("bloqueada", False):
                            resultado = manejar_respuesta_con_comodines(
                                i + 1, pregunta_actual, datos_juego, lista_respuestas, estado_comodines
                            )
                            
                            # Solo avanzar si no es doble chance en primera oportunidad
                            if resultado is not None:
                                pygame.time.wait(1000)
                                pasar_pregunta(datos_juego, datos_juego["preguntas_filtradas"])
                                iniciar_tiempo_pregunta(datos_juego)
                                pregunta_actual = obtener_pregunta_actual(datos_juego, datos_juego["preguntas_filtradas"])
                                cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 100)
                                lista_respuestas = crear_lista_respuestas("texturas/textura_respuesta.jpg", 125, 260, 4)
                                estado_comodines["comodin_activo"] = False
    
    if datos_juego.get("cantidad_vidas", 0) <= 0:
        ventana = "terminado"
    
    fondo_actual = fondos.get(categoria_elegida, pygame.Surface(PANTALLA))
    if isinstance(fondo_actual, pygame.Surface) and fondo_actual.get_size() != PANTALLA:
        fondo_actual = pygame.transform.scale(fondo_actual, PANTALLA)
    
    pantalla.blit(fondo_actual, (0, 0))
    mostrar_datos_juego_pygame(pantalla, datos_juego)
    mostrar_pregunta_pygame(pregunta_actual, pantalla, cuadro_pregunta, lista_respuestas)
    
    # Dibujar botones de comodines (esquina superior derecha)
    pantalla.blit(boton_bomba["superficie"], boton_bomba["rectangulo"])
    pantalla.blit(boton_x2["superficie"], boton_x2["rectangulo"])
    pantalla.blit(boton_doble_chance["superficie"], boton_doble_chance["rectangulo"])
    pantalla.blit(boton_pasar["superficie"], boton_pasar["rectangulo"])
    
    # Etiquetas de comodines (texto pequeño debajo de cada botón)
    color_bomba = COLOR_NEGRO if estado_comodines["bomba_disponible"] else COLOR_ROJO
    color_x2 = COLOR_NEGRO if estado_comodines["x2_disponible"] else COLOR_ROJO
    color_doble = COLOR_NEGRO if estado_comodines["doble_chance_disponible"] else COLOR_ROJO
    color_pasar = COLOR_NEGRO if estado_comodines["pasar_disponible"] else COLOR_ROJO
    
    mostrar_texto(pantalla, "BOMBA", (445, 63), FUENTE_ARIAL_20, color_bomba)
    mostrar_texto(pantalla, "X2", (520, 63), FUENTE_ARIAL_20, color_x2)
    mostrar_texto(pantalla, "2X CH", (445, 123), FUENTE_ARIAL_20, color_doble)
    mostrar_texto(pantalla, "PASAR", (505, 123), FUENTE_ARIAL_20, color_pasar)
    
    return ventana