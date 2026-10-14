"""Ejemplos de conjuntos: valores únicos y operaciones entre grupos."""

emails = {"ana@x.com", "luis@x.com"}
emails.add("sol@x.com")
emails.add("ana@x.com")
emails.discard("luis@x.com")
print("Emails registrados:", sorted(emails))

if "ana@x.com" in emails:
    print("Ese email ya está registrado")

ciudades = ["Guayaquil", "Quito", "Guayaquil", "Milagro", "Quito"]
unicas = set(ciudades)
print(len(unicas), "ciudades distintas")
lista_unica = sorted(unicas)
print("Ciudades ordenadas sin repetir:", lista_unica)

matematica = {"Ana", "Luis", "Sol"}
ingles = {"Luis", "Marco"}
print("Unión:", matematica | ingles)
print("Intersección:", matematica & ingles)
print("Diferencia:", matematica - ingles)
print("Diferencia simétrica:", matematica ^ ingles)
print("¿Ana está en Matemática?:", {"Ana"}.issubset(matematica))
print("¿Pedro no comparte alumnos?:", matematica.isdisjoint({"Pedro"}))
