import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIBROS_PATH = RAIZ / "libros.json"
USUARIOS_PATH = RAIZ / "usuarios.json"
PRESTAMOS_PATH = RAIZ / "prestamos.json"
PAGOS_PATH = RAIZ / "pagos.json"
CAPTURAS_DIR = RAIZ / "comprobantes_pago"

CATEGORIAS = [
    "finanzas",
    "fantasia",
    "educacion",
    "kdrama",
    "emprendimiento",
    "trading",
    "crecimiento_personal",
]

CATEGORIAS_RESTRINGIDAS = {"trading", "crecimiento_personal"}
ADMIN_USER = "elmartinezm"
ADMIN_PASSWORDS = {"Iiecg12", "Iiecg12."}


class Libro:
    def __init__(self, id_libro, titulo, autor, categoria, tipo="fisico", disponible=True, ruta_archivo=""):
        self.__id = id_libro
        self.__titulo = titulo
        self.__autor = autor
        self.__categoria = categoria
        self.__tipo = tipo
        self.__disponible = disponible
        self.__ruta_archivo = ruta_archivo

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def categoria(self):
        return self.__categoria

    @property
    def tipo(self):
        return self.__tipo

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        self.__disponible = bool(valor)

    @property
    def ruta_archivo(self):
        return self.__ruta_archivo

    def cambiar_disponibilidad(self, estado):
        self.__disponible = bool(estado)

    def prestar(self):
        if not self.__disponible:
            raise ValueError(f"El libro '{self.__titulo}' no está disponible.")
        self.__disponible = False
        return True

    def devolver(self):
        self.__disponible = True
        return True

    def abrir(self):
        return f"Abriendo libro físico '{self.__titulo}' en la biblioteca."

    def to_dict(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "autor": self.__autor,
            "categoria": self.__categoria,
            "tipo": self.__tipo,
            "disponible": self.__disponible,
            "ruta_archivo": self.__ruta_archivo,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_libro=data.get("id"),
            titulo=data.get("titulo"),
            autor=data.get("autor"),
            categoria=data.get("categoria"),
            tipo=data.get("tipo", "fisico"),
            disponible=data.get("disponible", True),
            ruta_archivo=data.get("ruta_archivo", ""),
        )


class LibroDigital(Libro):
    def __init__(self, id_libro, titulo, autor, categoria, disponible=True, ruta_archivo=""):
        super().__init__(
            id_libro=id_libro,
            titulo=titulo,
            autor=autor,
            categoria=categoria,
            tipo="digital",
            disponible=disponible,
            ruta_archivo=ruta_archivo,
        )

    def abrir(self):
        if self.ruta_archivo and os.path.exists(self.ruta_archivo):
            return f"Abriendo libro digital '{self.titulo}' desde: {self.ruta_archivo}"
        return f"El libro digital '{self.titulo}' no tiene archivo válido asociado."

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_libro=data.get("id"),
            titulo=data.get("titulo"),
            autor=data.get("autor"),
            categoria=data.get("categoria"),
            disponible=data.get("disponible", True),
            ruta_archivo=data.get("ruta_archivo", ""),
        )


class Usuario:
    def __init__(self, nombre, email, usuario, password, membresia="free", rol="usuario"):
        self.nombre = nombre
        self.email = email
        self.usuario = usuario
        self.password = password
        self.membresia = membresia
        self.rol = rol
        self.activo = True
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d")
        self.libros_en_casa = []
        self.lectura_inicio = None

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "email": self.email,
            "usuario": self.usuario,
            "password": self.password,
            "membresia": self.membresia,
            "rol": self.rol,
            "activo": self.activo,
            "fecha_registro": self.fecha_registro,
            "fecha_pago": None,
            "libros_en_casa": self.libros_en_casa,
            "lectura_inicio": self.lectura_inicio,
        }


def guardar_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_json(ruta, default):
    if not ruta.exists():
        guardar_json(ruta, default)
        return default
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            if datos is None:
                return default
            return datos
    except json.JSONDecodeError:
        return default


