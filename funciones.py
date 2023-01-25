
import PyPDF2
from icalendar import Calendar, Event
from datetime import date
import pytz


def dividir_en_categorias(txt):

    dias = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    #print(txt)

    bits = txt.split(" ")
    if "2022" in bits[1].split("-"):
        bits[1] = bits[1][0:7] + "22"

    bits2 = []
    bits2.append(" ".join(bits[0:2]))
    if bits[2] in dias:
        bits2.append(" ".join(bits[2:4]))
        if bits[4:5] == "Comunidad": 
            bits2.append(" ".join(bits[4:6]))
            bits2.append(" ".join(bits[6:]))
        elif " ".join(bits[4:6]) == "Estudiante Nuevo":
            bits2.append(" ".join(bits[4:6]))
            bits2.append(" ".join(bits[6:]))
        elif " ".join(bits[4:6]) == "Estudiante College":
            bits2.append(" ".join(bits[4:6]))
            bits2.append(" ".join(bits[6:]))
        elif " ".join(bits[4:6]) == "Estudiante de":
            bits2.append(" ".join(bits[4:10]))
            bits2.append(" ".join(bits[10:]))
        else:
            bits2.append(" ".join(bits[4:5]))
            bits2.append(" ".join(bits[5:]))

    else:
        if bits[2] == "Comunidad": 
            bits2.append(" ".join(bits[2:4]))
            bits2.append(" ".join(bits[4:]))
        elif " ".join(bits[2:4]) == "Estudiante Nuevo":
            bits2.append(" ".join(bits[2:4]))
            bits2.append(" ".join(bits[4:]))
        elif " ".join(bits[2:4]) == "Estudiante College":
            bits2.append(" ".join(bits[2:4]))
            bits2.append(" ".join(bits[4:]))
        elif " ".join(bits[2:4]) == "Estudiante de":
            bits2.append(" ".join(bits[2:8]))
            bits2.append(" ".join(bits[8:]))
        else:
            bits2.append(bits[2])
            bits2.append(" ".join(bits[3:]))

    #print(bits2)
    return bits2


def corregir_lineas(txt):
    #print(txt)
    txt = " ".join(txt)
    #print(txt)
    #old:
    #Cuando se lee el pdf, se genera una línea por cada elemento de
    #una fila en el archivo pdf. Lo que hace esta función es 
    #generar una lista que contiene las filas del archivo pdf

    #new:
    #al parecer ya genera una lista. Lo que va a pasar ahora es limpiar las líneas
    #Pasar de "FacultadUnidades Académicas no se cuanto" => "Facultad Unidades académicas no se cuanto"

    posiciones = []
    posicion = 0
    
    #Se marcan las líneas que parten por una fecha
    for i in range(len(txt)):
        if txt[i:i+4] in ["lun ", "mar ", "mié ", "jue ", "vie ", "sáb ", "dom "]:
            if txt[i+4].isdigit():
                posiciones.append(posicion)
        posicion += 1
    
    
    #Si en las posiciones se tiene algo del estilo [..., 5, 6, ...]
    #significa que el 6 corresponde a la fecha de término del evento
    #entonces se elimina el 6
    for i in posiciones:
        if i < int(posiciones[-1]):
            if i+12 == posiciones[posiciones.index(i)+1]:
                posiciones.remove(i+12)
            elif i+13 ==posiciones[posiciones.index(i)+1]:
                posiciones.remove(i+13)
            elif i+14 ==posiciones[posiciones.index(i)+1]:
                posiciones.remove(i+14)
            elif i+15 ==posiciones[posiciones.index(i)+1]:
                posiciones.remove(i+15)




    
    eventos = []

    #se genera una lista con cada línea en el pdf
    for i in posiciones:
        if i < posiciones[-1]:
           eventos.append(txt[i:posiciones[posiciones.index(i) + 1]])

    for i in range(len(eventos)):
        print(eventos[i])
        bits = eventos[i].split(" ")
        n_uppercase = []
        for j in range(len(bits)):
            for k in range(len(bits[j][1:])):
                if bits[j][1:][k].isupper():
                    if bits[j][k].islower() or bits[j][k].isdigit() or bits[j][k] == "C" or bits[j][k] == ")":
                        bits[j] = bits[j][0:k+1] + " " +bits[j][k+1:]
        eventos[i] = " ".join(bits).strip(" ")



        eventos[i] = dividir_en_categorias(eventos[i])

                       
    print("-----------eventos------------")
    #print(eventos)
    return eventos

def calibrar_fecha(txt):
    #print(txt)
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
#    print(eventos)
    for date in eventos:
#        print(date)
        descripcion = ""
        if date[1][0:3] in ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]:
            #En las líneas de Estudiante de Intercambio UC se generan
            #dos strings separados, esto lo corrige

#            #debug
#            print(date)
#            print("----------")
#            print("----------")
#            print(date[0])
#            print(date==eventos[0])
#            print("----------")
#            #debug

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
                #print(fin)
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
    fileReader = PyPDF2.PdfReader(calendario)
#    print(fileReader)
    
    calendario_nice = []
    
    for i in range(0,len(fileReader.pages)):
        pagina = fileReader.pages[i]
        crudo = pagina.extract_text().split("\n")
        eventos_obtenidos = corregir_lineas(crudo)
        eventos_obtenidos = ordenar_eventos(eventos_obtenidos)
        calendario_nice.extend(eventos_obtenidos)
        print(f"Se exportó la página {i+1}")
    return(calendario_nice)



