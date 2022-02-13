from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.
def view_text(request):
    """ View text
    """
    return render(request, 'text.html')
def ordenar_puntos(puntos):
    import numpy as np
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
    
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]
    
    
def read_text_d(request):
    decoded_info = ['hola']
    # instalar tesseact de https://github.com/tesseract-ocr/tessdoc
    if request.POST and request.FILES and request.FILES['image']:
        import cv2 as cv
        import numpy
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'
        im = cv.imdecode(numpy.fromstring(request.FILES['image'].read(), numpy.uint8), cv.IMREAD_UNCHANGED)
        im = cv.resize(im, None, fx=0.5, fy=0.5)
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        
        canny = cv.Canny(gray, 10, 150)
        canny = cv.dilate(canny, None, iterations=1)
        
        cnts = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:1]
        
        gray = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 113,11)
        config = '--psm 4'
        texto_gray = pytesseract.image_to_string(gray, lang='spa', config=config)
        print('texto_gray: ', len(texto_gray), " - ", texto_gray)
        
        from pytesseract import Output
        d = pytesseract.image_to_data(gray, output_type=Output.DICT, lang='spa')
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(float(d['conf'][i])) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                gray = cv2.rectangle(gray, (x,y), (x+w, y+h), (0, 0, 255), 2)
        
        cv.imshow('gray', gray)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
        
        # import re
        # from contexto.lectura import Lector, leer_texto
        # from contexto.escritura import Escritor, escribir_texto
    return JsonResponse(decoded_info, safe=False)
  
  
import cv2
import numpy as np
import pytesseract

        
def get_grayscale(image)       :
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
def remove_noise(image):
    return cv2.medianBlur(image, 5)
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
def dilate(image):
    kernel = np.ones((5,5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)
def erode(image):
    kernel = np.ones((5,5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)
def opening_def(image):
    kernel = np.ones((5,5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
def canny_def(image):
    return cv2.Canny(image, 100, 200)
def deskew(image):
    coords = np.column_stack(np.where(image>0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h,w) = image.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M,(w,h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated
    
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def read_text_s(request):
    decoded_info = ['hola']
    # instalar tesseact de https://github.com/tesseract-ocr/tessdoc
    
    if request.POST and request.FILES and request.FILES['image']:
        pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'
        img = cv2.imdecode(np.fromstring(request.FILES['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
        gray = get_grayscale(img)
        # cv2.imshow("gray", gray)
        thresh = thresholding(gray)
        # cv2.imshow("thresh", thresh)
        opening = opening_def(gray)
        # cv2.imshow("opening", opening)
        canny = canny_def(gray)
        # cv2.imshow("canny", canny)
        from pytesseract import Output
        
        custom_config = r'--oem 3 --psm 6'
        d = pytesseract.image_to_data(thresh, output_type=Output.DICT, lang='spa')
        
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(float(d['conf'][i])) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(thresh, (x,y), (x+w, y+h), (0, 0, 255), 2)
        cv2.imshow('img', img)
        print(d['text'])   
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return JsonResponse(decoded_info, safe=False)