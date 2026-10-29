class Estudiante: #这个是定义一个名为Estudiante的类
    def __init__(self, nombre, edad, telefono, email, carrera=None, direccion=None):
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.email = email
        self.carrera = carrera
        self.direccion = direccion

    def saludar(self): #这个是定义一个名为saludar的方法，用于返回一个问候语
        return f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años."

class Profesor: #这个是定义一个名为Profesor的类
    def __init__(self, nombre, edad, telefono, email, especialidad=None, direccion=None):
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.email = email
        self.especialidad = especialidad
        self.direccion = direccion

    def saludar(self): #这个是定义一个名为saludar的方法，用于返回一个问候语
        return f"Hola, mi nombre es {self.nombre} y soy profesor de {self.especialidad}."

    
estudiante_1 = Estudiante("Juan", 20, "123456789", "juan@email.com", "Ingeniería", "Calle Falsa 123") #这个是创建一个名为estudiante_1的Estudiante对象，并传入参数
estudiante_2 = Estudiante("María", 22, "987654321", "maria@email.com", "Medicina", "Avenida Principal 456") #这个是创建一个名为estudiante_2的Estudiante对象，并传入参数
profesor_1 = Profesor("Dr. García", 45, "555-1234", "garcia@email.com", "Matemáticas") #这个是创建一个名为profesor_1的Profesor对象，并传入参数

personal = [estudiante_1, estudiante_2, profesor_1] #这个是创建一个名为personal的列表，并将estudiante_1、estudiante_2和profesor_1添加到列表中


for persona in personal:
    print()
    print('----------------------')
    if isinstance(persona, Estudiante): #这个是检查persona是否是Estudiante类的实例
        print("Es un estudiante")
        print(f"Nombre: {persona.nombre}, Edad: {persona.edad}, Teléfono: {persona.telefono}, Email: {persona.email}, Carrera: {persona.carrera}, Dirección: {persona.direccion}")
    else:
        print("Es un profesor")
        print(f"Nombre: {persona.nombre}, Edad: {persona.edad}, Teléfono: {persona.telefono}, Email: {persona.email}, Especialidad: {persona.especialidad}, Dirección: {persona.direccion}")


print(estudiante_1.email)
print(estudiante_2.email) #这个是打印estudiante_1和estudiante_2的email属性
print(profesor_1.saludar()) #这个是打印profesor_1的问候语

#这整个代码定义了一个名为Estudiante的类，该类有一个构造函数__init__，用于初始化学生的属性，包括nombre（姓名）、edad（年龄）、telefono（电话）、email（电子邮件）、carrera（专业）和direccion（地址）。
#此外，该类还定义了一个方法saludar，用于返回一个问候语。然后，代码创建了两个Estudiante对象estudiante_1和estudiante_2，并打印了它们的email属性。
#它的作用是展示如何定义一个类、创建对象以及访问对象的属性和方法。

print(isinstance(estudiante_1, Estudiante)) #这个是检查estudiante_1是否是Estudiante类的实例
#isinstance()函数用于检查一个对象是否是指定类的实例，如果是则返回True，否则返回False。
print(isinstance(estudiante_2, Estudiante))
print(isinstance(profesor_1, Profesor)) #这个是检查profesor_1是否是Profesor类的实例


#-----------------------STR------------------------------#
#str()函数用于将对象转换为字符串表示形式。它通常用于打印对象或将对象作为字符串处理。
print(str(estudiante_1))
#会显示类似于 <__main__.Estudiante object at 0x7f8b8c3e1d30> 的输出，这表示estudiante_1是Estudiante类的一个实例，并显示了它在内存中的地址。

#----------------------isinstance()------------------------------#
#isinstance()函数用于检查一个对象是否是指定类的实例。如果是，则返回True，否则返回False。它可以用于类型检查和多态性处理。
