from db import conectar

def validar_codigo(codigo):
    try:
        c = int(codigo)
        return c > 0
    except:
        return False

def validar_nombre(nombre):
    return len(nombre.strip()) > 0

def validar_dia(dia):
    try:
        d = int(dia)
        return 1 <= d <= 7  # Ajusta según convención usada
    except:
        return False

def validar_hora(hora):
    try:
        h = int(hora)
        return 0 <= h <= 23
    except:
        return False

def validar_cupos(cupos):
    try:
        c = int(cupos)
        return c >= 0
    except:
        return False

def existe_extraprogramatico(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM extraprogramatica WHERE codigo = %s", (codigo,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def crear_extraprogramatico():
    while True:
        codigo = input("Código: ").strip()
        if not validar_codigo(codigo):
            print("Código inválido. Debe ser un entero positivo.")
            continue
        if existe_extraprogramatico(codigo):
            print(f"Ya existe una actividad con código {codigo}.")
            continue

        nombre = input("Nombre: ").strip()
        if not validar_nombre(nombre):
            print("Nombre inválido.")
            continue

        dia = input("Día (1=Lunes...): ").strip()
        if not validar_dia(dia):
            print("Día inválido. Debe estar entre 1 y 7.")
            continue

        hora_inicio = input("Hora inicio (0-23): ").strip()
        if not validar_hora(hora_inicio):
            print("Hora inicio inválida.")
            continue

        hora_fin = input("Hora fin (0-23): ").strip()
        if not validar_hora(hora_fin):
            print("Hora fin inválida.")
            continue
        if int(hora_fin) <= int(hora_inicio):
            print("Hora fin debe ser mayor que hora inicio.")
            continue

        cupos = input("Cupos: ").strip()
        if not validar_cupos(cupos):
            print("Cupos inválidos. Debe ser un entero >= 0.")
            continue

        lugar = input("Lugar: ").strip()
        if not lugar:
            print("Lugar no puede estar vacío.")
            continue

        rut_profesor = input("RUT profesor: ").strip()
        if not rut_profesor:
            print("RUT profesor no puede estar vacío.")
            continue

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO extraprogramatica (codigo, nombre, dia, hora_inicio, hora_fin, cupos, lugar, rut_profesor)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, dia, hora_inicio, hora_fin, cupos, lugar, rut_profesor))
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Actividad insertada correctamente.")
            break
        except Exception as e:
            print(f"Error al insertar actividad: {e}")
            break

def listar_extraprogramaticas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM extraprogramatica")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def actualizar_extraprogramatico():
    codigo = input("Código de la actividad a actualizar: ").strip()
    if not existe_extraprogramatico(codigo):
        print("Actividad no encontrada.")
        return

    nombre = input("Nuevo nombre: ").strip()
    if not validar_nombre(nombre):
        print("Nombre inválido.")
        return

    dia = input("Nuevo día (1-7): ").strip()
    if not validar_dia(dia):
        print("Día inválido.")
        return

    hora_inicio = input("Nueva hora inicio (0-23): ").strip()
    if not validar_hora(hora_inicio):
        print("Hora inicio inválida.")
        return

    hora_fin = input("Nueva hora fin (0-23): ").strip()
    if not validar_hora(hora_fin):
        print("Hora fin inválida.")
        return
    if int(hora_fin) <= int(hora_inicio):
        print("Hora fin debe ser mayor que hora inicio.")
        return

    cupos = input("Nuevos cupos: ").strip()
    if not validar_cupos(cupos):
        print("Cupos inválidos.")
        return

    lugar = input("Nuevo lugar: ").strip()
    if not lugar:
        print("Lugar no puede estar vacío.")
        return

    rut_profesor = input("Nuevo RUT profesor: ").strip()
    if not rut_profesor:
        print("RUT profesor no puede estar vacío.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE extraprogramatica SET nombre=%s, dia=%s, hora_inicio=%s, hora_fin=%s, cupos=%s, lugar=%s, rut_profesor=%s
            WHERE codigo=%s
        """, (nombre, dia, hora_inicio, hora_fin, cupos, lugar, rut_profesor, codigo))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Actividad actualizada correctamente.")
    except Exception as e:
        print(f"Error al actualizar actividad: {e}")

def eliminar_extraprogramatico():
    codigo = input("Código de la actividad a eliminar: ").strip()
    if not existe_extraprogramatico(codigo):
        print("Actividad no encontrada.")
        return
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM extraprogramatica WHERE codigo=%s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Actividad eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar actividad: {e}")

def menu_extraprogramatico():
    while True:
        print("\n🏀 MENÚ EXTRA PROGRAMÁTICA")
        print("1. Listar")
        print("2. Insertar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Salir")
        opcion = input("Elige: ")
        if opcion == '1':
            listar_extraprogramaticas()
        elif opcion == '2':
            crear_extraprogramatico()
        elif opcion == '3':
            actualizar_extraprogramatico()
        elif opcion == '4':
            eliminar_extraprogramatico()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida.")
