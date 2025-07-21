from db import conectar

def validar_rut(rut):
    return len(rut.strip()) > 0

def validar_nombre(nombre):
    return len(nombre.strip()) > 0

def existe_apoderado(rut):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM apoderado WHERE rut = %s", (rut,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def crear_apoderado():
    while True:
        rut = input("RUT: ").strip()
        if not validar_rut(rut):
            print("RUT inválido. Intente de nuevo.")
            continue
        if existe_apoderado(rut):
            print(f"El apoderado con RUT {rut} ya existe. Intente con otro.")
            continue

        nombres = input("Nombres: ").strip()
        if not validar_nombre(nombres):
            print("Nombre inválido. Intente de nuevo.")
            continue

        apellido_paterno = input("Apellido paterno: ").strip()
        apellido_materno = input("Apellido materno: ").strip()
        direccion = input("Dirección: ").strip()
        ciudad = input("Ciudad: ").strip()

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO apoderado (rut, nombres, apellido_paterno, apellido_materno, direccion, ciudad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (rut, nombres, apellido_paterno, apellido_materno, direccion, ciudad))
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Apoderado insertado correctamente.")
            break
        except Exception as e:
            print(f"Error al insertar apoderado: {e}")
            break

def listar_apoderados():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apoderado")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def actualizar_apoderado():
    rut = input("RUT del apoderado a actualizar: ").strip()
    if not existe_apoderado(rut):
        print("Apoderado no encontrado.")
        return

    nombres = input("Nuevo nombre: ").strip()
    apellido_paterno = input("Nuevo apellido paterno: ").strip()
    apellido_materno = input("Nuevo apellido materno: ").strip()
    direccion = input("Nueva dirección: ").strip()
    ciudad = input("Nueva ciudad: ").strip()

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE apoderado SET nombres=%s, apellido_paterno=%s, apellido_materno=%s, direccion=%s, ciudad=%s
            WHERE rut=%s
        """, (nombres, apellido_paterno, apellido_materno, direccion, ciudad, rut))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Apoderado actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar apoderado: {e}")

def eliminar_apoderado():
    rut = input("RUT del apoderado a eliminar: ").strip()
    if not existe_apoderado(rut):
        print("Apoderado no encontrado.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM apoderado WHERE rut=%s", (rut,))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Apoderado eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar apoderado: {e}")

def menu_apoderado():
    while True:
        print("\n👨‍👩‍👧 MENÚ APODERADO")
        print("1. Listar")
        print("2. Insertar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Salir")
        opcion = input("Elige: ")
        if opcion == '1':
            listar_apoderados()
        elif opcion == '2':
            crear_apoderado()
        elif opcion == '3':
            actualizar_apoderado()
        elif opcion == '4':
            eliminar_apoderado()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida.")
