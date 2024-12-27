import sqlite3

db_path = "database.db"
conection = sqlite3.connect(db_path)
cursor = conection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        descripcion TEXT NOT NULL,
                        stock INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        categoria TEXT NOT NULL
                    )'''
               )

def getProductDetails():
    name = input("Ingrese el nombre del producto: ").capitalize()
    description = input("Descripcion: ").capitalize()
    
    stock = 0
    while stock <= 0:
        try:
            stock = int(input("Cantidad: "))
            if stock <= 0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
    
    price = 0
    while price <= 0:
        try:
            price = float(input("Precio: "))
            if price <= 0:
                print("Ingrese un numero mayor que 0")
            else:
                # Redondear a 2 decimales
                price = round(price, 2)    
        except ValueError:
            print("Ingrese un numero")
    
    category = input("Categoria: ").capitalize()
    return name, description, stock, price, category

def addProduct():
    product_details = getProductDetails()
    conection = sqlite3.connect("./database.db")
    cursor = conection.cursor()
    cursor.execute("INSERT INTO productos (nombre, descripcion, stock, precio, categoria) VALUES (?, ?, ?, ?, ?)", product_details )
    conection.commit()
    print(f"Producto {product_details[0]} agregado con exito")
    conection.close()

def showProducts(productos = 0, unico_producto = False):
    if productos == 0:
        conection = sqlite3.connect("./database.db")
        cursor = conection.cursor()
        cursor.execute("SELECT * FROM productos")
        result = cursor.fetchall()
        #print(resultados)
        for product in result:
            print("ID:", product[0], "Nombre:", product[1], "Descripcion:", product[2], "Stock:", product[3], "Precio:", product[4], "Categoria:", product[5])
        conection.close()
    else:
        if unico_producto:
            print("ID:", productos[0], "Nombre:", productos[1], "Descripcion:", productos[2], "Stock:", productos[3], "Precio:", productos[4], "Categoria", productos[5])
        else:
            for product in productos:
                print("ID:", product[0], "Nombre:", product[1], "Descripcion:", product[2], "Stock:", product[3], "Precio:", product[4], "Categoria", product[5])
        
def updateProduct():
    showProducts()
    codigo = 0
    while codigo <= 0:
        try:
            codigo = int(input("Ingrese el codigo del producto que desea modificar: "))
            if codigo <=0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            codigo = 0
    nombre = input("Ingrese el nuevo nombre del producto: ")
    descripcion = input("Ingrese la nueva descripcion del producto: ")
    stock = 0
    while stock <= 0:
        try:
            stock = int(input("Ingrese el nuevo stock: "))
            if stock <0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            stock = 0
    precio = 0
    while precio <= 0:
        try:
            precio = int(input("Ingrese el nuevo precio: "))
            if precio <= 0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            precio = 0
    categoria = input("Ingrese la nueva categoria: ")
    conexion = sqlite3.connect("./database.db")
    cursor = conexion.cursor()
    #comando = f"UPDATE FROM productos SET nombre = {nombre}, descripcion = {descripcion}, stock = {stock}, precio = {precio}, categoria = {categoria} WHERE id = {codigo}"
    cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, stock = ?, precio = ?, 
                   categoria = ? WHERE id = ?''', (nombre, descripcion, stock, precio, categoria, codigo))
    conexion.commit()
    conexion.close()
    showProducts()

def deleteProduct():
    showProducts()
    codigo = 0
    while codigo <= 0:
        try:
            codigo = int(input("Ingrese el codigo del producto que desea eliminar: "))
            if codigo <=0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            codigo = 0
    try: 
        with sqlite3.connect("./database.db") as cursor:
            cursor.execute("DELETE FROM productos WHERE id = ?", (codigo, ))
            print("Producto eliminado")
    except ValueError:
        print("Codigo incorrecto")

def lowStockReport():
    valor_bajo = 0
    while valor_bajo <= 0:
        try:
            valor_bajo = int(input("Ingrese la cantidad minima de stock: "))
            if valor_bajo <=0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            valor_bajo = 0
    conexion = sqlite3.connect("./database.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE stock <= ?",(valor_bajo,))
    resultados = cursor.fetchall()
    if len(resultados) > 0:
        print(resultados)
        showProducts(resultados)
    else:
        print("No hay productos con bajo stock")
    conexion.close()
        
def searchProductByName():
    nombre = input("Ingrese el nombre del producto a buscar: ").capitalize()
    conexion = sqlite3.connect("./base-de-datos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?",(nombre,))
    #contador = cursor.fetchone()[0]
    resultados = cursor.fetchone()
    #print(resultados)
    if resultados != None:
        showProducts(resultados, True)
    else:
        print("Registro no encontrado")
    conexion.close()

def showMenu():
    print("Gestion de inventario")
    print("1. Agregar producto")
    print("2. Mostrar todos los productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Reporte de bajo stock")
    print("6. Buscar producto")
    print("7. Salir")

def main():
    menu = True
    while menu:
        showMenu()
        option = input("Ingrese la opcion deseada: ")

        match option:
                    case "1":
                        addProduct()
                    case "2":
                        showProducts()
                    case "3":
                        updateProduct()
                    case "4":
                        deleteProduct()
                    case "5":
                        lowStockReport()
                    case "6":
                        searchProductByName()
                    case "7":
                        menu = False
                    case _:
                        print("Opcion incorrecta\n")

main()