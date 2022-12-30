# CODIGO ALPHA
""" 
################## COMANDOS: ######################
    -reproduce [...]: Comando para abrir una busqueda en Youtube
    -busca [...]: Comando para obtener el resultado de una busqueda
    -significado de [...]: Comando para obtener el resultado de una busqueda
    -alarma [...]: Comando para programar una alarma
    -abre [...]: Comando para abrir una direccion URL (del diccionario "sites") en Edge o una app (del diccionario "programas")
    -archivo [...]: Comando para abrir un archivo (del diccioanrio "files")
    -toma nota: Comando para escribir un dictado, en un archivo .txt
    -escribe [...]: Comando para escribir un dictado, en un archivo .txt
    -termina: Comando para terminar la escucha
###################################################
"""
#LIBRERIAS
import speech_recognition as sr #Importando libreria Speech Recognition, para temas de reconocimiento de voz
import subprocess as sub #Importando libreria Subprocess, para diferentes procesos con el sistema
import pyttsx3 #Importando libreria pyttsx3, para temas de reconocimiento de voz
import pywhatkit #Importando libreria pywhatkit, para temas de reconocimiento de voz
import wikipedia #Importando libreria wikipedia, para la obtencion de la informacion cuando se le solicita
import datetime #Importando libreria datetime, para la alarma
import keyboard #Importando libreria keyboard, para la alarma
import os #Importando libreria os, para procesos con el sistema
from tkinter import * #Importando libreria tkinter, para la interfaz
from PIL import Image, ImageTk #Importando modulos de la libreria PIL, para la interfaz
from pygame import mixer #Importando libreria pygame, para la interfaz
import threading as tr #Importando libreria threading, para hilar procesos

#CONFIGURACION DE LA INTERFAZ
main_window = Tk()
main_window.title("Tesla IA")
main_window.geometry("250x600")
main_window.resizable(0,0)
main_window.configure(bg='#434343')

#CONFIGURACION DEL CUADRO DE TEXTO
text_info = Text(main_window, bg="#92FE9D", fg="Black")
text_info.place(x=25, y=280, height=100, width=200)

#CONFIGURACION DEL GIF EN LA INTERFAZ
tesla_gif_rostro = "images/wavyT.gif"
info_gif = Image.open(tesla_gif_rostro)
gif_nframes = info_gif.n_frames
tesla_gif_list = [PhotoImage(file=tesla_gif_rostro, format=f'gif -index {i}') for i in range(gif_nframes)]
label_gif = Label(main_window)
label_gif.pack(pady=5)

#FUNCION PARA LA ANIMACION DEL GIF
def animated_gif(index):
    frame = tesla_gif_list[index]
    index += 1
    if index == gif_nframes:
        index = 0
    label_gif.configure(image=frame)
    main_window.after(20, animated_gif, index)

animated_gif(0)


name = "Tesla" #DECLARACION DEL NOMBRE DEL SISTEMA
engine = pyttsx3.init() #INICIO DE LA LIBRERIA pyttsx3

#ASIGNACION Y CONFIGURACION DE LA VOZ
voices = engine.getProperty('voices')
# Asignacion de la vos en Español Mexico
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)


# DICCIONARIOS
sites = {  # Diccioario de sitios web
    'google': 'google.com', #CLAVE PARA ABIRIR GOOGLE
    'youtube': 'youtube.com', #CLAVE PARA ABIRIR YOUTUBE
    'facebook': 'facebook.com', #CLAVE PARA ABIRIR FACEBOOK
    'correo': 'outlook.live.com', #CLAVE PARA ABIRIR OUTLOOK
    'gmail': 'gmail.com', #CLAVE PARA ABIRIR GMAIL
    'cursos': 'www.udemy.com', #CLAVE PARA ABIRIR UDEMY
    'classroom': 'classroom.google.com' #CLAVE PARA ABIRIR CLASSRROM
}

files = {  # Diccioario de documentos para poder abrir
    'boletos': 'BoletosBioparqueEstrella.pdf', #CLAVE PARA ABIRIR EL DOCUMENTO BOLETOS
    'notas': 'ENCUESTA_SEGUIMIENTO_spProyectoConsultarPorId.txt', #CLAVE PARA ABIRIR EL DOCUMENTO EN BLOCK DE NOTAS
}
programas = {  # Diccioanrio de aplicaciones para poder abrir
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE", #CLAVE PARA ABIRIR WORD
    'excel': r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE", #CLAVE PARA ABIRIR EXCEL
    'code': r"C:\Users\est11\AppData\Local\Programs\Microsoft VS Code\Code.exe", #CLAVE PARA ABIRIR VSC
    'chrome': r"C:\Program Files\Google\Chrome\Application\chrome.exe", #CLAVE PARA ABIRIR CHROME
    'edge': r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" #CLAVE PARA ABIRIR MICROSOFT EDGE
}

