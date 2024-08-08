import os
import subprocess

HOST_URL = "$HOST"
AUTH_USERNAME = "$USERNAME"
AUTH_PASSWD = "$PASSWORD"

def authenticate():
    subprocess.run(["faraday-cli", "auth", "-f", HOST_URL, "-u", AUTH_USERNAME, "-p", AUTH_PASSWD], check=True)

def check_schedules():
    workspaces = subprocess.run(["faraday-cli", "workspace", "list"], capture_output=True, text=True, check=True).stdout
    workspaces = [line.split()[0] for line in workspaces.splitlines()[3:] if line.strip()]

    for workspace in workspaces:
        print(f"Verificando el workspace: {workspace}")
        subprocess.run(["faraday-cli", "workspace", "select", workspace], check=True)
        schedule = subprocess.run(["faraday-cli", "schedule", "list", "--workspace", workspace], capture_output=True, text=True, check=True).stdout
        
        if "August" in schedule:
            print(f"El workspace {workspace} tiene tareas programadas para agosto.")
        else:
            print(f"El workspace {workspace} NO tiene tareas programadas para agosto.")

if __name__ == "__main__":
    authenticate()
    check_schedules()
