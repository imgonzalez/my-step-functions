import json

class State:
    def __init__(self, name, definition):
        self.name = name
        self.definition = definition

    def execute(self, input_data):
        # Base execute method - to be implemented by subclasses
        raise NotImplementedError

class PassState(State):
    def execute(self, input_data):
        output = self.definition.get('Result', input_data) # Pass state can have a 'Result' field
        next_state = self.definition.get('Next')
        return next_state, output

class StateMachine:
    def __init__(self):
        self.definition = None
        self.states = {}
        self.start_at = None

    def _create_state(self, state_name, state_definition):
        state_type = state_definition.get('Type')
        if state_type == 'Pass':
            return PassState(state_name, state_definition)
        # Add other state types here as they are implemented
        else:
            raise NotImplementedError(f"State type '{state_type}' not supported yet.")

    def load_definition(self, definition):
        self.definition = definition
        self.states = {}
        self.start_at = definition.get('StartAt')
        for state_name, state_definition in definition.get('States', {}).items():
            self.states[state_name] = self._create_state(state_name, state_definition)

    def execute(self, input_data):
        if not self.definition:
            raise ValueError("State machine definition not loaded.")

        current_state_name = self.start_at
        current_input = input_data
        execution_trace = []

        while current_state_name:
            if current_state_name not in self.states:
                raise ValueError(f"State '{current_state_name}' not found.")

            current_state = self.states[current_state_name]

            trace_entry = {
                'state_name': current_state_name,
                'input': current_input,
                'output': None,
                'next_state': None,
                'error': None
            }
            execution_trace.append(trace_entry)

            try:
                next_state_name, output = current_state.execute(current_input)
                current_input = output
                current_state_name = next_state_name
                trace_entry['output'] = output
                trace_entry['next_state'] = next_state_name

            except Exception as e:
                trace_entry['error'] = str(e)
                current_state_name = None # Stop execution on error
                raise e # Re-raise the exception after logging

        return current_input, execution_trace


class TaskState(State):
    def execute(self, input_data):
        # Implementation will involve making HTTP requests
        pass

class ChoiceState(State):
    def execute(self, input_data):
        pass

class WaitState(State):
    def execute(self, input_data):
        pass

class SucceedState(State):
    def execute(self, input_data):
        pass

class FailState(State):
    def execute(self, input_data):
        pass

if __name__ == '__main__':
    # Example Usage (for testing the basic structure)
    sample_asl = {
        "StartAt": "HelloWorld",
        "States": {
            "HelloWorld": {
                "Type": "Pass",
                "Result": "Hello, World!",
                "End": True
            }
        }
    }

    sm = StateMachine()
    sm.load_definition(sample_asl)
    result, trace = sm.execute({})
    print("Result:", result)
    print("Trace:", json.dumps(trace, indent=2))