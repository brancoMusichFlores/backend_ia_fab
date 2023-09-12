import sys
from datetime import datetime

class CDKHelpers:
    # Funcion para crear logs personalizados en terminal
    def f_logs(e_mensaje: Exception, e_nombre_clase: str):
        print("\x1b[31m--------------------E R R O R--------------------")
        print("Error en {}:".format(e_nombre_clase))
        print("❌ \x1b[36m {} -->  \x1b[33m ".format(datetime.now()), e_mensaje.args, " \x1b[31m")
        print("-------------------------------------------------\x1b[0m")

    def f_falta_configuracion(e_mensaje:str , e_nombre_clase: str):
        print("\x1b[31m--------------------E R R O R--------------------")
        print("Falta configuracion en {}:".format(e_nombre_clase))
        print("❌ \x1b[36m {} -->  \x1b[33m ".format(datetime.now()) + e_mensaje + " \x1b[31m")
        print("-------------------------------------------------\x1b[0m")
        sys.exit("\x1b[31mFalla al levantar")