def crear_catalogo_inicial():
    return [
        {"id": 1, "titulo": "El negocio del siglo XXI", "autor": "Robert Kiyosaki", "categoria": "finanzas", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 2, "titulo": "Padre rico, padre pobre", "autor": "Robert Kiyosaki", "categoria": "finanzas", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
        {"id": 3, "titulo": "La riqueza de las naciones", "autor": "Adam Smith", "categoria": "finanzas", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 4, "titulo": "Harry Potter y la piedra filosofal", "autor": "J.K. Rowling", "categoria": "fantasia", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 5, "titulo": "El señor de los anillos", "autor": "J.R.R. Tolkien", "categoria": "fantasia", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
        {"id": 6, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria": "fantasia", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 7, "titulo": "Aprende matemáticas desde cero", "autor": "Ana López", "categoria": "educacion", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 8, "titulo": "Biología para principiantes", "autor": "Carlos Vega", "categoria": "educacion", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
        {"id": 9, "titulo": "Historia del mundo", "autor": "Martín Torres", "categoria": "educacion", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 10, "titulo": "Mi primera novela coreana", "autor": "Jin Park", "categoria": "kdrama", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 11, "titulo": "K-drama y cultura pop", "autor": "Ingrid Kim", "categoria": "kdrama", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
        {"id": 12, "titulo": "Secretos de los dramas coreanos", "autor": "Sara Min", "categoria": "kdrama", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 13, "titulo": "Emprende sin miedo", "autor": "Lina Morales", "categoria": "emprendimiento", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 14, "titulo": "Startup 101", "autor": "Pablo Ruiz", "categoria": "emprendimiento", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
        {"id": 15, "titulo": "Tu negocio paso a paso", "autor": "Valentina Cruz", "categoria": "emprendimiento", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 16, "titulo": "Trading para principiantes", "autor": "Gabriel Flores", "categoria": "trading", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 17, "titulo": "Análisis técnico esencial", "autor": "Miguel Ortega", "categoria": "trading", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
        {"id": 18, "titulo": "Rendimiento y disciplina", "autor": "Tomás Rivera", "categoria": "trading", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 19, "titulo": "Crecimiento personal intensivo", "autor": "Mariana Ahumada", "categoria": "crecimiento_personal", "tipo": "fisico", "disponible": True, "ruta_archivo": ""},
        {"id": 20, "titulo": "Mindset 360", "autor": "Fernanda Soto", "categoria": "crecimiento_personal", "tipo": "digital", "disponible": True, "ruta_archivo": ""},
    ]


def inicializar_archivos():
    CAPTURAS_DIR.mkdir(parents=True, exist_ok=True)

    if not LIBROS_PATH.exists():
        guardar_json(LIBROS_PATH, crear_catalogo_inicial())

    if not USUARIOS_PATH.exists():
        admin = Usuario(
            nombre="Administrador",
            email="admin@biblioteca.local",
            usuario=ADMIN_USER,
            password="Iiecg12.",
            membresia="gold",
            rol="admin",
        )
        guardar_json(USUARIOS_PATH, [admin.to_dict()])

    if not PRESTAMOS_PATH.exists():
        guardar_json(PRESTAMOS_PATH, [])

    if not PAGOS_PATH.exists():
        guardar_json(PAGOS_PATH, [])


def cargar_libros():
    return cargar_json(LIBROS_PATH, crear_catalogo_inicial())


def guardar_libros(libros):
    guardar_json(LIBROS_PATH, libros)


def cargar_usuarios():
    default = []
    if USUARIOS_PATH.exists():
        datos = cargar_json(USUARIOS_PATH, default)
        return datos
    return default


def guardar_usuarios(usuarios):
    guardar_json(USUARIOS_PATH, usuarios)


def cargar_prestamos():
    return cargar_json(PRESTAMOS_PATH, [])


def guardar_prestamos(prestamos):
    guardar_json(PRESTAMOS_PATH, prestamos)


def cargar_pagos():
    return cargar_json(PAGOS_PATH, [])


def guardar_pagos(pagos):
    guardar_json(PAGOS_PATH, pagos)


def mostrar_catalogo(usuario=None, categoria=None):
    libros = cargar_libros()
    if categoria:
        libros = [l for l in libros if l["categoria"] == categoria]

    print("\n========================================")
    print("       CATÁLOGO DE LA BIBLIOTECA")
    print("========================================")
    if usuario:
        print(f"Usuario: {usuario['usuario']} | Membresía: {usuario['membresia']}")
    if categoria:
        print(f"Categoría: {categoria}")
    else:
        print("Categorías disponibles: ")
        for idx, cat in enumerate(CATEGORIAS, 1):
            print(f"  {idx}. {cat}")

    if not libros:
        print("No hay libros disponibles en esta categoría.")
        return

    print(f"{'ID':<4} | {'Título':<30} | {'Autor':<22} | {'Tipo':<8} | {'Disp.':<6}")
    print("-" * 90)
    for libro in libros:
        disponible = "Sí" if libro.get("disponible") else "No"
        print(f"{libro['id']:<4} | {libro['titulo']:<30} | {libro['autor']:<22} | {libro['tipo']:<8} | {disponible:<6}")
    print("-" * 90)


def selec_categoria(usuario):
    print("\nElige una categoría:")
    for idx, cat in enumerate(CATEGORIAS, 1):
        print(f"  {idx}. {cat}")
    try:
        opcion = int(input("Opción: ").strip())
    except ValueError:
        print("Debes escribir un número válido.")
        return None

    if opcion < 1 or opcion > len(CATEGORIAS):
        print("Número de categoría inválido.")
        return None

    categoria = CATEGORIAS[opcion - 1]
    if usuario and usuario.get("membresia") == "free" and categoria in CATEGORIAS_RESTRINGIDAS:
        print("Lo siento, esa categoría está restringida para Free.")
        return None
    return categoria


def buscar_libro_por_id(id_libro):
    libros = cargar_libros()
    for libro in libros:
        if libro["id"] == int(id_libro):
            return libro
    return None


def buscar_usuario_por_usuario(usuario):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario:
            return u
    return None


def actualizar_usuario(usuario_actual):
    usuarios = cargar_usuarios()
    for idx, usuario in enumerate(usuarios):
        if usuario["usuario"] == usuario_actual["usuario"]:
            usuarios[idx] = usuario_actual
            break
    guardar_usuarios(usuarios)


def registrar_usuario():
    print("\n=== REGISTRO ===")
    nombre = input("Nombre completo: ").strip()
    email = input("Correo electrónico: ").strip()
    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    membresia = input("Membresía (free/gold/platinum): ").strip().lower()

    if not nombre or not email or not usuario or not password:
        print("Todos los campos son obligatorios.")
        return None

    if membresia not in ["free", "gold", "platinum"]:
        print("Membresía no válida.")
        return None

    usuarios = cargar_usuarios()
    for u in usuarios:
        if u["usuario"].lower() == usuario.lower():
            print("Ese usuario ya existe.")
            return None
        if u["email"].lower() == email.lower():
            print("Ese correo ya existe.")
            return None

    nuevo = Usuario(nombre, email, usuario, password, membresia, "usuario")
    usuarios.append(nuevo.to_dict())
    guardar_usuarios(usuarios)
    print("Usuario registrado con éxito.")
    return nuevo.to_dict()


def iniciar_sesion():
    print("\n=== INICIO DE SESIÓN ===")
    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario and u["password"] == password:
            return u

    if usuario == ADMIN_USER and password in ADMIN_PASSWORDS:
        admin = buscar_usuario_por_usuario(ADMIN_USER)
        if admin:
            return admin

    print("Usuario o contraseña incorrectos.")
    return None


def iniciar_lectura(usuario):
    if usuario["membresia"] == "free":
        usuario["lectura_inicio"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        actualizar_usuario(usuario)
        print("Sesión de lectura iniciada. Tienes un máximo de 2 horas.")
        return True
    usuario["lectura_inicio"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    actualizar_usuario(usuario)
    print("Sesión de lectura iniciada.")
    return True


def cerrar_lectura(usuario):
    if not usuario.get("lectura_inicio"):
        print("No hay lectura activa.")
        return

    inicio = datetime.strptime(usuario["lectura_inicio"], "%Y-%m-%d %H:%M:%S")
    horas = (datetime.now() - inicio).total_seconds() / 3600

    if usuario["membresia"] == "free" and horas > 2:
        print(f"Excediste el máximo permitido. Duraste {horas:.2f} horas.")
    else:
        print(f"Lectura finalizada. Duraste {horas:.2f} horas.")

    usuario["lectura_inicio"] = None
    actualizar_usuario(usuario)


def prestamos_activos(usuario):
    prestamos = cargar_prestamos()
    return [p for p in prestamos if p["usuario"] == usuario["usuario"] and not p.get("devuelto", False)]


def validar_limites(usuario):
    activos = prestamos_activos(usuario)
    if usuario["membresia"] == "free":
        return False, "Free no puede llevar libros a casa. Solo lectura en la biblioteca."
    if usuario["membresia"] == "gold" and len(activos) >= 1:
        return False, "Gold solo puede llevarse 1 libro de préstamo activo."
    if usuario["membresia"] == "platinum" and len(activos) >= 3:
        return False, "Platinum solo puede llevarse 3 libros de préstamo activo."
    return True, ""


def calcular_multa(fecha_esperada, fecha_entrega):
    fecha_esperada = datetime.strptime(fecha_esperada, "%Y-%m-%d").date()
    fecha_entrega = datetime.strptime(fecha_entrega, "%Y-%m-%d").date()
    if fecha_entrega <= fecha_esperada:
        return 0
    delta = fecha_entrega - fecha_esperada
    return max(delta.days, 0)


def prestar_libro(usuario):
    if usuario["membresia"] == "free":
        print("Free no puede llevar libros a casa.")
        return

    valido, mensaje = validar_limites(usuario)
    if not valido:
        print(mensaje)
        return

    categoria = selec_categoria(usuario)
    if not categoria:
        return

    libros = cargar_libros()
    disponibles = [l for l in libros if l["categoria"] == categoria and l["disponible"]]
    if not disponibles:
        print("No hay libros disponibles en esta categoría.")
        return

    print("\nLibros disponibles:")
    for libro in disponibles:
        print(f"{libro['id']} - {libro['titulo']} ({libro['tipo']})")

    try:
        id_libro = int(input("Selecciona el ID del libro: ").strip())
    except ValueError:
        print("Debes ingresar un número válido.")
        return

    libro = buscar_libro_por_id(id_libro)
    if not libro:
        print("Ese libro no existe.")
        return
    if libro["categoria"] != categoria or not libro["disponible"]:
        print("Ese libro no está disponible en la categoría indicada.")
        return

    if usuario["membresia"] == "gold":
        dias = 7
    elif usuario["membresia"] == "platinum":
        dias = 30
    else:
        dias = 0

    fecha_prestamo = datetime.now().date()
    fecha_limite = fecha_prestamo + timedelta(days=dias)

    prestamo = {
        "id": len(cargar_prestamos()) + 1,
        "usuario": usuario["usuario"],
        "email": usuario["email"],
        "libro_id": libro["id"],
        "titulo": libro["titulo"],
        "categoria": libro["categoria"],
        "tipo": libro["tipo"],
        "fecha_prestamo": fecha_prestamo.strftime("%Y-%m-%d"),
        "fecha_devolucion": fecha_limite.strftime("%Y-%m-%d"),
        "devuelto": False,
        "multa": 0,
    }

    prestamos = cargar_prestamos()
    prestamos.append(prestamo)
    guardar_prestamos(prestamos)

    for item in libros:
        if item["id"] == libro["id"]:
            item["disponible"] = False
            break
    guardar_libros(libros)

    if usuario.get("libros_en_casa") is None:
        usuario["libros_en_casa"] = []
    usuario["libros_en_casa"].append(libro["id"])
    actualizar_usuario(usuario)

    print(f"Libro prestado correctamente. Debes devolverlo antes del {fecha_limite.strftime('%d/%m/%Y')}.")


def devolver_libro(usuario):
    prestamos = cargar_prestamos()
    activos = [p for p in prestamos if p["usuario"] == usuario["usuario"] and not p.get("devuelto", False)]
    if not activos:
        print("No tienes libros prestados activos.")
        return

    print("\nTus préstamos activos:")
    for p in activos:
        print(f"{p['id']} - {p['titulo']} (devolver antes de {p['fecha_devolucion']})")

    try:
        id_prestamo = int(input("Selecciona el ID del préstamo a devolver: ").strip())
    except ValueError:
        print("Debes ingresar un número válido.")
        return

    prestamo = None
    for p in activos:
        if p["id"] == id_prestamo:
            prestamo = p
            break

    if not prestamo:
        print("Ese préstamo no existe para este usuario.")
        return

    fecha_real = datetime.now().date().strftime("%Y-%m-%d")
    multa = calcular_multa(prestamo["fecha_devolucion"], fecha_real)
    prestamo["fecha_entrega_real"] = fecha_real
    prestamo["multa"] = multa
    prestamo["devuelto"] = True

    libros = cargar_libros()
    for libro in libros:
        if libro["id"] == prestamo["libro_id"]:
            libro["disponible"] = True
            break
    guardar_libros(libros)

    for idx, item in enumerate(prestamos):
        if item["id"] == prestamo["id"]:
            prestamos[idx] = prestamo
            break
    guardar_prestamos(prestamos)

    if usuario.get("libros_en_casa") is not None and prestamo["libro_id"] in usuario["libros_en_casa"]:
        usuario["libros_en_casa"].remove(prestamo["libro_id"])
    actualizar_usuario(usuario)

    if multa > 0:
        print(f"Libro devuelto. Multa aplicada: ${multa:.2f} por {multa} día(s) de retraso.")
    else:
        print("Libro devuelto a tiempo. Sin multa.")


def pagar_membresia(usuario):
    print("\n=== PAGAR MEMBRESÍA ===")
    print("Método: Binance")
    print("Cuenta: alejandromartinezmedina18@gmail.com")
    print("Gold = $30 anual")
    print("Platinum = $50 anual")
    print("Free = sin costo")

    opcion = input("Elige membresía (free/gold/platinum): ").strip().lower()
    if opcion not in ["free", "gold", "platinum"]:
        print("Opción no válida.")
        return

    if opcion == "free":
        usuario["membresia"] = "free"
        actualizar_usuario(usuario)
        print("Tu membresía quedó en Free.")
        return

    monto = 30 if opcion == "gold" else 50
    ruta_capture = input("Ruta del comprobante de pago (imagen): ").strip()
    if not ruta_capture or not os.path.exists(ruta_capture):
        print("La ruta no existe. Debes adjuntar un comprobante válido.")
        return

    nombre_archivo = f"{usuario['usuario']}_{opcion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    destino = CAPTURAS_DIR / nombre_archivo
    shutil.copy2(ruta_capture, destino)

    pago = {
        "usuario": usuario["usuario"],
        "email": usuario["email"],
        "membresia": opcion,
        "monto": monto,
        "fecha_pago": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metodo": "Binance",
        "cuenta": "alejandromartinezmedina18@gmail.com",
        "archivo": nombre_archivo,
        "estado": "pagado",
    }

    pagos = cargar_pagos()
    pagos.append(pago)
    guardar_pagos(pagos)

    usuario["membresia"] = opcion
    usuario["fecha_pago"] = datetime.now().strftime("%Y-%m-%d")
    actualizar_usuario(usuario)
    print(f"Pago registrado correctamente. Ahora tu membresía es {opcion.upper()}.")
    print(f"Comprobante guardado en {destino}")


def mostrar_mi_perfil(usuario):
    print("\n=== MI PERFIL ===")
    print(f"Nombre: {usuario['nombre']}")
    print(f"Email: {usuario['email']}")
    print(f"Usuario: {usuario['usuario']}")
    print(f"Membresía: {usuario['membresia']}")
    print(f"Rol: {usuario['rol']}")
    print(f"Libros en casa: {usuario.get('libros_en_casa', [])}")


def ver_mis_prestamos(usuario):
    prestamos = cargar_prestamos()
    print("\n=== MIS PRÉSTAMOS ===")
    filas = [p for p in prestamos if p["usuario"] == usuario["usuario"]]
    if not filas:
        print("No tienes préstamos registrados.")
        return
    for p in filas:
        estado = "Devuelto" if p.get("devuelto") else "Activo"
        print(f"#{p['id']} | {p['titulo']} | Estado: {estado} | Fecha límite: {p['fecha_devolucion']} | Multa: ${p.get('multa', 0):.2f}")


def menu_usuario(usuario):
    while True:
        print("\n========================================")
        print("         MENÚ DEL USUARIO")
        print("========================================")
        print("1. Ver perfil")
        print("2. Ver catálogo por categoría")
        print("3. Iniciar lectura en biblioteca")
        print("4. Cerrar lectura")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Pagar membresía")
        print("8. Ver mis préstamos")
        print("9. Cerrar sesión")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_mi_perfil(usuario)
        elif opcion == "2":
            categoria = selec_categoria(usuario)
            if categoria:
                mostrar_catalogo(usuario, categoria)
        elif opcion == "3":
            iniciar_lectura(usuario)
        elif opcion == "4":
            cerrar_lectura(usuario)
        elif opcion == "5":
            prestar_libro(usuario)
        elif opcion == "6":
            devolver_libro(usuario)
        elif opcion == "7":
            pagar_membresia(usuario)
        elif opcion == "8":
            ver_mis_prestamos(usuario)
        elif opcion == "9":
            if usuario.get("lectura_inicio"):
                cerrar_lectura(usuario)
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")


def ver_usuarios_admin():
    usuarios = cargar_usuarios()
    print("\n=== USUARIOS REGISTRADOS ===")
    for u in usuarios:
        print(f"{u['usuario']} | {u['email']} | Membresía: {u['membresia']} | Rol: {u['rol']}")


def ver_pagos_admin():
    pagos = cargar_pagos()
    print("\n=== PAGOS REGISTRADOS ===")
    if not pagos:
        print("No hay pagos registrados.")
        return
    for p in pagos:
        print(f"Usuario: {p['usuario']} | Membresía: {p['membresia']} | Monto: ${p['monto']} | Fecha: {p['fecha_pago']} | Archivo: {p['archivo']}")


def agregar_libro_admin():
    print("\n=== AGREGAR LIBRO ===")
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    categoria = input("Categoría: ").strip().lower()
    tipo = input("Tipo (fisico/digital): ").strip().lower()

    if categoria not in CATEGORIAS:
        print("Categoría no válida.")
        return
    if tipo not in ["fisico", "digital"]:
        print("Tipo no válido.")
        return

    libros = cargar_libros()
    id_nuevo = max([l["id"] for l in libros], default=0) + 1
    ruta_archivo = ""
    if tipo == "digital":
        ruta_archivo = input("Ruta del archivo PDF (opcional): ").strip()

    if tipo == "digital":
        libro = LibroDigital(id_nuevo, titulo, autor, categoria, True, ruta_archivo)
    else:
        libro = Libro(id_nuevo, titulo, autor, categoria, "fisico", True, ruta_archivo)

    libros.append(libro.to_dict())
    guardar_libros(libros)
    print("Libro agregado correctamente.")


def cambiar_disponibilidad_admin():
    libros = cargar_libros()
    print("\n=== CAMBIAR DISPONIBILIDAD ===")
    for l in libros:
        print(f"{l['id']} - {l['titulo']} | Disponible: {'Sí' if l['disponible'] else 'No'}")

    try:
        id_libro = int(input("ID del libro: ").strip())
    except ValueError:
        print("Debes ingresar un número válido.")
        return

    for libro in libros:
        if libro["id"] == id_libro:
            estado = input("¿Disponible? (s/n): ").strip().lower()
            libro["disponible"] = estado in {"s", "si", "y", "yes"}
            guardar_libros(libros)
            print("Disponibilidad actualizada.")
            return
    print("No existe ese libro.")


def ver_prestamos_admin():
    prestamos = cargar_prestamos()
    print("\n=== PRÉSTAMOS DEL SISTEMA ===")
    if not prestamos:
        print("No hay préstamos registrados.")
        return
    for p in prestamos:
        estado = "Devuelto" if p.get("devuelto", False) else "Activo"
        print(f"#{p['id']} | Usuario: {p['usuario']} | Libro: {p['titulo']} | Estado: {estado} | Fecha límite: {p['fecha_devolucion']} | Multa: ${p.get('multa', 0):.2f}")


def menu_admin(usuario):
    while True:
        print("\n========================================")
        print("          MENÚ ADMINISTRADOR")
        print("========================================")
        print("1. Ver usuarios")
        print("2. Ver pagos")
        print("3. Agregar libro")
        print("4. Ver catálogo")
        print("5. Cambiar disponibilidad")
        print("6. Ver préstamos")
        print("7. Cerrar sesión")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            ver_usuarios_admin()
        elif opcion == "2":
            ver_pagos_admin()
        elif opcion == "3":
            agregar_libro_admin()
        elif opcion == "4":
            mostrar_catalogo(usuario)
        elif opcion == "5":
            cambiar_disponibilidad_admin()
        elif opcion == "6":
            ver_prestamos_admin()
        elif opcion == "7":
            print("Sesión de administrador cerrada.")
            break
        else:
            print("Opción inválida.")


def main():
    inicializar_archivos()
    print("\n========================================")
    print("   BIBLIOTECA PÚBLICA")
    print("========================================")
    while True:
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            usuario = iniciar_sesion()
            if not usuario:
                continue
            if usuario["usuario"] == ADMIN_USER:
                menu_admin(usuario)
            else:
                menu_usuario(usuario)
        elif opcion == "2":
            usuario = registrar_usuario()
            if usuario:
                menu_usuario(usuario)
        elif opcion == "3":
            print("Gracias por usar la biblioteca.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
