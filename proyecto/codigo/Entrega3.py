import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from PIL import Image
import pandas as pd
import string
import sys
from sys import argv
from struct import *
import time
import memory_profiler

path = input("Ingrese la ruta de carpeta ")
path = path.replace('\'', '/')
carpeta = os.listdir(path)
cont = 0

start = time.process_time()
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
        tiimee = time.process_time()
        # taking the input file and the number of bits from command line
        # defining the maximum table size
        # opening the input file
        # reading the input file and storing the file data into data variable
        input_file  = path + "cow_comp" + str(cont) + ".csv"
        maximum_table_size = pow(2,500)      
        file = open(input_file)                 
        data = file.read()                      

        # Building and initializing the dictionary.
        dictionary_size = 256                   
        dictionary = {chr(i): i for i in range(dictionary_size)}    
        string = ""             # String is null.
        compressed_data = []    # variable to store the compressed data.

        # iterating through the input symbols.
        # LZW Compression algorithm
        for symbol in data:                     
            string_plus_symbol = string + symbol # get input symbol.
            if string_plus_symbol in dictionary: 
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if(len(dictionary) <= maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            compressed_data.append(dictionary[string])

        # storing the compressed string into a file (byte-wise).
        out = input_file.split(".")[0]
        output_file = open(out + ".lzw", "wb")
        for data in compressed_data:
             output_file.write(pack('>I',int(data)))
            
        output_file.close()
        file.close()
        elapsed1 = time.process_time() - tiimee
        
        print(elapsed1)
        
        cont = cont + 1
        
elapsed2 = time.process_time() - start
print( "tiempo = " + str(elapsed2))


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
 
#plt.show()

aei = memory_profiler.memory_usage()
print(aei)


