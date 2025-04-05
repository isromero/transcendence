import os

env = "./be/.env"
host = f"OAUTH42_REDIRECT_URI=http://{os.uname().nodename.split('.')[0]}:8000/api/oauth/callback"

with open(env, "r") as f:
    lines = f.readlines()
if lines:
    lines[-1] = host
else:
    lines.append(host)
with open(env, "w") as f:
    f.writelines(lines)
