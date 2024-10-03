import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import time
import sched
import requests
import random

# Opciones de voz / idioma
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_texto():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 0.8
        print("Ya puedes hablar")
        audio = r.listen(origen)

        try:
            pedido = r.recognize_google(audio, language="es-ES")
            print(f"Dijiste: {pedido}")
            return pedido
        except sr.UnknownValueError:
            print("Ups, no entendí")
            return "Sigo esperando"
        except sr.RequestError:
            print("Ups, no hay servicio")
            return "Sigo esperando"
        except:
            print("Ups, algo ha salido mal")
            return "Sigo esperando"

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

# Recordatorio para tomar agua
def recordar_agua():
    hablar("Es hora de tomar un vaso de agua.")

# Recordatorio para mejorar postura
def recordar_postura():
    hablar("Por favor, ajusta tu postura para evitar dolores de espalda.")

# Nueva funcionalidad: Recordatorio de higiene bucal
def recordar_higiene_bucal():
    hablar("Recuerda lavarte los dientes después de comer.")

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

# Programar recordatorios
def programar_recordatorios():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(3600, 1, recordar_agua)
    s.enter(1800, 1, recordar_postura)
    s.enter(7200, 1, recordar_higiene_bucal)
    s.run()

# Función para manejar los comandos
def manejar_comandos():
    saludo_inicial()
    while True:
        pedido = transformar_audio_texto().lower()
        
        if "abrir youtube" in pedido:
            hablar("Estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "crear recordatorio de agua" in pedido:
            hablar("Activando recordatorios para tomar agua cada hora.")
            agregar_a_historial("Recordatorio de agua")
            programar_recordatorios()
        elif "recordatorio de postura" in pedido:
            hablar("Activando recordatorios para mejorar postura.")
            agregar_a_historial("Recordatorio de postura")
            programar_recordatorios()
        elif "ejercicio" in pedido:
            sugerir_ejercicio()
        elif "historial" in pedido:
            mostrar_historial()
        elif "adiós" in pedido:
            hablar("Nos vemos, avísame si necesitas otra cosa.")
            break

# Interfaz gráfica con Tkinter
def iniciar_gui():
    ventana = tk.Tk()
    ventana.title("Asistente Virtual de Salud")
    ventana.geometry("400x300")

    # Texto para mostrar los comandos
    label_comandos = tk.Label(ventana, text="Comandos disponibles:")
    label_comandos.pack()

    # Área de texto para mostrar los comandos
    text_area = scrolledtext.ScrolledText(ventana, width=40, height=10)
    text_area.pack()
    text_area.insert(tk.INSERT, "1. abrir youtube\n")
    text_area.insert(tk.INSERT, "2. crear recordatorio de agua\n")
    text_area.insert(tk.INSERT, "3. recordatorio de postura\n")
    text_area.insert(tk.INSERT, "4. ejercicio\n")
    text_area.insert(tk.INSERT, "5. historial\n")
    text_area.insert(tk.INSERT, "6. adiós\n")

    # Botón para iniciar el asistente
    boton_iniciar = tk.Button(ventana, text="Iniciar Asistente", command=lambda: threading.Thread(target=manejar_comandos).start())
    boton_iniciar.pack()

    ventana.mainloop()

# Ejecutar la interfaz gráfica
iniciar_gui()

