import re
import os


def get_hostname() -> str:
    hostname = os.popen("hostname").read().strip()
    if re.match(r"^c[1-3]r[1-9]|1[0-9]s[1-6]\.42madrid\.com$", hostname):
        return hostname
    return "localhost"


def update_env_file(env_path, hostname):
    with open(env_path, "r") as file:
        lines = file.readlines()

    with open(env_path, "w") as file:
        for line in lines:
            if line.startswith("OAUTH42_REDIRECT_URI="):
                file.write(
                    f"OAUTH42_REDIRECT_URI=https://{hostname}:8443/api/oauth/callback\n"
                )
            elif line.startswith("OAUTH42_HOSTNAME="):
                file.write(f"OAUTH42_HOSTNAME={hostname}:8443\n")
            else:
                file.write(line)


def update_caddyfile(caddyfile_path, hostname):
    if hostname == "localhost":
        return

    with open(caddyfile_path, "r") as file:
        content = file.read()

    updated_content = re.sub(
        r"https://[^,\s]+\.42madrid\.com,\s*https://localhost",
        f"https://{hostname}, https://localhost",
        content,
    )

    with open(caddyfile_path, "w") as file:
        file.write(updated_content)


def main():
    hostname = get_hostname()
    env_path = ".env"
    caddyfile_path = "./deployment/Caddyfile"

    print(f"Using hostname: {hostname}")
    update_env_file(env_path, hostname)
    update_caddyfile(caddyfile_path, hostname)
    print("Files updated successfully.")


if __name__ == "__main__":
    main()
