
import PyPDF2
from icalendar import Calendar, Event
from datetime import date
import pytz
def separar_por_lineas(txt):
    #Cuando se lee el pdf, se genera una línea por cada elemento de
    #una fila en el archivo pdf. Lo que hace esta función es 
    #generar una lista que contiene las filas del archivo pdf

    posiciones = []
    posicion = 0
    
    #Se marcan las líneas que parten por una fecha
    for i in txt:
        if i[0:3] in ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]:
            posiciones.append(posicion)
        posicion += 1
    
    #Si en las posiciones se tiene algo del estilo [..., 5, 6, ...]
    #significa que el 6 corresponde a la fecha de término del evento
    #entonces se elimina el 6
    for i in posiciones:
        if i < int(posiciones[-1]):
            if i+1 == posiciones[posiciones.index(i)+1]:
                posiciones.remove(i+1)
    
    eventos = []

    #se genera una lista con cada línea en el pdf
    for i in posiciones:
        if i < posiciones[-1]:
           eventos.append(txt[i:posiciones[posiciones.index(i) + 1]])

    return eventos

def calibrar_fecha(txt):
    #pasar de 'lun 3-ene-22' a '2022 1 3'
    meses = [("ene", 1),
            ("feb", 2),
            ("mar", 3),
            ("abr", 4),
            ("may", 5),
            ("jun", 6),
            ("jul", 7),
            ("ago", 8),
            ("sept", 9),
            ("oct", 10),
            ("nov", 11),
            ("dic", 12),
            ]
    fecha = txt[4:]
    fecha = fecha.split("-")

    for mes in meses:
        if fecha[1] == mes[0]:
            mm=mes[1]

    if len(fecha[2]) == 4:
        yy = fecha[2][-2:]
    else:
        yy = "20" + fecha[2]

    dd = fecha[0]
    return [yy,mm,dd]




def ordenar_eventos(eventos):
    #traducir las líneas de texto a un formato de:
    #Fecha de inicio:
    #Fecha de Término:
    #Descripción:
    #Comunidad:
    ordenados = []
    for date in eventos:
#        print(date)
        descripcion = ""
        if date[1][0:3] in ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]:
            #En las líneas de Estudiante de Intercambio UC se generan
            #dos strings separados, esto lo corrige
            if date[2] == "Estudiante de ": 
                comunidad = date[2] + date[3]

                for texto in date[4:]:
                    descripcion += texto
            else:
                comunidad = date[2]
                for texto in date[3:]:
                    descripcion += texto

            inicio = calibrar_fecha(date[0])
            fin = calibrar_fecha(date[1])
            about = descripcion
            corregido = {
                    "inicio": inicio,
                    "fin": fin,
                    "comunidad": comunidad,
                    "descripcion": about}
            ordenados.append(corregido)
        else:
            #En las líneas de Estudiante de Intercambio UC se generan
            #dos strings separados, esto lo corrige
            if date[1] == "Estudiante de ":
                comunidad = date[1] + date[2]

                for texto in date[3:]:
                    descripcion += texto
            else:
                comunidad = date[1]
                for texto in date[2:]:
                    descripcion += texto

            inicio = calibrar_fecha(date[0])
            about = descripcion
            corregido = {
                    "inicio": inicio,
                    "comunidad": comunidad,
                    "descripcion": about}
            ordenados.append(corregido)
    return ordenados


def lista_comunidad(calendario):
    lista = []
    for evento in calendario:
        if evento["comunidad"] not in lista:
            lista.append(evento["comunidad"])
    return lista




def generar_calendario_simple(calendar):
    comunidades = lista_comunidad(calendar)

    lista_calendarios = {}
    for colectivo in comunidades:
        calendario_de = f"calendario_{colectivo}"
        calendario_python = Calendar()
    
        for evento in calendar:
            if evento["comunidad"] != colectivo:
                continue
            if len(evento) == 4:
                carrito_inicio = Event()
                carrito_fin = Event()
    
                inicio = evento["inicio"]
                fin = evento["fin"]
                summary = evento["descripcion"]
    
                carrito_inicio.add("dtstart", date(int(inicio[0]), int(inicio[1]), int(inicio[2])))
                carrito_inicio.add("summary", summary + " (inicio)")
    
                carrito_fin.add("dtstart", date(int(fin[0]), int(fin[1]), int(fin[2])))
                carrito_fin.add("summary", summary + " (término)")
    
                calendario_python.add_component(carrito_inicio)
                calendario_python.add_component(carrito_fin)
            else:
                carrito = Event()
                inicio = evento["inicio"]
                summary = evento["descripcion"]
    
                carrito.add("dtstart", date(int(inicio[0]), int(inicio[1]),int(inicio[2])))
                carrito.add("summary", summary)
                calendario_python.add_component(carrito)
    
        lista_calendarios[calendario_de] = calendario_python
    return lista_calendarios

def generar_calendario_completo(calendar):
    comunidades = lista_comunidad(calendar)

    lista_calendarios = {}
    for colectivo in comunidades:
        calendario_de = f"calendario_{colectivo}"
        calendario_python = Calendar()
    
        for evento in calendar:
            if evento["comunidad"] != colectivo:
                continue
            carrito = Event()
            if len(evento) == 4:
                inicio = evento["inicio"]
                fin = evento["fin"]
                summary = evento["descripcion"]
    
                carrito.add("dtstart", date(int(inicio[0]), int(inicio[1]), int(inicio[2])))
                carrito.add("dtend", date(int(fin[0]), int(fin[1]), int(fin[2])))
                carrito.add("summary", summary)
                calendario_python.add_component(carrito)
            else:
                inicio = evento["inicio"]
                summary = evento["descripcion"]
    
                carrito.add("dtstart", date(int(inicio[0]), int(inicio[1]),int(inicio[2])))
                carrito.add("summary", summary)
                calendario_python.add_component(carrito)
    
        lista_calendarios[calendario_de] = calendario_python
    return lista_calendarios

def traducir_pdf(calendario):
    fileReader = PyPDF2.PdfFileReader(calendario)
    
    calendario_nice = []
    
    print(fileReader.numPages)
    for i in range(0,fileReader.numPages):
        pagina = fileReader.getPage(i)
        crudo = pagina.extractText().split("\n")
        eventos_obtenidos = separar_por_lineas(crudo)
        eventos_obtenidos = ordenar_eventos(eventos_obtenidos)
        calendario_nice.extend(eventos_obtenidos)
        print(f"Se exportó la página {i+1}")
    return(calendario_nice)