#FUNCION CON LAS INTRUCCIONES PARA QUE EL SISTEMA HABLE
def talk(text):
    engine.say(text)
    engine.runAndWait()

#FUNCION CON LAS INTRUCCIONES PARA QUE EL SISTEMA LEA LO QUE SE LE INDICO
def read_talk():
    text = text_info.get("1.0", "end") #PRINCIPIO A FIN
    talk(text)

#FUNCION CON LAS CONFIGURACIONES INICIALES DEL SISTEMA 
def listen():
    listener = sr.Recognizer() 
    with sr.Microphone() as source:  # Usar el microfono como la fuente
        #listener.adjust_for_ambient_noise(source) #FUNCION PARA REDUCIR EL RUIDO AMBIENTAL (SUELE ENTORPECER EL FUNCIONAIENTO)
        talk("¿En que puedo ayudarte?")
        pc = listener.listen(source)
    try:
        # Configuracion del idioma Español
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
        if name in rec:
            rec = rec.replace(name, '')
    except sr.UnknownValueError:  # En caso de no encontrar algun comando ya programado
        print("No te entendí, intenta de nuevo")
    return rec

#FUNCION PARA EL FUNCIONAMIENTO DE LA ALARMA
def clock(rec):
    num = rec.replace('alarma', '') #QUITAR LA PALABRA ALARMA DE LA ORACION 
    num = num.strip()
    talk("Alarma activada " + num + " horas") 
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("Hora de Despertar")
            mixer.music.load("Despertador.mp3") #TONO DE ALARMA
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s": #DETENER LA ALARMA
            mixer.music.stop()
            break

def run_codar():
    while True:  # Ciclo para que pueda seguir escuchando despues de un comando
        try:
            rec = listen()
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo") #En caso de que no entienda la intruccion
            continue
        if 'reproduce' in rec:  # Comando para abrir una busqueda en Youtube
            music = rec.replace('reproduce', '') #quitar la palabra reproduce de la oracion
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:  # Comando para obtener el resultado de una busqueda
            search = rec.replace('busca', '') #quitar la palabra busa de la oracion
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": " + wiki)
            talk(wiki)
        elif 'significado de' in rec:  # Comando para obtener el resultado de una busqueda
            search = rec.replace('significado de', '') #quitar la palabra "significado de" de la oracion
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": " + wiki)
            talk(wiki)
        elif 'alarma' in rec:  # Comando para programar una alarma
            t = tr.Thread(target=clock, args=(rec,)) #llamada de la funcion clock e hilado de procesos
            t.start()
        elif 'abre' in rec:  # Comando para abrir...
            # ...una direccion URL (del diccionario "sites") en Edge
            for site in sites:
                if site in rec:
                    sub.call(
                        f'start MicrosoftEdge.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programas:  # ...una app (del diccionario "programas")
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.startfile(programas[app])
        # Comando para abrir un archivo (del diccioanrio "files")
        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'toma nota' in rec:  # Comando para escribir un dictado, en un archivo .txt
            try:
                with open("nota.txt", 'a') as f:  # Agrega el dictado al archivo "nota.txt"
                    write(f)
            except FileNotFoundError as e:  # Si no existe "nota.txt"
                file = open("nota.txt", 'w')
                write(file)
        elif 'escribe' in rec:  # Comando para escribir un dictado, en un archivo .txt
            try:
                with open("nota.txt", 'a') as f:  # Agrega el dictado al archivo "nota.txt"
                    write(f)
            except FileNotFoundError as e:  # Si no existe "nota.txt"
                file = open("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:  # Comando para terminar la escucha
            print("Vale, adios!")
            talk('Vale, adios!')
            break 

main_window.update()

def write(f):  # Funcion para las instrucciones del manejo del nuevo .txt
    talk("¿Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

button_listen = Button(main_window, text="Escuchar", fg="black", bg="#00C9FF",  #Boton para activar la escucha
                        font=("Arial", 10, "bold"), width=10, height=1 ,command=run_codar)
button_listen.pack(pady=10)
button_speak = Button(main_window, text="Hablar", fg="black", bg="#00C9FF", 
                        font=("Arial", 10, "bold"), width=10, height=1 ,command=read_talk) #Boton para activar la voz y reproducir lo que se le escribio
button_speak.pack(pady=150)

main_window.mainloop()