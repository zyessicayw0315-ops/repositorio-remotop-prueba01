from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta_boletos" # 用于显示操作提示消息

DB_NAME = "boletos.db"

def init_db():
    """初始化数据库与数据表"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. 路线/车次表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rutas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destino TEXT NOT NULL,
            dias TEXT NOT NULL,
            horarios TEXT NOT NULL,
            chofer TEXT NOT NULL,
            asientos_disponibles INTEGER NOT NULL
        )
    ''')
    
    # 2. 车票/客户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boletos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cedula TEXT NOT NULL,
            telefono TEXT NOT NULL,
            ruta_id INTEGER NOT NULL,
            dia_seleccionado TEXT NOT NULL,
            horario_seleccionado TEXT NOT NULL,
            FOREIGN KEY (ruta_id) REFERENCES rutas (id)
        )
    ''')
    
    # 如果车次表为空，插入默认的 5 个车次信息
    cursor.execute("SELECT COUNT(*) FROM rutas")
    if cursor.fetchone()[0] == 0:
        rutas_iniciales = [
            ('Caracas', 'Lunes y Miércoles', '06:00 AM, 10:00 AM', 'Carlos Mendoza', 32),
            ('Valencia', 'Martes y Jueves', '08:00 AM, 11:00 AM', 'José Rodríguez', 32),
            ('Maracaibo', 'Martes y Viernes', '04:00 AM, 06:00 AM', 'Luis Hernández', 28),
            ('Barquisimeto', 'Miércoles y Viernes', '05:00 AM, 08:00 AM', 'Miguel Gómez', 30),
            ('Zulia', 'Jueves y Sábado', '02:30 AM, 10:00 AM', 'Pedro Martínez', 28)
        ]
        cursor.executemany('''
            INSERT INTO rutas (destino, dias, horarios, chofer, asientos_disponibles)
            VALUES (?, ?, ?, ?, ?)
        ''', rutas_iniciales)
        
    conn.commit()
    conn.close()

# 启动时初始化数据库
init_db()

@app.route('/')
def index():
    """首页：获取所有车次和订单"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rutas")
    rutas = cursor.fetchall()
    
    cursor.execute('''
        SELECT b.id, b.nombre, b.cedula, b.telefono, r.destino, b.dia_seleccionado, b.horario_seleccionado, r.chofer
        FROM boletos b
        JOIN rutas r ON b.ruta_id = r.id
    ''')
    boletos = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', rutas=rutas, boletos=boletos)

@app.route('/comprar', methods=['POST'])
def comprar():
    """购买车票接口"""
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    ruta_id = int(request.form['ruta_id'])
    dia = request.form['dia']
    horario = request.form['horario']
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 检查座位余量
    cursor.execute("SELECT asientos_disponibles FROM rutas WHERE id = ?", (ruta_id,))
    asientos = cursor.fetchone()[0]
    
    if asientos <= 0:
        flash(" ¡Lo sentimos! Este autobús no tiene asientos disponibles (¡Agotado!).")
    else:
        # 扣减 1 个座位
        cursor.execute("UPDATE rutas SET asientos_disponibles = asientos_disponibles - 1 WHERE id = ?", (ruta_id,))
        # 保存购票记录
        cursor.execute('''
            INSERT INTO boletos (nombre, cedula, telefono, ruta_id, dia_seleccionado, horario_seleccionado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, cedula, telefono, ruta_id, dia, horario))
        conn.commit()
        flash(" ¡Boleto comprado con éxito!")
        
    conn.close()
    return redirect(url_for('index'))

@app.route('/cambiar/<int:boleto_id>', methods=['POST'])
def cambiar(boleto_id):
    """改签/修改车票时间接口"""
    nuevo_dia = request.form['nuevo_dia']
    nuevo_horario = request.form['nuevo_horario']
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE boletos 
        SET dia_seleccionado = ?, horario_seleccionado = ?
        WHERE id = ?
    ''', (nuevo_dia, nuevo_horario, boleto_id))
    conn.commit()
    conn.close()
    
    flash(" ¡Fecha y hora del boleto actualizadas correctamente!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)