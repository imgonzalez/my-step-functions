import os

import json
from flask import Flask, send_file, request, jsonify
from step_functions_emulator.engine import StateMachine

state_machines = {}

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/state-machine", methods=["POST"])
def upload_state_machine_definition():
    definition = request.json
    if not definition:
        return jsonify({"error": "Invalid ASL definition provided"}), 400

    try:
        sm = StateMachine()
        sm.load_definition(definition)
        # Use a simple name or generate an ID for the state machine
        state_machine_name = definition.get("Comment", "default-state-machine")
        state_machines[state_machine_name] = sm
        return jsonify({"message": f"State machine '{state_machine_name}' uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/execute", methods=["POST"])
def execute_state_machine():
    execution_input = request.json
    state_machine_name = execution_input.get("stateMachineName", "default-state-machine")
    input_data = execution_input.get("input", {})

    sm = state_machines.get(state_machine_name)
    if not sm:
        return jsonify({"error": f"State machine '{state_machine_name}' not found"}), 404

    result = sm.execute(input_data)
    return jsonify({"result": result}), 200

@app.route("/execute-example", methods=["GET"])
def execute_example_workflow():
    with open("/home/user/my-step-functions/samples/example_workflow_3.json", "r") as f:
        definition = json.load(f)

    sm = StateMachine()
    sm.load_definition(definition)

    # Execute with some sample input, or no input
    result = sm.execute({"att": "hi"})

    return jsonify({"result": result}), 200
