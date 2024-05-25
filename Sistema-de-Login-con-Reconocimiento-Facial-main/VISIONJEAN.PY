from tkinter import *
from PIL import Image, ImageTk
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()

    archivo = open(usuario_info, "w")
    archivo.write(usuario_info + "\n")
    archivo.write(contra_info)
    archivo.close()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    Label(pantalla1, text="REGISTRO DE MANERA EXITOSA", fg="#00ff00", font=("Old English Text MT", 11), bg="#000000").pack()

def registro_facial():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('REGISTRO FACIAL', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro Facial Exitoso", fg="#00ff00", font=("Old English Text MT", 11), bg="#000000").pack()

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(usuario_img+".jpg", cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)

def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.title("PANTALLA DE BIENVENIDO JEAN POL JIMENEZ")
    pantalla1.geometry("300x250")
    pantalla1.configure(bg="#000000")
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text="REGISTRAR MEDIANTE FACIAL: debe de asignar un usuario:", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    Label(pantalla1, text="REGISTRAR POR CONTRASEÑA: debe asignar usuario y contraseña:", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    Label(pantalla1, text="Usuario * ", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    usuario_entrada = Entry(pantalla1, textvariable=usuario)
    usuario_entrada.pack()
    Label(pantalla1, text="Contraseña * ", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    contra_entrada = Entry(pantalla1, textvariable=contra)
    contra_entrada.pack()
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro Tradicional", width=15, height=1, command=registrar_usuario, bg="#000000", fg="#00ff00", bd=2, relief="groove", font=("Old English Text MT", 11)).pack()
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="REGISTRO FACIAL", width=15, height=1, command=registro_facial, bg="#000000", fg="#00ff00", bd=2, relief="groove", font=("Old English Text MT", 11)).pack()

def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()
    if log_usuario in lista_archivos:
        archivo2 = open(log_usuario, "r")
        verificacion = archivo2.read().splitlines()
        if log_contra in verificacion:
            print("BIENVENIDO AL ESPACIO DE JEAN POL JIMENEZ")
            Label(pantalla2, text="Inicio de Sesion Exitoso", fg="#00ff00", font=("Old English Text MT", 11), bg="#000000").pack()
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text="Contraseña Incorrecta", fg="#ff0000", font=("Old English Text MT", 11), bg="#000000").pack()
    else:
        print("USUARIO NO IDENTIFICADO")
        Label(pantalla2, text="Usuario no encontrado", fg="#ff0000", font=("Old English Text MT", 11), bg="#000000").pack()

def login_facial():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('Login Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_login = verificacion_usuario.get()
    cv2.imwrite(usuario_login+"LOG.jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(usuario_login+"LOG.jpg", cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    def orb_sim(img1, img2):
        orb = cv2.ORB_create()
 
        kpa, descr_a = orb.detectAndCompute(img1, None)
        kpb, descr_b = orb.detectAndCompute(img2, None)

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = comp.match(descr_a, descr_b)

        regiones_similares = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)
        
    im_archivos = os.listdir()
    if usuario_login+".jpg" in im_archivos:
        rostro_reg = cv2.imread(usuario_login+".jpg", 0)
        rostro_log = cv2.imread(usuario_login+"LOG.jpg", 0)
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            Label(pantalla2, text="Inicio de Sesion Exitoso", fg="#00ff00", font=("Old English Text MT", 11), bg="#000000").pack()
            print("Bienvenido al sistema usuario: ", usuario_login)
            print("Compatibilidad con la foto del registro: ", similitud)
        else:
            print("Rostro incorrecto, verifique su usuario")
            print("Compatibilidad con la foto del registro: ", similitud)
            Label(pantalla2, text="Incompatibilidad de rostros", fg="#ff0000", font=("Old English Text MT", 11), bg="#000000").pack()
    else:
        print("USUARIO DESCONOCIDO")
        Label(pantalla2, text="Usuario no encontrado", fg="#ff0000", font=("Old English Text MT", 11), bg="#000000").pack()

def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("JEAN POL JIMENEZ")
    pantalla2.geometry("400x300")
    pantalla2.configure(bg="#000000")
    Label(pantalla2, text="Login facial: debe de asignar un usuario:", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    Label(pantalla2, text="Login tradicional: debe asignar usuario y contraseña:", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    Label(pantalla2, text="").pack()
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    
    Label(pantalla2, text="Usuario * ", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    usuario_entrada2 = Entry(pantalla2, textvariable=verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text="Contraseña * ", fg="#00ff00", bg="#000000", font=("Old English Text MT", 11)).pack()
    contra_entrada2 = Entry(pantalla2, textvariable=verificacion_contra)
    contra_entrada2.pack()
    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesion Tradicional", width=20, height=1, command=verificacion_login, bg="#000000", fg="#00ff00", bd=2, relief="groove", font=("Old English Text MT", 11)).pack()
    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesion Facial", width=20, height=1, command=login_facial, bg="#000000", fg="#00ff00", bd=2, relief="groove", font=("Old English Text MT", 11)).pack()
        
def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("400x300")
    pantalla.title("RECONOCIMIENTO FACIAL JEAN POL")
    
    # Cargar la imagen de fondo con PIL
    ruta_imagen_fondo = r"C:\Users\Soporte\Desktop\RECONOCIMIENTO\fondo.jpg"
    imagen_fondo = Image.open(ruta_imagen_fondo)
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    fondo = Label(pantalla, image=imagen_fondo)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)

    Label(text="Login Inteligente", bg="#000000", width="300", height="2", font=("Old English Text MT", 13), fg="#00ff00").pack()
    
    Label(text="").pack()
    Button(text="Iniciar Sesion", height="2", width="30", command=login, bg="#000000", fg="#00ff00", bd=2, relief="groove", font=("Old English Text MT", 11)).pack()
    Label(text="").pack()
    Button(text="Registro", height="2", width="30", command=registro, bg="#000000", fg="#00ff00", bd=2, relief="groove", font=("Old English Text MT", 11)).pack()

    pantalla.mainloop()

pantalla_principal()
