import os
import subprocess

HOST_URL = "$HOST"
AUTH_USERNAME = "$USERNAME"
AUTH_PASSWD = "$PASSWORD"

def authenticate():
    subprocess.run(["faraday-cli", "auth", "-f", HOST_URL, "-u", AUTH_USERNAME, "-p", AUTH_PASSWD], check=True)

def triage_workspaces():
    workspaces = subprocess.run(["faraday-cli", "workspace", "list"], capture_output=True, text=True, check=True).stdout
    workspaces = [line.split()[0] for line in workspaces.splitlines()[3:] if line.strip()]

    for workspace in workspaces:
        print(f"Realizando triage del workspace: {workspace}")
        subprocess.run(["faraday-cli", "workspace", "select", workspace], check=True)
        vulns = subprocess.run(["faraday-cli", "vuln", "list", "--workspace", workspace], capture_output=True, text=True, check=True).stdout
        
        vuln_count = len([line for line in vulns.splitlines() if line.strip()])
        print(f"El workspace {workspace} tiene {vuln_count} vulnerabilidades.")

        impact = sum(1 for line in vulns.splitlines() if "impact" in line)
        evidences = sum(1 for line in vulns.splitlines() if "evidences" in line)
        tags = sum(1 for line in vulns.splitlines() if "tags" in line)

        print(f"Impacto: {impact}, Evidencias: {evidences}, Tags: {tags}")

if __name__ == "__main__":
    authenticate()
    triage_workspaces()
