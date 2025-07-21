from alumno import menu_alumno
from profesor import menu_profesor
from curso import menu_curso
from apoderado import menu_apoderado
from extraprogramatico import menu_extraprogramatico
from asignaciones import asignar_ciclo_curso, asignar_apoderado, asignar_extraprogramatica, asignar_especialidad
from db import conectar


def consulta_q1():
    print("\n📊 Consulta Q1 - Alumnos, curso, profesor jefe y apoderado vigente en 2025")
    conn = conectar()
    cur = conn.cursor()
    
    query = """
        SELECT a.nombres, c.codigo AS curso,
               p.nombres AS profesor_jefe_nombre, p.apellido_paterno AS profesor_jefe_apellido,
               ap.nombres AS apoderado_nombre
        FROM alumno a
        JOIN curso c ON a.codigo_curso = c.codigo
        JOIN es_jefe ej ON c.codigo = ej.codigo_curso
        JOIN profesor p ON ej.rut_profesor_jefe = p.rut
        JOIN representa r ON a.rut = r.rut_alumno
        JOIN apoderado ap ON r.rut_apoderado = ap.rut
        WHERE c.anio = 2025
    """

    try:
        cur.execute(query)
        rows = cur.fetchall()
        if rows:
            print("\nResultados:")
            for row in rows:
                print(f"Alumno: {row[0]}, Curso: {row[1]}, Profesor Jefe: {row[2]} {row[3]}, Apoderado vigente: {row[4]}")
        else:
            print("No se encontraron resultados.")
    except Exception as e:
        print(f"❌ Error al ejecutar la consulta: {e}")
    finally:
        cur.close()
        conn.close()

def main():
    while True:
        print("\n🏫 MENÚ PRINCIPAL")
        print("1. Alumnos")
        print("2. Profesores")
        print("3. Cursos")
        print("4. Apoderados")
        print("5. Extra programáticas")
        print("6. Ejecutar consulta Q1")
        print("6. Consulta Q1")
        print("7. Asignar ciclo y curso")
        print("8. Asignar apoderado")
        print("9. Asignar extraprogramática")
        print("10. Asignar especialidad")
        print("0. Salir")
        opcion = input("Elige una opción: ")
        if opcion == '1':
            menu_alumno()
        elif opcion == '2':
            menu_profesor()
        elif opcion == '3':
            menu_curso()
        elif opcion == '4':
            menu_apoderado()
        elif opcion == '5':
            menu_extraprogramatico()
        elif opcion == '6':
            consulta_q1()
        elif opcion == '7':
            asignar_ciclo_curso()
        elif opcion == '8':
          asignar_apoderado()
        elif opcion == '9':
          asignar_extraprogramatica()
        elif opcion == '10':
            asignar_especialidad()
        elif opcion == '0':
            print("¡Adiós!")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    main()
