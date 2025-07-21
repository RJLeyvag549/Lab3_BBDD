import psycopg2

def conectar():
    return psycopg2.connect(
        host="pgsqltrans.face.ubiobio.cl",
        database="rleyva_bd",
        user="rleyva",
        password="pass123"
    )
