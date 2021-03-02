#Planteamiento del proyecto:

'''
	Realiar un programa que extraiga los resultados de la pagina 'loteriadehoy.com', para su posterior analisis.

'''

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def guardar(data_f):

	print(' ')
	print('¿Desea guardar el marco de datos?')
	r = int(input('Sí (1) | No (2): '))
	print(' ')

	while (r != 1) and (r != 2):

		print('.:DATOS INVALIDO:.')
		r = int(input('Sí (1) | No (2): '))
		print(' ')

	if (r == 1):

		print('¿En que formato desea guardar el marco de datos?')
		print('1. CSV')
		print('2. XLSX')
		r1 = int(input('1 o 2: '))
		print(' ')

		while (r1 != 1) and (r1 != 2):

			print('.:DATOS INVALIDO:.')
			r1 = int(input('1 o 2: '))
			print(' ')

		if (r1 == 1):

			print('Ingrese el directorio junto al nombre con el que guardara el archivo.')
			print('Recuerde colocarle la extension al nombre del archivo ("nombre.csv")')
			direc1 = input('Directorio: ')
			data_f.to_csv(direc1)
			print(' ')
			print('¡Su marco de datos a sido guardado!')
			print(' ')

		if (r1 == 2):

			print('Ingrese el directorio junto al nombre con el que guardara el archivo.')
			print('Recuerde colocarle la extension al nombre del archivo ("nombre.xlsx")')
			direc2 = input('Directorio: ')
			data_f.to_excel(direc2)
			print(' ')
			print('¡Su marco de datos a sido guardado!')
			print(' ')

	elif (r == 2):

		print('No se guarda el marco de datos')
		print(' ')

	return '¡LISTO!'


def incremento(d, m, a):

	d = int(d)
	m = int(m)
	a = int(a)

	d += 1

	if (a % 4 == 0) and (not(a % 100 == 0) or (a % 400 == 0)):

	 	if (m == 2) and (d > 29): 
	 		
	 		d = 1
	 		m = 3

	elif (m == 2) and (d > 28):

	 	d = 1
	 	m = 3

	if (((m == 1) or (m == 3) or (m == 5) or (m == 7) or (m == 8) or (m == 10)) and (d > 31)):

		d = 1
		m += 1

	if (m == 12) and (d > 31):

		d = 1
		m = 1
		a += 1


	if (((m == 4) or (m == 6) or (m == 9) or (m == 11)) and (d > 30)):

		d = 1
		m += 1

	d = str(d)
	m = str(m)
	a = str(a)

	return d, m, a


#Antes de todo, hagamos que el usuario, ingrese y le haga saber al programa, de que rango de fechas desea extraer los datos.
#Que resultados de que dias desea conocer basicamente, para esto no pediremos la fecha en ningun formato para no hacer...
#... que el programa sea complejo, lo que haremos es pedir dato por dato.
print(' ')
print('Ingrese el rango de fechas las cuales desea tomar:')
print(' ')
print('FECHA INICIAL: ')
dia_i = input('Dia: ')
mes_i = input('Mes: ')
año_i = input('Año: ')
print(' ')
print('FECHA FINAL: ')
dia_f = input('Dia: ')
mes_f = input('Mes: ')
año_f = input('Año: ')
print(' ')

#Ahora si, pasemos a la parte de extraer los datos, tenemos que trabajar segun los datos de las fechas proporcionadas...
#... por el usuario.

#1. Veamos la forma de un URL cualquiera de la pagina 'loteriadehoy.com':
# https://www.loteriadehoy.com/animalito/lottoactivo/resultados/2021-01-24/

#Basicamente la forma GENERAL del enlace pasa a ser el mismo de arriba, con la diferencia de que claramente la fecha va a...
#... variar segun el dia el cual queramos ver el resultado. En base a esto, definamos una direccion web general:
url_gen = 'https://www.loteriadehoy.com/animalito/lottoactivo/resultados/'


#Pasemos ahora a trabajar con los datos proporcinados por el usuario, basicamente vamos repetir una cantidad indeterminada...
#... de acciones hasta que se recorra desde el dia inicial hasta el dia final y se recopilen dia por dia todos los datos:

#Para esto inicialicemos las variables que iran aumentando a medida el bucle se vaya repitiendo:
año = año_i
mes = mes_i
dia = dia_i

#Consideremos el siguiente diccionario en el cual guardaremos nuestros numeros los cuales vayamos recopilando:
dicc_pre_df= {}

#Crearemo una lista, la cual tendra un nombre caracteristo para reconocerla mas adelante ya que la usaremos para graficar:
lista_con_nombre_caracteristico_xd = []
#En esta lista con nombre caracteristico apilaremos todos los numeros obtenidos de la pagina en datos enteros.

