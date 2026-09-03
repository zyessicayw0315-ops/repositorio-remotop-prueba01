def pedir_datos_cliente():
    print("\n====================================")
    print("        DATOS DEL CLIENTE")
    print("====================================")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()

    edad_valida = False
    while not edad_valida:
        edad = input("Edad: ").strip()
        if edad.isdigit() and int(edad) > 0:
            edad_valida = True
        else:
            print("La edad debe ser un número válido mayor que 0.")

    return {
        "nombre": nombre,
        "apellido": apellido,
        "edad": int(edad)
    }