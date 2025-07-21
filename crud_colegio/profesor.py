from db import conectar

def validar_rut(rut):
    return len(rut.strip()) > 0

def validar_nombre(nombre):
    return len(nombre.strip()) > 0

def existe_profesor(rut):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM profesor WHERE rut = %s", (rut,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def crear_profesor():
    while True:
        rut = input("RUT: ").strip()
        if not validar_rut(rut):
            print("RUT inválido.")
            continue
        if existe_profesor(rut):
            print(f"Ya existe un profesor con RUT {rut}. Intente otro.")
            continue
        
        nombres = input("Nombres: ").strip()
        if not validar_nombre(nombres):
            print("Nombre inválido.")
            continue
        
        apellido_paterno = input("Apellido paterno: ").strip()
        if not validar_nombre(apellido_paterno):
            print("Apellido paterno inválido.")
            continue
        
        apellido_materno = input("Apellido materno: ").strip()
        if not validar_nombre(apellido_materno):
            print("Apellido materno inválido.")
            continue
        
        direccion = input("Dirección: ").strip()
        if len(direccion) == 0:
            print("Dirección no puede estar vacía.")
            continue
        
        ciudad = input("Ciudad: ").strip()
        if len(ciudad) == 0:
            print("Ciudad no puede estar vacía.")
            continue

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO profesor (rut, nombres, apellido_paterno, apellido_materno, direccion, ciudad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (rut, nombres, apellido_paterno, apellido_materno, direccion, ciudad))
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Profesor insertado correctamente.")
            break
        except Exception as e:
            print(f"Error al insertar profesor: {e}")
            break

def listar_profesores():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profesor")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

def actualizar_profesor():
    rut = input("RUT del profesor a actualizar: ").strip()
    if not existe_profesor(rut):
        print("Profesor no encontrado.")
        return
    
    nombres = input("Nuevo nombre: ").strip()
    apellido_paterno = input("Nuevo apellido paterno: ").strip()
    apellido_materno = input("Nuevo apellido materno: ").strip()
    direccion = input("Nueva dirección: ").strip()
    ciudad = input("Nueva ciudad: ").strip()

    # Opcional: validar aquí también, como antes

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE profesor SET nombres=%s, apellido_paterno=%s, apellido_materno=%s, direccion=%s, ciudad=%s
            WHERE rut=%s
        """, (nombres, apellido_paterno, apellido_materno, direccion, ciudad, rut))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Profesor actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar profesor: {e}")

def eliminar_profesor():
    rut = input("RUT del profesor a eliminar: ").strip()
    if not existe_profesor(rut):
        print("Profesor no encontrado.")
        return
    
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM profesor WHERE rut=%s", (rut,))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Profesor eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar profesor: {e}")

def menu_profesor():
    while True:
        print("\n📚 MENÚ PROFESOR")
        print("1. Listar")
        print("2. Insertar")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Salir")
        opcion = input("Elige: ")
        if opcion == '1':
            listar_profesores()
        elif opcion == '2':
            crear_profesor()
        elif opcion == '3':
            actualizar_profesor()
        elif opcion == '4':
            eliminar_profesor()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida.")
