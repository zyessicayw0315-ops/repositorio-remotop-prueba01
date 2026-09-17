# 1. encapsulamiento
# - Proteger y controlar datos de las clases

# 2. Abstraccion
# - Mostrar lo necesario y ocultar complejidad

#3. Herencia
# - Crear clases nuevas reutilazon atributos y metodos de otras clases

# 4. Polimorfismo
# - Una misma accion puede comportase diferente dependiendo de la clase que lo ejecutr

# ================== ENCAPSULAMIENTO ==============================#
# 这个是封装的例子， encapsulamiento是指的是将数据和方法封装在类中，保护数据不被外部直接访问和修改。通过使用私有属性和方法，可以控制对数据的访问权限，从而提高代码的安全性和可维护性。

class CuentaBancaria: #这个是建立一个银行
    def __init__(self, titular,numero_de_cuenta, saldo): #这个是银行的特征
        self.titular = titular
        self.numero_de_cuenta = numero_de_cuenta
        self.saldo = saldo # self.__saldo = saldo #这个是可以保护的属性，外部不能直接访问和修改
        self.__saldo = saldo

    def consultar_saldo(self):
        return self.__saldo

    def depositar(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad
        else:
            print("Cantidad inválida para depositar.")

    def retirar(self, cantidad):
        if 0 < cantidad <= self.__saldo:
            self.__saldo -= cantidad
        else:
            print("Cantidad inválida para retirar o saldo insuficiente.")
cuenta_1 = CuentaBancaria("David Marin", "12345678", 5000.00) #这个是银行的特征
cuenta_2 = CuentaBancaria("Freddy Colina", "22345678", 9000.00) #这个是银行的特征

print(cuenta_1.titular) #这个是银行的特征
print(cuenta_2.titular) #这个是银行的特征

cuenta_1.saldo = 10000.00

print(cuenta_1.saldo) #这里我不应该自己增加我的账号存款，他必须得有一个合法的程序知道我的钱怎么来的，它的来源是什么。
#比如pago movil, 或者transferencias.像这种第三方添加资金我的账号资金才可以改变。

print(cuenta_1.consultar_saldo()) #使用封装的方法来查看余额
cuenta_1.depositar(2000.00) #使用封装的方法来存款
print(cuenta_1.consultar_saldo()) #使用封装的方法来查看余额
cuenta_1.retirar(1000.00) #使用封装的方法来取款
print(cuenta_1.consultar_saldo()) #使用封装的方法来查看余额



# ==============ABSTRACCION========================#
# 这个是抽象的例子，abstraccion是指的是将复杂的系统简化为更易于理解和使用的模型。
# 通过抽象，我们可以隐藏不必要的细节，只展示对用户有用的信息和功能，从而提高代码的可读性和可维护性。

class Cafetera:
    def __init__(self):
        self.agua = 1000

    def __encender(self): #添加———— 是为了保护这个方法不被外部直接调用，只有类内部的方法可以调用它，从而实现封装的效果。
        print("Encendiendo cafetera")

    def __calendar_agua(self):
        print("Colocando agua.....")
        print("Calentado agua.....")

    def ___prepara_cafe(self):
        print("Colocando cafe.....")
        print("preparando cafe.....")

#这里的三个方法都是私有方法，外部不能直接调用它们，只能通过hacer_cafe()方法来调用它们，从而实现了抽象的效果。

    def hacer_cafe(self):
        self.__encender()
        self.__calendar_agua()
        self.___prepara_cafe()

        print("Cafe listo.")

caf = Cafetera()

caf.hacer_cafe() #这个是调用咖啡机的功能，外部只能调用这个方法，不能直接调用内部的私有方法，从而实现了抽象的效果。

#这个抽象的例子是咖啡机的功能，用户只需要知道如何使用咖啡机，而不需要了解咖啡机内部的工作原理和细节，从而实现了抽象的效果。
#这里在咖啡机的例子中，用户只需要调用hacer_cafe()方法，就可以完成整个咖啡制作的过程，而不需要关心咖啡机内部的具体实现细节，这就是抽象的体现。
#而用户不需要知道咖啡机内部的工作原理和细节，比如如何加热水，如何研磨咖啡豆，如何控制水流量等等，这些都是咖啡机内部的实现细节，用户不需要关心这些细节，只需要知道如何使用咖啡机就可以了，这就是抽象的体现。


# ==============HERENCIA========================#
# 这个是继承的例子，herencia是指的是一个类可以继承另一个类的属性和方法，从而实现代码的重用和扩展。通过继承，我们可以创建一个新的类，
# 该类可以继承父类的属性和方法，同时还可以添加自己的属性和方法，从而实现代码的扩展和定制。 

class Usuario:
    def __init__(self, nombre, cedular, email, telefono, direccion, edad):
        self.nombre = nombre
        self.cedular = cedular
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.edad = edad

class Estudiante(Usuario): #这个是继承的例子，Estudiante类继承了Usuario类的属性和方法，同时还添加了自己的属性和方法，从而实现了代码的扩展和定制。
    def __init__(self, nombre, cedular, email, telefono, direccion, edad, carrera, semestre):
        super().__init__(nombre, cedular, email, telefono, direccion, edad)
        self.carrera = carrera
        self.semestre = semestre

# 这里super().__init__()是调用父类的构造函数，来初始化父类的属性，从而实现了代码的重用和扩展。
# 就比如说你有一个父类是动物，子类是狗，猫，鸟等等，这些子类都继承了父类的属性和方法，同时还可以添加自己的属性和方法，从而实现了代码的扩展和定制。
# 这里super()是一个内置函数，它返回父类的一个临时对象，从而可以调用父类的方法。
# 如果不加super()，那么子类就无法调用父类的方法，从而无法实现代码的重用和扩展。

class Profesor(Usuario): #这个是继承的例子，Profesor类继承了Usuario类的属性和方法，同时还添加了自己的属性和方法，从而实现了代码的扩展和定制。
    def __init__(self, nombre, cedular, email, telefono, direccion, edad, materia):
        super().__init__(nombre, cedular, email, telefono, direccion, edad)
        self.materia = materia

usuario_1 = Usuario("Juan Perez", "12345678", "juan.perez@email.com", "0987654321", "Calle 123", 25)
estudiante_1 = Estudiante("Maria Garcia", "87654321", "maria.garcia@email.com", "0912345678", "Calle 456", 20, "Ingenieria", 3)
profesor_1 = Profesor("Carlos Rodriguez", "11223344", "carlos.rodriguez@email.com", "0987654321", "Calle 789", 35, "Matematicas")

print("==========Informacion de Usuario==========")
usuario_1.mostrar_informacion() #这个是调用父类的方法，显示用户的信息
print("==========Informacion de Estudiante==========")
estudiante_1.mostrar_informacion() #这个是调用子类的方法，显示学生的信息
print("==========Informacion de Profesor==========")
profesor_1.mostrar_informacion() #这个是调用子类的方法，显示教授的信息


# ==============POLIMORFISMO========================#
# 这个是多态的例子，polimorfismo是指的是同一个方法在不同的类中可以有不同的实现，
# 从而实现代码的灵活性和可扩展性。通过多态，我们可以使用相同的方法名来调用不同类中的方法，从而实现代码的灵活性和可扩展性。

class Usuario:
    def __init__(self, nombre, cedular, email, telefono, direccion, edad):
        self.nombre = nombre
        self.cedular = cedular
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.edad = edad

class Estudiante(Usuario): 
    def __init__(self, nombre, cedular, email, telefono, direccion, edad, carrera, semestre):
        super().__init__(nombre, cedular, email, telefono, direccion, edad)
        self.carrera = carrera
        self.semestre = semestre

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Cedula: {self.cedular}")
        print(f"Email: {self.email}")
        print(f"Telefono: {self.telefono}")
        print(f"Direccion: {self.direccion}")
        print(f"Edad: {self.edad}")
        print(f"Carrera: {self.carrera}")
        print(f"Semestre: {self.semestre}")

class Profesor(Usuario): 
    def __init__(self, nombre, cedular, email, telefono, direccion, edad, materia):
        super().__init__(nombre, cedular, email, telefono, direccion, edad)
        self.materia = materia

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Cedula: {self.cedular}")
        print(f"Email: {self.email}")
        print(f"Telefono: {self.telefono}")
        print(f"Direccion: {self.direccion}")
        print(f"Edad: {self.edad}")
        print(f"Materia: {self.materia}")

#这里多态的体现就是Estudiante和Profesor类都继承了Usuario类，并且都实现了mostrar_informacion()方法，但是它们的实现方式不同，从而实现了代码的灵活性和可扩展性。

usuario_1 = Usuario("Juan Perez", "12345678", "juan.perez@email.com", "0987654321", "Calle 123", 25)
estudiante_1 = Estudiante("Maria Garcia", "87654321", "maria.garcia@email.com", "0912345678", "Calle 456", 20, "Ingenieria", 3)
profesor_1 = Profesor("Carlos Rodriguez", "11223344", "carlos.rodriguez@email.com", "0987654321", "Calle 789", 35, "Matematicas")

print("==========Informacion de Usuario==========")
usuario_1.mostrar_informacion() 
print("==========Informacion de Estudiante==========")
estudiante_1.mostrar_informacion() 
print("==========Informacion de Profesor==========")
profesor_1.mostrar_informacion()