
import os
import subprocess
from datetime import datetime, timedelta

HOST_URL = "$HOST"
AUTH_USERNAME = "$USERNAME"
AUTH_PASSWD = "$PASSWORD"

def authenticate():
    subprocess.run(["faraday-cli", "auth", "-f", HOST_URL, "-u", AUTH_USERNAME, "-p", AUTH_PASSWD], check=True)

def check_recent_scans():
    workspaces = subprocess.run(["faraday-cli", "workspace", "list"], capture_output=True, text=True, check=True).stdout
    workspaces = [line.split()[0] for line in workspaces.splitlines()[3:] if line.strip()]

    three_months_ago = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    for workspace in workspaces:
        print(f"Verificando scans recientes en el workspace: {workspace}")
        subprocess.run(["faraday-cli", "workspace", "select", workspace], check=True)
        reports = subprocess.run(["faraday-cli", "report", "list", "--workspace", workspace], capture_output=True, text=True, check=True).stdout
        
        recent_report = max([line.split()[0] for line in reports.splitlines() if line.strip()], default="1970-01-01")
        
        if recent_report > three_months_ago:
            print(f"El workspace {workspace} tiene reportes recientes.")
        else:
            print(f"El workspace {workspace} NO tiene reportes recientes.")

if __name__ == "__main__":
    authenticate()
    check_recent_scans()
