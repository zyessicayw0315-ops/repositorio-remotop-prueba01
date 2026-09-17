class Supermarket: #这里是你要创造的场景
    def __init__(self, nombre, monto, peso): #这个场景有的特性，比如学校的话就是学生，书桌，老师。。。
        self.nombre = nombre
        self.monto = monto
        self.peso = peso
#上面三个都是超市所需要的特征
    def mostrar_informacion(self): #每一个特征的名字
        print(f"Nombre: {self.nombre}")
        print(f"Monto: {self.monto}")
        print(f"Peso: {self.peso}")

    def consulta_precio(self, consulta): #当你需要叫唤它的时候你想要他做出回应。
        print(f"{consulta}, {self.monto}$")

producto_1 = Supermarket("Carne", "8", "1kg") #货物的特征
producto_2 = Supermarket("Pollo", "6", "1.5kg")
producto_3 = Supermarket("Marrano", "10", "500g")

producto_2.mostrar_informacion() #测试是否运行
print("=======================================")
print(producto_2.nombre)
producto_2.consulta_precio("Hola el precio es: ")


