from db import conectar

def existe_curso(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM curso WHERE codigo=%s", (codigo,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r is not None

def existe_profesor(rut):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM profesor WHERE rut=%s", (rut,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r is not None

def existe_alumno(rut):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM alumno WHERE rut=%s", (rut,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r is not None

def existe_apoderado(rut):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM apoderado WHERE rut=%s", (rut,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r is not None

def existe_actividad(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM extraprogramatica WHERE codigo=%s", (codigo,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r is not None

def existe_especialidad(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM especialidad WHERE codigo=%s", (codigo,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r is not None

# --------------------------
def asignar_ciclo_curso():
    while True:
        codigo = input("Código del curso: ")
        if existe_curso(codigo):
            break
        print("❌ Curso no existe, ingresa de nuevo.")

    while True:
        rut_jefe = input("RUT del profesor jefe: ")
        if existe_profesor(rut_jefe):
            break
        print("❌ Profesor jefe no existe, ingresa de nuevo.")

    tipo = input("¿Es media o basica? ").strip().lower()

    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO es_jefe (codigo_curso, rut_profesor_jefe) VALUES (%s, %s)", (codigo, rut_jefe))

        if tipo == 'media':
            orientacion = input("Orientación: ")
            cur.execute("INSERT INTO media (codigo_curso, orientacion) VALUES (%s, %s)", (codigo, orientacion))
        elif tipo == 'basica':
            while True:
                rut_asistente = input("RUT del profesor asistente: ")
                if existe_profesor(rut_asistente):
                    break
                print("❌ Profesor asistente no existe, ingresa de nuevo.")
            cur.execute("INSERT INTO basica (codigo_curso) VALUES (%s)", (codigo,))
            cur.execute("INSERT INTO es_asistente (codigo_curso, rut_profesor_asistente) VALUES (%s, %s)", (codigo, rut_asistente))
        else:
            print("❌ Tipo inválido, debe ser 'media' o 'basica'.")
            conn.rollback()
            return

        conn.commit()
        print("✅ Ciclo asignado correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

# --------------------------
def asignar_apoderado():
    while True:
        rut_alumno = input("RUT del alumno: ")
        if existe_alumno(rut_alumno):
            break
        print("❌ Alumno no existe, ingresa de nuevo.")

    while True:
        rut_apoderado = input("RUT del apoderado: ")
        if existe_apoderado(rut_apoderado):
            break
        print("❌ Apoderado no existe, ingresa de nuevo.")

    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_termino = input("Fecha termino (YYYY-MM-DD): ")

    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO representa (rut_alumno, rut_apoderado, fecha_inicio, fecha_termino)
            VALUES (%s, %s, %s, %s)
        """, (rut_alumno, rut_apoderado, fecha_inicio, fecha_termino))
        conn.commit()
        print("✅ Apoderado asignado correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

# --------------------------
def asignar_extraprogramatica():
    while True:
        rut = input("RUT del alumno: ")
        if existe_alumno(rut):
            break
        print("❌ Alumno no existe, ingresa de nuevo.")

    while True:
        codigo = input("Código de la actividad: ")
        if existe_actividad(codigo):
            break
        print("❌ Actividad no existe, ingresa de nuevo.")

    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO participa (rut_alumno, codigo) VALUES (%s, %s)", (rut, codigo))
        conn.commit()
        print("✅ Actividad asignada correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

# --------------------------
def mostrar_especialidades():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT codigo, descripcion FROM especialidad")
    print("📚 Especialidades disponibles:")
    for codigo, desc in cur.fetchall():
        print(f"{codigo}: {desc}")
    cur.close()
    conn.close()

def asignar_especialidad():
    while True:
        rut = input("RUT del profesor: ")
        if existe_profesor(rut):
            break
        print("❌ Profesor no existe, ingresa de nuevo.")

    mostrar_especialidades()

    while True:
        codigo = input("Código de la especialidad: ")
        if existe_especialidad(codigo):
            break
        print("❌ Especialidad no existe, ingresa de nuevo.")

    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO tiene (rut_profesor, codigo_especialidad) VALUES (%s, %s)", (rut, codigo))
        conn.commit()
        print("✅ Especialidad asignada correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()