while True:

	#Una vez aqui, el URL generico pasara a ser un poco mas especifico ya que estos contendran las fechas:
	#Vease que en la forma de los url de 'loteriadehoy.com', las fechas se encuentran en el formato 'AAAA-MM-DD'.
	
	#Ademas tambien hay que tener presente que cuando los numeros son de digitos individuales, estos esten acompañados...
	#... con un cero a la izquierda.

	#Vamos a contruir una condicion para curar este mal:

	año = int(año)
	mes = int(mes)
	dia = int(dia)


	if (dia >= 10) and (mes >= 10):

		dia = str(dia)
		mes = str(mes)
		año = str(año)
		url = url_gen + año + '-' + mes + '-' + dia + '/'

	elif (dia < 10) and (mes < 10):

		dia = str(dia)
		mes = str(mes)
		año = str(año)
		url = url_gen + año + '-' + '0' + mes + '-' + '0' + dia + '/'

	elif (dia < 10):

		dia = str(dia)
		mes = str(mes)
		año = str(año)
		url = url_gen + año + '-' + mes + '-' + '0' + dia + '/'

	elif (mes < 10):

		dia = str(dia)
		mes = str(mes)
		año = str(año)
		url = url_gen + año + '-' + '0' + mes + '-' + dia + '/'

	print(url)

	#Ahora pasemos a importar todo el HTML de la pagina hacia Python:
	html = urllib.request.urlopen(url).read()

	#Creemos un objeto de tipo 'BeautifulSoup' con todo nuestro HTML como parametro:
	soup = BeautifulSoup(html, 'html.parser')

	#Como siguiente paso, vamos a indicar que queremos exactamente extraer de dicho HTML, y bueno, despues de inspeccionar...
	#... el elemento en mi navegador web, llegue a la conclusion de que los datos que queremos extraer estan todos dentro...
	#... de etiquetas 'img', por lo tanto esas seran las etiquetas que usaremos.
	etiquetas = soup('img')
	#Por defecto, el objeto 'BeautifulSoup' crea una lista y almacena las etiquetas ahi.

	#Consideremos una lista que reinicie sus valores luego de cada repeticion del bucle:
	lista_to_append = []

	if (len(etiquetas) > 8):
		if len(etiquetas) > 9 :
			if (etiquetas != []):
				for e in etiquetas:

					#Pasamos la codificacion de los archivos de UTF-8 a una que Python pueda leer:
					x = e.decode()

					if re.search('[0-9]+',x):
						#Efectuemos la busqueda de los numeros dentro de cada etiquera 'img', haciendo uso de una expresion regular:
						lista_to_append.append(re.findall('[0-9]+', x)[0])

						if (re.findall('[0-9]+', x)[0] == '00'):
							lista_con_nombre_caracteristico_xd.append(37)

						else:
							lista_con_nombre_caracteristico_xd.append(int(re.findall('[0-9]+', x)[0]))

					else:
						lista_to_append.append('101')

			else:
				for i in range(10):
					lista_to_append.append('400')
		

		else :
			#Aqui todo lo de 9 Horarios
			if (etiquetas != []):
				lista_to_append.append('101')
				for e in etiquetas:
					x = e.decode()
					if re.search('[0-9]+',x):
						lista_to_append.append(re.findall('[0-9]+', x)[0])

						if (re.findall('[0-9]+', x)[0] == '00'):
							lista_con_nombre_caracteristico_xd.append(37)
						else :
							lista_con_nombre_caracteristico_xd.append(int(re.findall('[0-9]+', x)[0]))
					else :
						lista_to_append.append('101')
			else:
				for i in range(10):
					lista_to_append.append('400')

	
	else:
		#Aqui todo lo de 8 horarios
		if (etiquetas != []):
			lista_to_append.append('101')

			for e in etiquetas:
				#Pasamos la codificacion de los archivos de UTF-8 a una que Python pueda leer:
				x = e.decode()

				if re.search('[0-9]+',x):
					#Efectuemos la busqueda de los numeros dentro de cada etiquera 'img', haciendo uso de una expresion regular:
					lista_to_append.append(re.findall('[0-9]+', x)[0])

					if (len(lista_to_append) == 5):
						lista_to_append.append('101')

					if (re.findall('[0-9]+', x)[0] == '00'):
						lista_con_nombre_caracteristico_xd.append(37)

					else:
						lista_con_nombre_caracteristico_xd.append(int(re.findall('[0-9]+', x)[0]))

				else:
					lista_to_append.append('101')

					if (len(lista_to_append) == 5):
						lista_to_append.append('101')

		else:
			for i in range(10):
				lista_to_append.append('400')


	#Ahora pasemos a guardar todo esto dentro del diccionario que fue creado fuera del bucle ('dicc_pre_df')...
	#... recordemos que la lista se reinicia con cada iteracion del ciclo, y tambien que la etiqueta de cada...
	#... columna sera la fecha.
	fecha = dia + '/' + mes + '/' + año
	dicc_pre_df[fecha] = lista_to_append
	

	#Pasemos a colocar la condicion de salida del bucle, ya que es algo esencial:
	if (dia == dia_f) and (mes == mes_f) and (año == año_f):
		break


	#Ahora tenemos el ligero y solucionable problema de que necesitamos una forma de que incremente el dia y a medida de que...
	#... el dia va incrementando, los meses y los años tambien lo haran. Para esta tarea creamos una funcion incremento:
	incre = incremento(dia, mes, año)
	dia = incre[0]
	mes = incre[1]
	año = incre[2]


