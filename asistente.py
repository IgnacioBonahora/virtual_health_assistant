import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import random

# Opciones de voz / idioma
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Variable para controlar el estado del asistente
asistente_activo = False  

# Variables para los recordatorios
recordatorios_activos = False
timers = []  

# Mapa de números en texto a números enteros
numeros_texto_a_numero = {
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20
}

# Escuchar nuestro micrófono y devolver el audio como texto
def transformar_audio_texto():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 0.8
        print("Ya puedes hablar")
        try:
            audio = r.listen(origen, timeout=5, phrase_time_limit=10)  
            pedido = r.recognize_google(audio, language="es-ES")
            print(f"Dijiste: {pedido}")
            return pedido
        except sr.UnknownValueError:
            print("No entendí el comando.")
            return None
        except sr.RequestError:
            print("Error en el servicio de reconocimiento.")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)
    engine.say(mensaje)
    engine.runAndWait()

# Función saludo inicial
def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
    hablar(f"{momento}, en qué te puedo ayudar?")

# Recordatorios
def recordar_agua():
    hablar("Es hora de tomar un vaso de agua.")
    programar_recordatorio(recordar_agua, intervalo_agua)

def recordar_postura():
    hablar("Por favor, ajusta tu postura para evitar dolores de espalda.")
    programar_recordatorio(recordar_postura, intervalo_postura)

def recordar_higiene_bucal():
    hablar("Recuerda lavarte los dientes después de comer.")
    programar_recordatorio(recordar_higiene_bucal, intervalo_higiene)

def recordar_relajamiento_ojos():
    hablar("Recuerda relajar tus ojos y descansarlos.")

# Sugerencia aleatoria de ejercicios
def sugerir_ejercicio():
    ejercicios = [
        "Haz 10 minutos de estiramientos para relajar tu cuerpo.",
        "Realiza una caminata de 15 minutos.",
        "Haz 20 abdominales para fortalecer tu core.",
        "Haz una serie de 10 flexiones de brazos."
    ]
    ejercicio_seleccionado = random.choice(ejercicios)
    hablar(f"Te sugiero el siguiente ejercicio: {ejercicio_seleccionado}")

# Historial de recordatorios
historial_recordatorios = []

def agregar_a_historial(recordatorio):
    historial_recordatorios.append(recordatorio)
    hablar(f"Se ha agregado al historial: {recordatorio}")

def mostrar_historial():
    if historial_recordatorios:
        hablar("Este es el historial de recordatorios:")
        for recordatorio in historial_recordatorios:
            hablar(recordatorio)
    else:
        hablar("No hay recordatorios en el historial.")

# Función para verificar si una cadena es numérica o si es un número en texto
def es_numero(texto):
    return texto.isdigit() or texto in numeros_texto_a_numero

# Función para convertir el texto de un número a entero
def convertir_a_numero(texto):
    return int(texto) if texto.isdigit() else numeros_texto_a_numero.get(texto, None)

# Función para programar recordatorios usando threading.Timer
def programar_recordatorio(funcion, intervalo_minutos):
    timer = threading.Timer(intervalo_minutos * 60, funcion)
    timer.start()
    timers.append(timer)

# Variables globales para los intervalos
intervalo_agua = 0
intervalo_postura = 0
intervalo_higiene = 0

# Programar recordatorios de salud
def iniciar_recordatorios():
    global recordatorios_activos
    recordatorios_activos = True
    programar_recordatorio(recordar_agua, intervalo_agua)
    programar_recordatorio(recordar_postura, intervalo_postura)
    programar_recordatorio(recordar_higiene_bucal, intervalo_higiene)
    programar_recordatorio(recordar_relajamiento_ojos, 20)  # Cada 20 minutos

