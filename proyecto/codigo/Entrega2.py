import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from PIL import Image
import pandas as pd
import string

path = input("Ingrese la ruta de carpeta ")
path = path.replace('\'', '/')
carpeta = os.listdir(path)
cont = 0
for x in carpeta:
    
    with open(str(path + "/" + x), 'r') as data:

        archivo = genfromtxt(data, delimiter = ',')#se genera matriz del csv
        nombrearchivo = "vaca" + str(cont) + ".jpeg"
        cv2.imwrite(nombrearchivo, archivo) #se guarda como imagen la matriz


        img = cv2.imread(nombrearchivo, 0) #Lee la imagen

        height, width = img.shape

        if (height % 2 == 1):
            height += 1

        if (width % 2 == 1):
            width += 1

        resized_img = cv2.resize(img, (width, height))

        img1 = resized_img.astype ('float') #Convertir uint8 a tipo flotante
        
        img_dct = cv2.dct (img1) # Realizar transformada de coseno discreta
        
        img_dct_log = np.log (abs (img_dct)) #hacer procesamiento de registro
        
        img_recor = cv2.idct (img_dct) # Realizar transformada coseno discreta inversa
        
        # Compresión de imagen, solo conserva 100 * 100 datos
        recor_temp = img_dct[0:150,0:150] 
        recor_temp2 = np.zeros(img.shape)
        recor_temp2[0:150,0:150] = recor_temp
        

        height, width = recor_temp2.shape

        if (height % 2 == 1):
            height += 1

        if (width % 2 == 1):
            width += 1

        resized_temp2 = cv2.resize(recor_temp2, (width, height)) 
        # Recuperación de imágenes comprimidas
        img_recor1 = cv2.idct(resized_temp2) #Aquí está el array con la imagen descomprimida

        cv2.imwrite(nombrearchivo, img_recor1) #Se crea la imagen comprimida
        df = pd.DataFrame(recor_temp) #Aquí se crea un DataFrame con el archivo recor_temp
        df.to_csv(path + "cow_comp" + str(cont) + ".csv") #Se usa el DataFrame y se guarda como el csv final
        cont = cont + 1
 #monitor
plt.subplot(221)
plt.imshow(resized_img)
plt.title('original')
 
plt.subplot(222)
plt.imshow(img_dct_log)
plt.title('dct transformed')
 
plt.subplot(223)
plt.imshow(img_recor)
plt.title('idct transformed')
 
plt.subplot(224)
plt.imshow(img_recor1)
plt.title('idct transformed2')
 
plt.show()
