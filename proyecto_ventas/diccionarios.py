"""Ejemplos de diccionarios: campos de un registro e índices por clave."""

cliente = {"id": 1, "nombre": "Ana", "email": "ana@x.com"}

print("Nombre:", cliente["nombre"])
print("Teléfono:", cliente.get("telefono", "sin dato"))

cliente["telefono"] = "0987654321"
cliente.update({"ciudad": "Guayaquil"})
del cliente["ciudad"]
telefono = cliente.pop("telefono", None)
print("Teléfono retirado:", telefono)

for clave in cliente:
    print("Clave:", clave)
for valor in cliente.values():
    print("Valor:", valor)
for clave, valor in cliente.items():
    print(f"{clave} = {valor}")

print("¿Hay clave email?:", "email" in cliente)
print("Número de campos:", len(cliente))

notas = {"Matemática": [18, 19], "Inglés": [17]}
notas.setdefault("Historia", []).append(20)
print("Notas:", notas)

clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
indice = {registro["id"]: registro["nombre"] for registro in clientes}
print("Cliente con id 2:", indice[2])