#Pasemos el diccionario que contiene toda la informacion extraida ('dicc_pre_df') a un marco de datos 'df' para facilitar...
#... la lectura de los datos extraidos. Adicionalmente se agregara una lista que contenera todos indices de cada una de las...
#... filas.
df = pd.DataFrame(dicc_pre_df, index=['09AM', '10AM','11AM', '12PM', '01PM', '03PM', '04PM', '05PM', '06PM', '07PM'])
print(df.head(10))

#Se creo una funcion para guardas los marcos de datos a medida se vaya avanzando en el programa, luego se ira trabajando...
#... mas y mas con los DataFrames, pero quizas un usuario quiera almacenar los datos en un punto en especifico.

#Ahora, para que el usuario sepa hasta que punto esta el marco de datos, debemos decirselo antes.
print(' ')
print(' ')
print('De guardar el marco de datos, debe antes tener presente los siguientes puntos:')
print('Todos los datos son de tipo "str"')
print('"101": Horarios sin sorteos.')
print('"400": Dias sin sorteos.')
guardar(df)


#Pasemos a hacer un trabajito mas para poder hacer graficas de estos datos y es pasalos...
#... a datos de tipo 'int', aqui hay que evaluar el siguiente problema, y es que los datos recopilados son todos numeros...
#... del 1 al 36 incluyendo el 0 y el 00. Si pasamos esos datos a datos enteros tendremos que el 0 y 00 se confundiran...
#... asi que tomemos como generalidad que el 00 pasara a ser 37:
df = df. replace('00', '37')
#print(df.head(10))

#Previamente evaluamos el DataFrame para conocer los tipos de datos:
#print(' ')
#print(df.dtypes)

#Ahora si podemos pasar el marco de datos a tipo dato 'int'.
df = df.astype('int')

#Pasemos a limpieza de los datos de un marco de datos, en este caso, los datos que se limpiaran...
#... seran aquellos los cuales son '400' o '101', claramente estos datos (a los cuales podemos llamarles vacios), los vamos...
#... a reemplazar por 'NaN' (No a Number), perteneciente a la libreria NumPy.
df = df.replace(400, np.nan)
df = df.replace(101, np.nan)

#Si volvemos a evaluar veremos que los tipos de datos han cambiado.
#print(' ')
#print(df.head(10))
#print(' ')
#print(df.dtypes)


#Hasta este momento tambien podemos preguntarle al usuario si desea guardar el marco de datos.

#Ahora, para que el usuario sepa hasta que punto esta el marco de datos, debemos decirselo antes.
print(' ')
print(' ')
print('De guardar el marco de datos, debe antes tener presente los siguientes puntos:')
print('Todos los datos NO vacios son de tipo "int"')
print('"00": fue cambiado por el numero 37.')
print('"NaN": Son datos vacios.')
guardar(df)


#print(lista_con_nombre_caracteristico_xd)
#print(len(lista_con_nombre_caracteristico_xd))


#Hagamos un histograma donde veamos que tanto a salido un numero en un rango de tiempo determinado:

#Establecemos el rango de valores existentes en los datos...
rang = range(0, 37+2)

#... tambien los valores que estaran en el eje X, que seran los valores que la tabla posee, como ya sabemos son numeros...
#... del 0 al 37, por lo tanto podemos colocar todos los valores en una lista con nombre caracteristico, la cual ya...
#... contiene todo.
Xrang = lista_con_nombre_caracteristico_xd

plt.hist(x=Xrang, bins=rang, color='#008080', rwidth=0.85)
plt.title('Veces que ha salido un numero.')
plt.xlabel('Numeros')
plt.ylabel('Veces que salio')
plt.xticks(rang)
plt.show()