# Función para manejar los comandos
def manejar_comandos(ventana):
    global asistente_activo, recordatorios_activos, timers, intervalo_agua, intervalo_postura, intervalo_higiene
    saludo_inicial()

    while True:  
        pedido = transformar_audio_texto()

        if not pedido:  
            print("Lo siento, no entendí eso. Por favor, intenta de nuevo.")
            continue

        pedido = pedido.lower()

        if "activar asistente" in pedido and not asistente_activo:
            asistente_activo = True
            hablar("El asistente está activado.")

        elif asistente_activo:  
            if "abrir youtube" in pedido or "abrir un video en youtube" in pedido:
                hablar("¿Qué video deseas ver en YouTube?")
                video_pedido = transformar_audio_texto()
                if video_pedido:
                    hablar(f"Estoy buscando {video_pedido} en YouTube.")
                    pywhatkit.playonyt(video_pedido.lower())

            elif "establecer recordatorios de salud" in pedido:
                hablar("¿Cada cuántos minutos quieres el recordatorio de agua?")
                intervalo_agua = transformar_audio_texto()
                while not (intervalo_agua and es_numero(intervalo_agua)):
                    hablar("Lo siento, por favor, dime un número válido para el recordatorio de agua.")
                    intervalo_agua = transformar_audio_texto()
                intervalo_agua = convertir_a_numero(intervalo_agua)
                hablar(f"Intervalo de agua establecido en {intervalo_agua} minutos.")

                hablar("¿Cada cuántos minutos quieres el recordatorio de postura?")
                intervalo_postura = transformar_audio_texto()
                while not (intervalo_postura and es_numero(intervalo_postura)):
                    hablar("Lo siento, por favor, dime un número válido para el recordatorio de postura.")
                    intervalo_postura = transformar_audio_texto()
                intervalo_postura = convertir_a_numero(intervalo_postura)
                hablar(f"Intervalo de postura establecido en {intervalo_postura} minutos.")

                hablar("¿Cada cuántos minutos quieres el recordatorio de higiene bucal?")
                intervalo_higiene = transformar_audio_texto()
                while not (intervalo_higiene and es_numero(intervalo_higiene)):
                    hablar("Lo siento, por favor, dime un número válido para el recordatorio de higiene bucal.")
                    intervalo_higiene = transformar_audio_texto()
                intervalo_higiene = convertir_a_numero(intervalo_higiene)
                hablar(f"Intervalo de higiene bucal establecido en {intervalo_higiene} minutos.")

                agregar_a_historial(f"Recordatorios activados: Agua cada {intervalo_agua} minutos, Postura cada {intervalo_postura} minutos, Higiene bucal cada {intervalo_higiene} minutos.")
                
                # Detener temporizadores anteriores si los hay
                for timer in timers:
                    timer.cancel()
                timers.clear()
                
                # Iniciar nuevos recordatorios
                iniciar_recordatorios()
                hablar("Recordatorios activados.")

            elif "ejercicio" in pedido:
                sugerir_ejercicio()

            elif "historial" in pedido:
                mostrar_historial()

            elif "desactivar asistente" in pedido or "pausar asistente" in pedido:
                hablar("El asistente está desactivado.")
                asistente_activo = False
                recordatorios_activos = False
                for timer in timers:
                    timer.cancel()
                timers.clear()

            elif "adiós" in pedido or "chau" in pedido or "cerrar" in pedido or "salir" in pedido:
                hablar("Nos vemos, cerrando la aplicación.")
                recordatorios_activos = False
                for timer in timers:
                    timer.cancel()
                timers.clear()
                ventana.quit()  # Cerrar la ventana y terminar la aplicación
                break

# Interfaz gráfica con Tkinter
def iniciar_gui():
    ventana = tk.Tk()
    ventana.title("Asistente Virtual de Salud")
    ventana.geometry("400x400")  
    ventana.configure(bg="#f0f8ff")  

    # Texto para mostrar los comandos
    label_comandos = tk.Label(ventana, text="Comandos disponibles:", bg="#f0f8ff", font=("Arial", 12))
    label_comandos.pack(pady=10)

    # Área de texto para mostrar los comandos
    text_area = scrolledtext.ScrolledText(ventana, width=40, height=15, bg="#e0ffff", font=("Arial", 10))
    text_area.pack(padx=10, pady=10)
    
    text_area.insert(tk.INSERT, "1. activar asistente\n")
    text_area.insert(tk.INSERT, "2. abrir youtube (video específico)\n")
    text_area.insert(tk.INSERT, "3. establecer recordatorios de salud\n")
    text_area.insert(tk.INSERT, "4. ejercicio\n")
    text_area.insert(tk.INSERT, "5. historial\n")
    text_area.insert(tk.INSERT, "6. desactivar (desactivar asistente)\n")
    text_area.insert(tk.INSERT, "7. adiós / detener (cerrar la aplicación)\n")

    # Botón para iniciar el asistente
    boton_iniciar = tk.Button(
        ventana, 
        text="Iniciar Asistente", 
        command=lambda: threading.Thread(target=manejar_comandos, args=(ventana,), daemon=True).start(), 
        bg="#add8e6", 
        font=("Arial", 10)
    )
    boton_iniciar.pack(pady=10)

    ventana.mainloop()

# Ejecutar la interfaz gráfica
iniciar_gui()








