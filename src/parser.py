import pandas as pd
import re

from pathlib import Path

def parse_line(linea, patron_general, dic_patron):

    pat_com = re.compile(patron_general)
    str = pat_com.search(linea)

    dic_linea = str.groupdict()
    
    for patron in dic_patron:
        comprobar = re.compile(dic_patron[patron])
        str_mensaje = comprobar.search(dic_linea["message"])
        if str_mensaje:
            dic_mensaje = str_mensaje.groupdict()
            dic_mensaje["event_type"] = patron
            dic_linea = dic_linea | dic_mensaje
            break
        else:
            dic_linea["event_type"] = "other"
            
    return dic_linea


def parse_file(contenido, patron_general, dic_patron):    
    
    valores = []

    for linea in contenido:
        valores.append(parse_line(linea, patron_general, dic_patron))

    return pd.DataFrame(data=valores)

def leer_log(path):
    with open(path, "r", encoding= "utf-8") as archivo:
        return archivo.read().split("\n")

ruta = (Path(__file__).resolve().parent.parent/"data"/"sample_ssh.log")

PATRON_GENERAL = r"(?P<month>\S{3}) +(?P<day>\d+) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) sshd\[(?P<num_process>\d+)\]: (?P<message>.+)"

DIC_PATRON = {
    "invalid_user" : r"Invalid user +(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)",
    "failed_password" : r"Failed password for (?P<user_error>invalid user +)?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+) port (?P<port>\d+) ssh2",
    "accepted_password" : r"Accepted password for (?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+) port (?P<port>\d+) ssh2"
}


df = parse_file(leer_log(ruta), PATRON_GENERAL, DIC_PATRON)
