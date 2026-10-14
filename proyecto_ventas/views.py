from abc import ABC, abstractmethod

from models import Cliente, Producto, Venta, Devolucion
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# =====================================================================
# CLASE BASE (ABSTRACTA)
# =====================================================================
# Solo dice QUÉ métodos debe tener todo controlador.
# CÓMO se hace cada uno lo escribe cada controlador, de la forma más simple.
class CrudBase(ABC):
    """Interfaz abstracta que deben cumplir los controladores CRUD."""

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def obtener(self, id_registro):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass


# =====================================================================
# CONTROLADOR DE CLIENTES
# =====================================================================
class ClienteController(CrudBase):

    def __init__(self, archivo="data/clientes.json"):
        self.gestor = GestorJSON(archivo)

        # Leemos el JSON y convertimos cada diccionario en un objeto Cliente
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Cliente.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for cliente in self.lista:
            datos.append(cliente.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        """Devuelve un mensaje de error, o None si todo está bien."""
        # Al crear hay que traer los tres obligatorios; al actualizar, solo lo que cambia
        if id_actual is None:
            for campo in ("nombre", "apellido", "email"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            # CONJUNTO con los emails de los OTROS clientes
            usados = {c.email for c in self.lista if c.id != id_actual}
            if email in usados:
                return "Ese email ya está registrado"

        telefono = str(datos.get("telefono", "")).strip()
        if telefono != "" and not telefono.isdigit():
            return "El teléfono solo puede tener números"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_cliente):
        for cliente in self.lista:
            if cliente.id == id_cliente:
                return cliente
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for cliente in self.lista:
            if (texto in cliente.nombre.lower()
                    or texto in cliente.apellido.lower()
                    or texto in cliente.email
                    or texto in cliente.telefono
                    or texto in cliente.ciudad.lower()):
                encontrados.append(cliente)
        return encontrados

    def siguiente(self):
        mayor = 0
        for cliente in self.lista:
            if cliente.id > mayor:
                mayor = cliente.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        cliente = Cliente(self.siguiente(),
                          str(datos["nombre"]).strip().title(),
                          str(datos["apellido"]).strip().title(),
                          str(datos["email"]).strip().lower(),
                          str(datos.get("telefono", "")).strip(),
                          str(datos.get("ciudad", "")).strip().title())
        self.lista.append(cliente)
        self.guardar()
        return True, f"Cliente creado: {cliente.etiqueta()}"

    def actualizar(self, id_cliente, datos):
        cliente = self.obtener(id_cliente)
        if cliente is None:
            return False, f"No existe un cliente con id {id_cliente}"
        if not datos:
            return False, "No se indicó ningún cambio"

        # DIFERENCIA de conjuntos: campos que no existen en un cliente
        permitidos = {"nombre", "apellido", "email", "telefono", "ciudad"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        # Se valida ANTES de tocar el objeto: si algo falla, no cambia nada
        error = self.validar(datos, id_cliente)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "ciudad"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            setattr(cliente, campo, valor)

        self.guardar()
        return True, f"Cliente {id_cliente} actualizado"

    def eliminar(self, id_cliente):
        cliente = self.obtener(id_cliente)
        if cliente is None:
            return False, f"No existe un cliente con id {id_cliente}"

        self.lista.remove(cliente)
        self.guardar()
        return True, f"Cliente {id_cliente} eliminado"

    # --- propio de clientes ---
    def ciudades(self):
        """CONJUNTO de ciudades: sin repetidos. sorted() lo devuelve como lista."""
        return sorted({c.ciudad for c in self.lista if c.ciudad != ""})

    def clientes_por_ciudad(self):
        """DICCIONARIO de LISTAS: agrupa nombres en su ciudad."""
        agrupados = {}
        for cliente in self.lista:
            ciudad = cliente.ciudad or "Sin ciudad"
            agrupados.setdefault(ciudad, []).append(cliente.nombre)
        return agrupados


# =====================================================================
# CONTROLADOR DE PRODUCTOS
# =====================================================================
class ProductoController(CrudBase):

    def __init__(self, archivo="data/productos.json"):
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Producto.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for producto in self.lista:
            datos.append(producto.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "precio"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        # es_precio_valido es el método ESTÁTICO de Producto
        if "precio" in datos and not Producto.es_precio_valido(datos["precio"]):
            return f"Precio inválido: '{datos['precio']}' (debe ser un número mayor a 0)"

        stock = str(datos.get("stock", "")).strip()
        if stock != "" and not stock.isdigit():
            return "El stock debe ser un número entero positivo"

        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip().title()
            for otro in self.lista:
                if otro.nombre == nombre and otro.id != id_actual:
                    return f"Ya existe un producto llamado {nombre}"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_producto):
        for producto in self.lista:
            if producto.id == id_producto:
                return producto
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for producto in self.lista:
            if texto in producto.nombre.lower():
                encontrados.append(producto)
        return encontrados

    def siguiente(self):
        mayor = 0
        for producto in self.lista:
            if producto.id > mayor:
                mayor = producto.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        # Si no escribieron el stock, empieza en 0
        stock = str(datos.get("stock", "")).strip()
        producto = Producto(self.siguiente(),
                            str(datos["nombre"]).strip().title(),
                            float(datos["precio"]),
                            int(stock) if stock != "" else 0)
        self.lista.append(producto)
        self.guardar()
        return True, f"Producto creado: {producto.etiqueta()}"

    def actualizar(self, id_producto, datos):
        producto = self.obtener(id_producto)
        if producto is None:
            return False, f"No existe un producto con id {id_producto}"
        if not datos:
            return False, "No se indicó ningún cambio"

        desconocidos = set(datos) - {"nombre", "precio", "stock"}
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_producto)
        if error:
            return False, error

        if "nombre" in datos:
            producto.nombre = str(datos["nombre"]).strip().title()
        if "precio" in datos:
            producto.precio = float(datos["precio"])
        if "stock" in datos:
            producto.stock = int(datos["stock"])

        self.guardar()
        return True, f"Producto {id_producto} actualizado"

    def eliminar(self, id_producto):
        producto = self.obtener(id_producto)
        if producto is None:
            return False, f"No existe un producto con id {id_producto}"

        self.lista.remove(producto)
        self.guardar()
        return True, f"Producto {id_producto} eliminado"

    # --- propio de productos ---
    def con_stock_bajo(self):
        bajos = []
        for producto in self.lista:
            if producto.stock_bajo():
                bajos.append(producto)
        return bajos


# =====================================================================
# CONTROLADOR DE VENTAS
# =====================================================================
class VentaController(CrudBase):

    def __init__(self, clientes, productos, archivo="data/ventas.json"):
        # La venta USA a los otros dos controladores.
        # Hay que pasarle los MISMOS que usa main.py.
        self.clientes = clientes
        self.productos = productos
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Venta.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for venta in self.lista:
            datos.append(venta.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos):
        try:
            cliente_id = int(datos.get("cliente_id", 0))
            producto_id = int(datos.get("producto_id", 0))
            cantidad = int(datos.get("cantidad", 0))
        except (TypeError, ValueError):
            return "cliente_id, producto_id y cantidad deben ser números enteros"

        if cantidad <= 0:
            return "La cantidad debe ser mayor a 0"
        if self.clientes.obtener(cliente_id) is None:
            return f"No existe un cliente con id {cliente_id}"

        producto = self.productos.obtener(producto_id)
        if producto is None:
            return f"No existe un producto con id {producto_id}"
        if not producto.hay_stock(cantidad):
            return (f"Stock insuficiente de {producto.nombre}: "
                    f"hay {producto.stock}, piden {cantidad}")
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_venta):
        for venta in self.lista:
            if venta.id == id_venta:
                return venta
        return None

    def buscar(self, texto):
        # Las ventas se buscan por fecha, ej: "2026-09"
        texto = texto.strip()
        encontradas = []
        if texto == "":
            return encontradas

        for venta in self.lista:
            if texto in venta.fecha:
                encontradas.append(venta)
        return encontradas

    def siguiente(self):
        mayor = 0
        for venta in self.lista:
            if venta.id > mayor:
                mayor = venta.id
        return mayor + 1

    def crear(self, datos):
        # datos = {"cliente_id": 1, "producto_id": 2, "cantidad": 3}
        error = self.validar(datos)
        if error:
            return False, error

        producto = self.productos.obtener(int(datos["producto_id"]))
        precio = Producto.precio_mayorista(producto.precio, int(datos["cantidad"]))
        venta = Venta(self.siguiente(),
                      int(datos["cliente_id"]),
                      producto.id,
                      int(datos["cantidad"]),
                      precio)                   # conserva el precio ya descontado

        producto.descontar_stock(venta.cantidad)
        self.productos.guardar()                # guarda el stock nuevo en productos.json
        self.lista.append(venta)
        self.guardar()                          # guarda la venta en ventas.json
        return True, f"Venta {venta.id} registrada por ${venta.calcular_total():.2f}"

    def actualizar(self, id_venta, datos):
        # Una venta registrada no se modifica: se anula y se registra otra
        return False, "Las ventas no se pueden modificar: anúlela y registre otra"

    def eliminar(self, id_venta):
        """Anular una venta: se borra y el stock vuelve al producto."""
        venta = self.obtener(id_venta)
        if venta is None:
            return False, f"No existe la venta {id_venta}"
        if hasattr(self, "devoluciones"):
            for devolucion in self.devoluciones.leer():
                if devolucion.venta_id == id_venta:
                    return False, "La venta tiene devoluciones; elimínelas antes de anularla"

        producto = self.productos.obtener(venta.producto_id)
        if producto is not None:
            producto.devolver_stock(venta.cantidad)
            self.productos.guardar()

        self.lista.remove(venta)
        self.guardar()
        return True, f"Venta {id_venta} anulada y stock devuelto"

    # --- propio de ventas ---
    def comprobante(self, id_venta):
        venta = self.obtener(id_venta)
        if venta is None:
            return None

        cliente = self.clientes.obtener(venta.cliente_id)
        producto = self.productos.obtener(venta.producto_id)
        total = venta.calcular_total()

        texto = f"COMPROBANTE #{venta.id}   fecha: {venta.fecha}\n"
        texto += f"Cliente : {cliente.nombre_completo() if cliente else 'eliminado'}\n"
        texto += f"Producto: {producto.nombre if producto else 'eliminado'}\n"
        texto += f"Cantidad: {venta.cantidad} x ${venta.precio_unitario:.2f}\n"
        texto += "-" * 42 + "\n"
        texto += f"SUBTOTAL: ${total:.2f}\n"
        texto += f"TOTAL con IVA: ${Producto.con_iva(total):.2f}"
        return texto

    def ventas_por_cliente(self):
        """DICCIONARIO de LISTAS: {cliente_id: [ventas de ese cliente]}."""
        agrupadas = {}
        for venta in self.lista:
            if venta.cliente_id not in agrupadas:
                agrupadas[venta.cliente_id] = []
            agrupadas[venta.cliente_id].append(venta)
        return agrupadas

    def total_vendido(self):
        total = 0
        for venta in self.lista:
            total += venta.calcular_total()
        return round(total, 2)


