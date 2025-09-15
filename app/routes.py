from app import app
from flask import render_template, request
from services.robot_runner import get_phase_names, run_update_jira

@app.route("/", methods=["GET", "POST"])
def index():
    phase_names = get_phase_names()
    result_message = ""

    if request.method == "POST":
        selected_name = request.form.get("phase_name")
        code, _ = run_update_jira(selected_name)  # ignore stdout
        if code is None:
            result_message = "⚠️ Selected test not found in YAML config."
        elif code == 0:
            result_message = "😎 Update Success"
        else:
            result_message = "😱 Update Failed"

    return render_template("index.html", phase_names=phase_names, result_message=result_message)