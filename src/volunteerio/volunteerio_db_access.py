# volunteerio_db_ssm_access.py
import subprocess
import sys
from volunteerio.db_config import remote_host, instance_id

# ---------------- CONFIG ----------------
remote_port = 5432
local_port = 15432
# ---------------------------------------

# Start SSM port forwarding session
try:
    print("Starting SSM port forwarding session...")
    command = [
        "aws",
        "ssm",
        "start-session",
        "--target",
        instance_id,
        "--document-name",
        "AWS-StartPortForwardingSessionToRemoteHost",
        "--parameters",
        f'{{"host":["{remote_host}"],"portNumber":["{remote_port}"],"localPortNumber":["{local_port}"]}}',
    ]
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print("Error starting SSM session:", e)
    sys.exit(1)

print(f"Tunnel open: connect pgAdmin or psql to localhost:{local_port}")
