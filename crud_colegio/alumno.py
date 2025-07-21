from db import conectar
from datetime import datetime

def validar_rut(rut):
    return len(rut.strip()) > 0  # Puedes mejorar con regex

def validar_nombre(nombre):
    return len(nombre.strip()) > 0

def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except:
        return False

def existe_alumno(rut):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM alumno WHERE rut = %s", (rut,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def crear_alumno():
    while True:
        rut = input("RUT: ").strip()
        if not validar_rut(rut):
            print("RUT inválido. Intente de nuevo.")
            continue
        if existe_alumno(rut):
            print(f"El alumno con RUT {rut} ya existe. Intente con otro.")
            continue

        nombres = input("Nombres: ").strip()
        if not validar_nombre(nombres):
            print("Nombre inválido. Intente de nuevo.")
            continue

        apellido_paterno = input("Apellido paterno: ").strip()
        apellido_materno = input("Apellido materno: ").strip()

        fecha_nacimiento = input("Fecha nacimiento (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha_nacimiento):
            print("Fecha inválida. Intente de nuevo.")
            continue

        direccion = input("Dirección: ").strip()
        ciudad = input("Ciudad: ").strip()
        codigo_curso = input("Código curso: ").strip()

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO alumno (rut, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, ciudad, codigo_curso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (rut, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, ciudad, codigo_curso))
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Alumno insertado correctamente.")
            break
        except Exception as e:
            print(f"Error al insertar alumno: {e}")
            # Opcional: preguntar si quiere intentar de nuevo o salir
            break

def listar_alumnos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alumno ORDER BY rut")
    filas = cur.fetchall()
    if filas:
        for row in filas:
            print(row)
    else:
        print("No hay alumnos registrados.")
    cur.close()
    conn.close()

def actualizar_alumno():
    rut = input("RUT del alumno a actualizar: ").strip()
    if not existe_alumno(rut):
        print("Alumno no encontrado.")
        return

    nombres = input("Nuevo nombre: ").strip()
    apellido_paterno = input("Nuevo apellido paterno: ").strip()
    apellido_materno = input("Nuevo apellido materno: ").strip()
    fecha_nacimiento = input("Nueva fecha nacimiento (YYYY-MM-DD): ").strip()
    if not validar_fecha(fecha_nacimiento):
        print("Fecha inválida.")
        return
    direccion = input("Nueva dirección: ").strip()
    ciudad = input("Nueva ciudad: ").strip()
    codigo_curso = input("Nuevo código curso: ").strip()

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE alumno SET nombres=%s, apellido_paterno=%s, apellido_materno=%s, fecha_nacimiento=%s, direccion=%s, ciudad=%s, codigo_curso=%s
            WHERE rut=%s
        """, (nombres, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, ciudad, codigo_curso, rut))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Alumno actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar alumno: {e}")

def eliminar_alumno():
    rut = input("RUT del alumno a eliminar: ").strip()
    if not existe_alumno(rut):
        print("Alumno no encontrado.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM alumno WHERE rut=%s", (rut,))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Alumno eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar alumno: {e}")

def menu_alumno():
    while True:
        print("\n🎓 MENÚ ALUMNO")
        print("1. Listar alumnos")
        print("2. Insertar alumno")
        print("3. Actualizar alumno")
        print("4. Eliminar alumno")
        print("0. Volver")
        opcion = input("Elige: ").strip()
        if opcion == '1':
            listar_alumnos()
        elif opcion == '2':
            crear_alumno()
        elif opcion == '3':
            actualizar_alumno()
        elif opcion == '4':
            eliminar_alumno()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

