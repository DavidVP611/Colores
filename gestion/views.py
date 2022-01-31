from logging import exception
from cv2 import VideoCapture
from django.shortcuts import render, redirect
from .models import *
from profiles.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.http import JsonResponse
# Create your views here.

# @login_required
def home(request):
    """ View main
    """
    with open('../qr/data.json') as file:
        data = json.load(file)
    return render(request, 'home.html', {'data':data})

def codeQR(request):
    """ View Code """
    with open('../qr/data.json') as file:
        data = json.load(file)
        print(data['code'])
    return JsonResponse(data)

def createQR(request):
    if request.POST:
        import qrcode
        from PIL import Image
        code = request.POST.get("code-id")
        name = request.POST.get("code-name")
        quantity = request.POST.get("code-quantity")
        
        if len(code) > 0 and len(name) > 0:
            if Colors_Inventory.objects.filter(pk=code).exists():
                Colors_Inventory.objects.filter(pk=code).update(name=name)
            else:
                quantity = quantity if quantity.isdigit() and int(quantity) > 0 else 0
                Colors_Inventory.objects.create(code=code, name=name, quantity=quantity)
        else:
            pass
        qr = qrcode.QRCode(
            version = 1,
            error_correction= qrcode.constants.ERROR_CORRECT_L,
            box_size = 10,
            border = 4,
        )
        qr.clear()
        qr.add_data(str(code))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#f3872a", back_color="#f7f7fa")
        # return img
        response = HttpResponse(content_type="image/png")
        response['Content-Disposition'] = f"attachment;filename={code} - {name}.png"
        img.save(response, 'PNG')
        
        return response
    else:        
        return redirect('/')

def readQR_image(request):
    # Leerlo desde una imagen
    # pip install pyzbar
    # apt install libzbar0
    from pyzbar import pyzbar
    from PIL import Image
    
    image = Image.open("../ver3.png")
    qr_code = pyzbar.decode(image)[0]
    
    #convert into string
    data = qr_code.data.decode('utf8').decode('shift-jis').decode('utf-8')
    print("El mensaje es: ",data)
    
def readQR(request):
    if request.POST:
        try:
            # se importan las bibliotecas a utilizar
            import cv2
            import numpy as np
            from pyzbar.pyzbar import decode
            # pip install wheel
            # Es necesario tener instalado pyzbar para usar pyzbar - requiere de Microsoft Visual C++ 14.0
            # Para linux se debe usar "sudo apt.get install libzbar.dev"

            # Detectar la camara
            cap = cv2.VideoCapture(1)
            # Ancho de la camara
            cap.set(3, 680)
            # Altura de la camara
            cap.set(4, 480)

            # Mientras el bucle funcione
            action = request.POST.get("action")
            print(f"-- action: {action} -- {type(action)}")
            print(str(action) == "true")
            while str(action) == "true":
                # Se guarda la imagen de la camara
                success, img = cap.read()
                
                # Detectar los códigos de barra en la imagen
                for barcode in decode(img):                
                    # Se decodifica el codigo de barcode
                    mydata = barcode.data.decode('utf-8')
                    
                    # Se imprime el codigo
                    print(mydata)
                    
                    # si el codig barcode esta en la lista de accesos
                    # if mydata in mydatalist:
                    myoutput = "Autorizado"
                    color = (0,255,0)
                    # else:
                    #     myoutput = "No autorizado"
                    #     color = (0,0,255)
                    
                    # Coordenadas del barcode
                    pts = np.array([barcode.polygon],np.int32)
                    
                    # Se modifica el arreglo de pts
                    pts = pts.reshape((-1,1,2))
                    
                    # Se crea el cuadro de color segun el estado
                    cv2.polylines(img, # Imagen
                                [pts], # Coordenadas
                                True, # El poligono es cerrado
                                color, # Color del cuadro
                                5) # El espesor del polígono
                    
                    # Forma del segundo rectángulo para el texto
                    pts2 = barcode.rect
                    # Se va a colocar el texto en el cuadro
                    cv2.putText(img, # Imagen
                                myoutput, # Texto
                                (pts2[0], pts2[1]), # Coordenadas
                                cv2.FONT_HERSHEY_COMPLEX, # Tipo letra
                                0.9, # Tamanio letra
                                color, # Color letra
                                1) # Espesor letra
                                    
                #se muestra camara
                cv2.imshow('Camara Web - Produempak', img)
                
                
                # Se espera un milisegundo para terminar la camara
                cv2.waitKey(1)
        finally:
            if not cap.release():
                cap.release()
                cv2.destroyAllWindows()
    return JsonResponse({'1':'Hola'})


def readQR_A(request):
    if request.POST:
        # se importan las bibliotecas a utilizar
        import cv2
        
        # initalize the cam
        cap = cv2.VideoCapture(1)
        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read()
            # detect and decode
            data, bbox, _ = detector.detectAndDecode(img)
            # check if there is a QRCode in the image
            if bbox is not None:
                # display the image with lines
                for i in range(len(bbox)):
                    # draw all lines
                    cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
                if data:
                    print("[+] QR Code detected, data:", data)
            # display the result
            cv2.imshow("img", img)    
            if cv2.waitKey(1) == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()