# =====================================================================
# CONTROLADOR DE DEVOLUCIONES
# =====================================================================
class DevolucionController(CrudBase):

    def __init__(self, ventas, productos, archivo="data/devoluciones.json"):
        self.ventas = ventas
        self.productos = productos
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Devolucion.desde_diccionario(datos))
        # Al anular una venta hay que comprobar primero sus devoluciones.
        self.ventas.devoluciones = self

    def guardar(self):
        datos = []
        for devolucion in self.lista:
            datos.append(devolucion.a_diccionario())
        return self.gestor.guardar(datos)

    def leer(self):
        return self.lista

    def obtener(self, id_devolucion):
        for devolucion in self.lista:
            if devolucion.id == id_devolucion:
                return devolucion
        return None

    def buscar(self, texto):
        texto = str(texto).strip().lower()
        if not texto:
            return []
        return [d for d in self.lista if texto in d.motivo.lower()
                or texto in d.fecha or texto == str(d.venta_id)]

    def siguiente(self):
        return max((d.id for d in self.lista), default=0) + 1

    def crear(self, datos):
        try:
            venta_id = int(datos.get("venta_id"))
            cantidad = int(datos.get("cantidad"))
        except (TypeError, ValueError):
            return False, "El id de venta y la cantidad deben ser números enteros"
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a 0"

        venta = self.ventas.obtener(venta_id)
        if venta is None:
            return False, f"No existe la venta {venta_id}"
        producto = self.productos.obtener(venta.producto_id)
        if producto is None:
            return False, f"No existe el producto {venta.producto_id} de esa venta"

        ya_devuelto = sum(d.cantidad for d in self.lista if d.venta_id == venta_id)
        if cantidad > venta.cantidad - ya_devuelto:
            return False, f"Solo quedan {venta.cantidad - ya_devuelto} unidades por devolver"

        devolucion = Devolucion(self.siguiente(), venta_id, cantidad,
                                str(datos.get("motivo", "")).strip(),
                                venta.precio_unitario)
        self.lista.append(devolucion)
        if not self.guardar():
            self.lista.remove(devolucion)
            return False, "No se pudo guardar la devolución"
        producto.devolver_stock(cantidad)
        self.productos.guardar()
        return True, f"Devolución {devolucion.id} registrada por ${devolucion.calcular_total():.2f}"

    def actualizar(self, id_devolucion, datos):
        devolucion = self.obtener(id_devolucion)
        if devolucion is None:
            return False, f"No existe la devolución {id_devolucion}"
        if not datos:
            return False, "No se indicó ningún cambio"
        desconocidos = set(datos) - {"cantidad", "motivo"}
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        try:
            cantidad = int(datos.get("cantidad", devolucion.cantidad))
        except (TypeError, ValueError):
            return False, "La cantidad debe ser un número entero"
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a 0"

        venta = self.ventas.obtener(devolucion.venta_id)
        if venta is None:
            return False, "No existe la venta de esta devolución"
        producto = self.productos.obtener(venta.producto_id)
        if producto is None:
            return False, "No existe el producto de esta devolución"
        otras = sum(d.cantidad for d in self.lista
                    if d.venta_id == venta.id and d.id != id_devolucion)
        if cantidad + otras > venta.cantidad:
            return False, f"Solo se pueden devolver {venta.cantidad - otras} unidades"

        diferencia = cantidad - devolucion.cantidad
        if diferencia < 0 and producto.stock < -diferencia:
            return False, "No hay stock suficiente para reducir esta devolución"

        anterior = (devolucion.cantidad, devolucion.motivo)
        devolucion.cantidad = cantidad
        devolucion.motivo = str(datos.get("motivo", devolucion.motivo)).strip()
        if not self.guardar():
            devolucion.cantidad, devolucion.motivo = anterior
            return False, "No se pudo guardar la devolución"
        producto.stock += diferencia
        self.productos.guardar()
        return True, f"Devolución {id_devolucion} actualizada"

    def eliminar(self, id_devolucion):
        devolucion = self.obtener(id_devolucion)
        if devolucion is None:
            return False, f"No existe la devolución {id_devolucion}"
        venta = self.ventas.obtener(devolucion.venta_id)
        if venta is None:
            return False, "No existe la venta de esta devolución"
        producto = self.productos.obtener(venta.producto_id)
        if producto is None:
            return False, "No existe el producto de esta devolución"
        if producto.stock < devolucion.cantidad:
            return False, "No hay stock suficiente para eliminar esta devolución"

        self.lista.remove(devolucion)
        if not self.guardar():
            self.lista.append(devolucion)
            return False, "No se pudo eliminar la devolución"
        producto.descontar_stock(devolucion.cantidad)
        self.productos.guardar()
        return True, f"Devolución {id_devolucion} eliminada"
