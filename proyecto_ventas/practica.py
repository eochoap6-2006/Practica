"""Ejercicios 1 al 10 de la sección 15 de la guía.

Ejecutar desde proyecto_ventas con: python practica.py
"""

from tempfile import TemporaryDirectory

from models import Cliente, Producto, Proveedor, Venta
from views import ClienteController


def ejercicio_1():
    ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
    vistas = set()  # El conjunto recuerda qué nombres ya aparecieron.
    unicas = []     # La lista conserva el orden de aparición.
    for ciudad in ciudades:
        if ciudad not in vistas:
            vistas.add(ciudad)
            unicas.append(ciudad)
    return unicas


def ejercicio_2():
    ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
    conteo = {}
    for ciudad in ciudades:
        conteo[ciudad] = conteo.get(ciudad, 0) + 1
    mas_repetidas = [ciudad for ciudad, veces in conteo.items()
                     if veces == max(conteo.values())]
    return conteo, mas_repetidas


def ejercicio_3():
    inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
    inscritos_ingles = {"Luis", "Marco", "Ruth"}
    ambas = inscritos_matematica & inscritos_ingles
    solo_mate = inscritos_matematica - inscritos_ingles
    total = len(inscritos_matematica | inscritos_ingles)
    return sorted(ambas), sorted(solo_mate), total


def ejercicio_4():
    clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
    indice = {cliente["id"]: cliente for cliente in clientes}
    return indice[2]["nombre"]


def ejercicio_5():
    ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
    total = sum(monto for _mes, monto in ventas)
    mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])
    return total, mejor_mes, mejor_monto


def ejercicio_6():
    # clientes_por_ciudad() también se encuentra en el menú Clientes, opción 8.
    with TemporaryDirectory() as carpeta:
        controlador = ClienteController(f"{carpeta}/clientes.json")
        for nombre, ciudad in (("Ana", "Guayaquil"), ("Luis", "Guayaquil"),
                               ("Sol", "Quito")):
            controlador.crear({
                "nombre": nombre, "apellido": "Ejemplo",
                "email": f"{nombre.lower()}@example.com", "ciudad": ciudad,
            })
        return controlador.clientes_por_ciudad()


def ejercicio_7():
    # Clasificación según los datos que necesita cada método.
    return {
        "calcular_total": "instancia: usa la cantidad y el precio de una venta",
        "desde_diccionario": "clase: crea un objeto usando cls",
        "es_precio_valido": "estático: valida un número sin un producto",
        "stock_bajo": "instancia: usa el stock de un producto",
        "con_iva": "estático: recibe un monto y devuelve otro",
    }


def ejercicio_8():
    # Proveedor hereda de Persona; también hereda desde_diccionario() y __str__().
    proveedor = Proveedor.desde_diccionario({
        "id": 1, "nombre": "Luis", "apellido": "Mora",
        "email": "luis@x.com", "ruc": "0912345678001",
        "empresa": "Importadora Sur",
    })
    return str(proveedor)


def describir(objeto):
    # Ejercicio 9: la etiqueta cambia según el objeto, sin comprobar su tipo.
    return objeto.etiqueta()


def ejercicio_9():
    objetos = [
        Cliente(1, "Ana", "Pérez", "ana@x.com", ciudad="Guayaquil"),
        Producto(1, "Teclado", 25.50, 15),
        Venta(1, 1, 1, 2, 25.50, fecha="2026-10-14"),
        Proveedor(2, "Luis", "Mora", "luis@x.com", empresa="Importadora Sur"),
    ]
    return [describir(objeto) for objeto in objetos]


def ejercicio_10():
    # Con 12 unidades se aplica el descuento; con menos se conserva el precio.
    return Producto.precio_mayorista(25.50, 2), Producto.precio_mayorista(25.50, 12)


if __name__ == "__main__":
    for numero in range(1, 11):
        resultado = globals()[f"ejercicio_{numero}"]()
        print(f"Ejercicio {numero}: {resultado}")
