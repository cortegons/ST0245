import os
import csv  

path1 = "C:/Users/Camilo Ortegon/Desktop/sanos_csv"
path2 = "C:/Users/Camilo Ortegon/Desktop/enfermos_csv"

sanos = os.listdir(path1)
enfermos = os.listdir(path2)

matrizSanos = []
matrizEnfermos = []

for i in sanos:
    with open(str(path1 + "/" + i), 'r') as data:
        entrada = csv.reader(data)
        lista1 = list(entrada)

    arreglo1 = []
    for line in lista1:
         arreglo1.append(line)
    matrizSanos.append(arreglo1)
print(matrizSanos)

for j in enfermos:
    with open(str(path2 + "/" + j), 'r') as data:
        entrada = csv.reader(data)
        lista2 = list(entrada)

    arreglo2 = []
    for line in lista2:
         arreglo2.append(line)
    matrizSanos.append(arreglo2)
print(matrizEnfermos)