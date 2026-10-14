"""Ejemplos de tuplas: campos fijos, retornos y claves compuestas."""

CAMPOS_CLIENTE = ("nombre", "apellido", "email", "telefono", "direccion")

print("Cantidad de campos:", len(CAMPOS_CLIENTE))
print("Primer campo:", CAMPOS_CLIENTE[0])
print("¿Hay campo email?:", "email" in CAMPOS_CLIENTE)


def crear_cliente(nombre):
    if not nombre:
        return (False, "El nombre es obligatorio")
    return (True, "Cliente creado")


exito, mensaje = crear_cliente("Ana")
print("Resultado:", exito, mensaje)

campos = ("nombre", "email")
valores = ("Ana", "ana@x.com")
for campo, valor in zip(campos, valores):
    print(f"{campo}: {valor}")

a, b = 1, 2
a, b = b, a
print("Valores intercambiados:", a, b)

ventas = {("2026", "enero"): 1500, ("2026", "febrero"): 1800}
print("Ventas de enero:", ventas[("2026", "enero")])
