"""Ejemplos de conversión entre las colecciones de Python."""

datos = ["a", "b", "a", "c"]

print("Lista:", list(datos))
print("Tupla:", tuple(datos))
print("Conjunto:", set(datos))
print("Valores únicos ordenados:", sorted(set(datos)))

cliente = dict(zip(("id", "nombre"), (1, "Ana")))
print("Diccionario construido con zip:", cliente)
print("Pares del diccionario:", list({"id": 1, "nombre": "Ana"}.items()))
