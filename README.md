# Asistente Virtual de Salud

¡Bienvenido al Asistente Virtual de Salud! Este asistente está diseñado para ayudar a los usuarios con recordatorios de salud, sugerencias de ejercicios y notas personales. Utiliza tecnologías de reconocimiento de voz y síntesis de voz para interactuar con el usuario.

---

## 📋 Requisitos

Antes de ejecutar el asistente, asegúrate de tener instalado **Python** (versión 3.6 o superior). Además, necesitarás las siguientes bibliotecas:

- `tkinter`
- `pyttsx3`
- `speech_recognition`
- `pywhatkit`
- `datetime`
- `random`

---

## 🚀 Instalación

Para configurar el proyecto en tu máquina local, sigue los siguientes pasos:

### 1. Clonar el repositorio

Clona este repositorio a tu máquina local:

```bash
git clone https://github.com/tu_usuario/asistente_virtual_salud.git
cd asistente_virtual_salud

```
### 2. Crea un entorno virtual
Es recomendable crear un entorno virtual para evitar conflictos entre dependencias de diferentes proyectos. Para crear y activar un entorno virtual, sigue estos pasos:
### windows
```bash
python -m venv venv
venv\Scripts\activate

```
### macOS y linux
```bash
python3 -m venv venv
source venv/bin/activate

```
### 3. Instalar dependencias
Una vez que el entorno virtual esté activado, instala las dependencias necesarias utilizando el archivo requirements.txt que se encuentra en la raíz del proyecto:
```bash
pip install -r requirements.txt

```
### 4. Configurar la voz de TTS (opcional)
El asistente utiliza la voz de "Helena" de Microsoft para la síntesis de voz. Asegúrate de que tienes la voz instalada en tu sistema. Si utilizas un sistema diferente, modifica la variable id3 en el código para que apunte a la voz que deseas utilizar.

### 🎬 Ejecución
Para ejecutar el asistente, asegúrate de que el entorno virtual esté activado y utiliza el siguiente comando:
```bash
python main.py
```

### 📢 Comandos Disponibles
algunos comandos que puedes usar:

- **activar asistente**: Activa el asistente.
- **abrir youtube**: Abre un video específico en YouTube.
- **establecer recordatorios de salud**: Configura recordatorios para beber agua, mantener buena postura y practicar la higiene bucal.
- **ejercicio**: Sugiere un ejercicio aleatorio.
- **historial**: Muestra el historial de recordatorios.
- **agregar nota**: Permite agregar notas personales.
- **mostrar notas**: Muestra las notas guardadas.
- **desactivar asistente**: Desactiva el asistente.
- **adiós / cerrar**: Cierra la aplicación.