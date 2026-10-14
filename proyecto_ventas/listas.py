"""Ejemplos de listas: agregar, quitar, consultar y transformar datos."""

clientes = ["Ana", "Luis", "Sol"]

# Agregar
clientes.append("Marco")
clientes.insert(1, "Beto")
clientes.extend(["Iván", "Ruth"])
print("Después de agregar:", clientes)

# Quitar
clientes.remove("Beto")
ultimo = clientes.pop()
primero = clientes.pop(0)
print("Salieron:", primero, "y", ultimo)
print("Lista actual:", clientes)

# Consultar
print("Cantidad:", len(clientes))
print("Primero y último:", clientes[0], clientes[-1])
print("¿Está Ana?:", "Ana" in clientes)
print("Posición de Sol:", clientes.index("Sol"))
print("Veces que aparece Ana:", clientes.count("Ana"))

# Recorrer
for nombre in clientes:
    print("Cliente:", nombre)

for posicion, nombre in enumerate(clientes):
    print("Posición:", posicion, "Nombre:", nombre)

# Ordenar
copia_ordenada = sorted(clientes)
print("Copia ordenada:", copia_ordenada)
clientes.sort()
print("Lista ordenada:", clientes)
clientes.sort(reverse=True)
print("Orden inverso:", clientes)

# Transformar y filtrar con comprensiones
mayusculas = [nombre.upper() for nombre in clientes]
con_a = [nombre for nombre in clientes if nombre.startswith("A")]
longitudes = [len(nombre) for nombre in clientes]
print("Mayúsculas:", mayusculas)
print("Nombres con A:", con_a)
print("Longitudes:", longitudes)

# Acumular
notas = [18, 15, 20, 12]
print("Suma, máximo, mínimo y promedio:", sum(notas), max(notas), min(notas), sum(notas) / len(notas))
