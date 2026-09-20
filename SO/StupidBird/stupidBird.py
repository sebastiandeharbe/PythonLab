import sys
import os
import threading
import time
import random
import keyboard
import pystray
from PIL import Image, ImageDraw

# --- Función para obtener la ruta correcta del archivo ---
def obtener_ruta_recurso(nombre_archivo):
    """
    Obtiene la ruta absoluta al recurso, funciona para desarrollo
    y para el ejecutable generado con PyInstaller (_MEIPASS).
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.abspath("."), nombre_archivo)

# --- Estado global y control del bucle ---
activo = False
en_ejecucion = True
hilo_loop = None

INTERVALO = 1.0  # Segundos entre teclas
INTERVALO_MIN = 1.0
INTERVALO_MAX = 10.0

def bucle_teclas():
    """Bucle en segundo plano que envía F15 y F16 si el script está activo."""
    global activo, en_ejecucion
    while en_ejecucion:
        if activo:
            keyboard.send("f15")
            INTERVALO = random.uniform(INTERVALO_MIN, INTERVALO_MAX)
            time.sleep(INTERVALO)
            if activo:
                keyboard.send("f16")
                INTERVALO = random.uniform(INTERVALO_MIN, INTERVALO_MAX)
                time.sleep(INTERVALO)
        else:
            time.sleep(0.2)  # Pausa breve para no saturar la CPU mientras esté inactivo


def alternar_estado(icon, item):
    """Activa o desactiva la pulsación según el estado actual."""
    global activo
    activo = not activo


def salir(icon, item):
    """Detiene el bucle y cierra el icono del tray."""
    global en_ejecucion, activo
    activo = False
    en_ejecucion = False
    icon.stop()


def cargar_icono():
    """Carga el archivo .ico desde la raíz del proyecto."""
    ruta_ico = obtener_ruta_recurso("trayicon.ico")  # Reemplaza 'icono.ico' por el nombre real de tu archivo
    return Image.open(ruta_ico)


def main():
    global hilo_loop

    # Iniciar el hilo del bucle de teclado
    hilo_loop = threading.Thread(target=bucle_teclas, daemon=True)
    hilo_loop.start()

    # Menú contextual del System Tray
    # Checked indica visualmente con un tic cuál está activo actualmente
    menu = pystray.Menu(
        pystray.MenuItem(
            "Activar",
            alternar_estado,
            checked=lambda item: activo,
            enabled=lambda item: not activo,
        ),
        pystray.MenuItem(
            "Desactivar",
            alternar_estado,
            checked=lambda item: not activo,
            enabled=lambda item: activo,
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", salir),
    )

    # Crear y ejecutar el icono
    icono = pystray.Icon(
        name="AutoKeyTray",
        icon=cargar_icono(),
        title="Stupid Bird",
        menu=menu,
    )

    icono.run()


if __name__ == "__main__":
    main()