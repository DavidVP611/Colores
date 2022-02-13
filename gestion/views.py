from logging import exception
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
    return render(request, 'home.html')

def createQR(request):
    if request.POST:
        mark_error = []
        try:
            import qrcode
            from PIL import Image
            
            code = request.POST.get("code-id")
            name = request.POST.get("code-name")
            quantity = request.POST.get("code-quantity")
            print(f"// code: {code} +++ name: {name} +++ quantity: {quantity} //")
            if code and len(code) > 0:
                if name and Colors_Inventory.objects.filter(pk=code).exists():
                    Colors_Inventory.objects.filter(pk=code).update(name=name)
                elif quantity:
                    quantity = quantity if quantity.isdigit() and int(quantity) > 0 else 0
                    Colors_Inventory.objects.create(code=code, name=name, quantity=quantity)
                elif name == None or len(name) == 0:
                    name = Colors_Inventory.objects.get(pk=code).name if Colors_Inventory.objects.filter(pk=code).exists() else "Desconocido"
                    
            else:
                raise Exception('code')
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
            response = HttpResponse(content_type="image/png")
            response['Content-Disposition'] = f"attachment;filename={code} - {name}.png"
            img.save(response, 'PNG')
            
            return response
        except Exception as inst:
            if inst.get('code'):
                mark_error.append({'title':'No se ha asignado un código', 'body':'Por favor, asignarlo'})            
        return JsonResponse(mark_error, False)
                
    else:        
        return redirect('/')

def readQR_image(request):
    import random
    decoded_info = ['hola']
    if request.POST and request.FILES and request.FILES['image']:
        code = random.randint(1,40000000)
        if Image_Inventory.objects.filter(code=code).exists():
            code = random.randint(1,40000000)            
            Image_Inventory.objects.create(name="color", quantity=4, image=request.POST.get('image'))
        else:
            Image_Inventory.objects.create(code=code, name="color", quantity=4, image=request.POST.get('image'))
        import cv2 as cv
        import numpy        
        from pyzbar import pyzbar
        # im = cv.imread(request.FILES['image'])
        im = cv.imdecode(numpy.fromstring(request.FILES['image'].read(), numpy.uint8), cv.IMREAD_UNCHANGED)
        
        det = cv.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(im)
        
        barcodes = pyzbar.decode(im)
        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the im
            (x, y, w, h) = barcode.rect
            cv.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it on
            # our output im we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the im
            text = "{} ({})".format(barcodeData, barcodeType)
            cv.putText(im, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 2)
            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        
    return JsonResponse(decoded_info, safe=False)

def readQR(request):
    print(request.POST.get('action'), type(request.POST.get('action')))
    mark_error = []
    if request.POST and str(request.POST.get('action')) == "true":
        try:
            # se importan las bibliotecas a utilizar
            import cv2
            import numpy as np
            from pyzbar.pyzbar import decode
            # pip install wheel if lo pide
            # Para linux se debe usar "sudo apt.get install libzbar.dev"   aunque no lo he probado        

            code_safed = ""
            # Detectar la camara
            cap = cv2.VideoCapture(1)
            # Ancho de la camara
            cap.set(3, 420)
            # Altura de la camara
            cap.set(4, 400)
            
            cv2.namedWindow("Camara_Web__Produempak", cv2.WINDOW_KEEPRATIO)
            # while success:
            while cv2.getWindowProperty('Camara_Web__Produempak', cv2.WND_PROP_VISIBLE) >= 1:
                # Se guarda la imagen de la camara
                success, img = cap.read()
                
                # Detectar los códigos de barra en la imagen
                for barcode in decode(img):                
                    # Se decodifica el codigo de barcode
                    mydata = barcode.data.decode('utf-8')
                    
                    # Se imprime el codigo
                    print(mydata)
                    # Esto es para validar y traer el nombre del producto
                    if str(mydata) != code_safed:
                        code_safed = str(mydata)
                        name = Colors_Inventory.objects.get(pk=code_safed).name if Colors_Inventory.objects.filter(pk=code_safed).exists() else "Desconocido"
                    if str(name) == "Desconocido":
                        color = (0,0,255)
                    else:
                        color = (0,255,0)
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
                                name, # Texto
                                (pts2[0], pts2[1]), # Coordenadas
                                cv2.FONT_HERSHEY_COMPLEX, # Tipo letra
                                0.9, # Tamanio letra
                                color, # Color letra
                                1) # Espesor letra
                                    
                #se muestra camara
                cv2.imshow('Camara_Web__Produempak', img)                
                
                # Se espera un milisegundo para terminar la camara (cv2.waitKey(1))
                keyCode = cv2.waitKey(1)
                # Valida si la tecla q o Esc es presionada, para ocasionar el fin del ciclo
                if (keyCode & 0xFF) == ord("q") or (keyCode & 0xFF) == 27:
                    cv2.destroyAllWindows()
                    break
        except Exception as inst:            	
            import traceback
            print(traceback.format_exc())
            print(f"¿? Error: {inst}")
            if str(inst) == "cannot unpack non-iterable NoneType object":
                mark_error.append({'title':'Error de valor nulo', 'body':'Puede que la cámara asignada no se encuentre activa'})
                
            print(f"¿? Error: {mark_error}")
        finally:
            if not cap.release():
                cv2.destroyAllWindows()
                cap.release()
    return JsonResponse(mark_error, safe=False)      

def readJS(request):
    return render(request, "readJS.html", {})

