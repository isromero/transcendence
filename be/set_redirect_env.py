import os

archivo = "./be/.env"
host = f"OAUTH42_REDIRECT_URI=http://{os.uname().nodename.split('.')[0]}:8000/auth/callback/"

with open(archivo, "r") as f:
    lineas = f.readlines()
if lineas:
    lineas[-1] = host
else:
    lineas.append(host)
with open(archivo, "w") as f:
    f.writelines(lineas)