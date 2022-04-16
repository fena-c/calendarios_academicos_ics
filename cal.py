from funciones import separar_por_lineas, ordenar_eventos, calibrar_fecha, lista_comunidad, generar_calendario_completo, generar_calendario_simple, traducir_pdf
import os

#Se abre el pdf

archivos_disponibles = os.listdir()
archivos_pdf = []
for archivo in archivos_disponibles:
    if archivo.endswith(".pdf"):
        archivos_pdf.append(archivo)



print("""Hola buenas

Con esta herramienta vas a poder generar un .ics a partir del
calendario académico en .pdf

Se van a mostrar los archivos pdf encontrados en el directorio, elige
el calendario académico.
""")

if len(archivos_pdf) == 0:
    print("\n No se encontró un archivo pdf :(, coloca el pdf del calendario"
            " académico en la misma dirección que este programa")
    exit()

for candidato in archivos_pdf:
    i = 1
    print(f"[{i}] {candidato}")
    i += 1

numero_pdf = input("\nSelecciona el número del archivo: ")


try:
    archivo_pdf = archivos_pdf[int(numero_pdf) - 1]
    calendario = open(archivo_pdf, 'rb')
except:
    print("\nERROR: Se ingresó un número no válido :(")
    print("Cerrando el programa")
    exit()

lineas_traducidas = traducir_pdf(calendario)
#Parte el calendario iCal


print("""Se pueden generar dos tipos de calendarios:

[1] Por cada línea en el calendario académico, generar un solo evento
con fecha de inicio hasta la fecha de término.

[2] Por cada línea en el calendario académico, generar dos eventos distintos,
uno que de comienzo al evento, y otro que marque el final.
""")
opcion_calendario = input("Escribe la opción que te gustaría generar: ")

if opcion_calendario == "1":
    lista_calendarios = generar_calendario_completo(lineas_traducidas)
elif opcion_calendario == "2":
    lista_calendarios = generar_calendario_simple(lineas_traducidas)
else:
    print("\nERROR: Se eligió una opción inválida :(")
    exit()



lista_calendarios = generar_calendario_completo(lineas_traducidas)


for calendario in lista_calendarios:
    f = open(f"{calendario}.ics", "wb")
    f.write(lista_calendarios[calendario].to_ical())
    print(f"escrito {calendario}.ics")
    f.close()

print("\nSe generaron todos los calendarios, los puedes encontrar en la misma"
        " dirección donde se ubica el programa")


