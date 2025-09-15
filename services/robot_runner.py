import os
import yaml
from robot import run as robot_run

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

    # Prepare variables
    variables = [
        f"WEBHOOK_PATH:{record['webhook_path']}",
        f"PROJECT:{record['project_name']}",
        f"VERSION:{record['version_name']}",
        f"CYCLE:{record['cycle_name']}",
        f"ENV:{record['env']}"
    ]

    # Add folders if present
    if "folders" in record and record["folders"]:
        folder_str = ";".join(record["folders"])
        variables.append(f"FOLDERS_STR:{folder_str}")

    # Run Robot Framework using Python API
    # Don't pass stdout as a string; use default or None
    result_code = robot_run(
        robot_file,
        variable=variables,
        log=None,       # Disable HTML log
        report=None,    # Disable HTML report
        output=None,    # Disable HTML output
        console='NONE'  # Avoid stdout issues
    )

    return result_code, "Robot run finished."