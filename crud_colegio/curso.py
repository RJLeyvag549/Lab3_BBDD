from db import conectar

def validar_codigo(codigo):
    try:
        c = int(codigo)
        return c > 0
    except:
        return False

def validar_anio(anio):
    try:
        a = int(anio)
        return 1900 <= a <= 2100
    except:
        return False

def existe_curso(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM curso WHERE codigo = %s", (codigo,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def crear_curso():
    while True:
        codigo = input("Código del curso: ").strip()
        if not validar_codigo(codigo):
            print("Código inválido. Debe ser un entero positivo.")
            continue
        if existe_curso(codigo):
            print(f"El curso con código {codigo} ya existe.")
            continue

        anio = input("Año: ").strip()
        if not validar_anio(anio):
            print("Año inválido. Debe estar entre 1900 y 2100.")
            continue

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO curso (codigo, anio)
                VALUES (%s, %s)
            """, (codigo, anio))
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Curso insertado correctamente.")
            break
        except Exception as e:
            print(f"Error al insertar curso: {e}")
            break

def listar_cursos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM curso")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def actualizar_curso():
    codigo = input("Código del curso a actualizar: ").strip()
    if not existe_curso(codigo):
        print("Curso no encontrado.")
        return

    anio = input("Nuevo año: ").strip()
    if not validar_anio(anio):
        print("Año inválido. Debe estar entre 1900 y 2100.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE curso SET anio=%s WHERE codigo=%s
        """, (anio, codigo))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Curso actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar curso: {e}")

def eliminar_curso():
    codigo = input("Código del curso a eliminar: ").strip()
    if not existe_curso(codigo):
        print("Curso no encontrado.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM curso WHERE codigo=%s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Curso eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar curso: {e}")

def menu_curso():
    while True:
        print("\n📖 MENÚ CURSO")
        print("1. Listar")
        print("2. Insertar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Salir")
        opcion = input("Elige: ")
        if opcion == '1':
            listar_cursos()
        elif opcion == '2':
            crear_curso()
        elif opcion == '3':
            actualizar_curso()
        elif opcion == '4':
            eliminar_curso()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida.")
