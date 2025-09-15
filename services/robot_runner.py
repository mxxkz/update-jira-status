import subprocess, os, re, yaml
from services.ZephyrLibraryUat import ZephyrLibraryUat

CONFIG_FILE = "config/data.yml"

def get_phase_names():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    return [record["name"] for record in config["data"]]

def run_update_jira(selected_name):
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    record = next((r for r in config["data"] if r["name"] == selected_name), None)
    if not record:
        return None, "⚠️ Selected test not found in YAML config."

    robot_file = os.path.join("services", "SQ4_Update_Jira_UAT.robot")

    # base command
    cmd = [
        "robot",
        "--variable", f"WEBHOOK_PATH:{record['webhook_path']}",
        "--variable", f"PROJECT:{record['project_name']}",
        "--variable", f"VERSION:{record['version_name']}",
        "--variable", f"CYCLE:{record['cycle_name']}",
        "--variable", f"ENV:{record['env']}",
    ]

    # Only add folders if present in YAML
    if "folders" in record and record["folders"]:
        for folder in record["folders"]:
            folder_str = ";".join(record['folders'])
        cmd.extend(["--variable", f"FOLDERS_STR:{folder_str}"])


    cmd.append(robot_file)

    process = subprocess.run(cmd, capture_output=True, text=True)
    output_str = re.sub(r"^(Output:.*|Log:.*|Report:.*)\n?", "", process.stdout, flags=re.MULTILINE).strip()

    return process.returncode, output_str