import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/swissbyte', methods=['POST'])
def testing():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    
    # my code starts here
    code = iter(data["code"])
    cases = data["cases"]
    outcomes = []

    for case in cases:
        variables = case.copy()
        is_solvable = True

        code = iter(data["code"])
        # logging.info(f"case: {case}")

        for line in code:
            line = line.strip()
            # logging.info(line)

            if line.startswith("if"):
                condition = line[2:].strip()
                # logging.info(f"condition: {condition}")
                # Evaluate the condition based on the current variable states
                try:
                    if eval(condition, {}, variables):
                        # logging.info("condition is true")
                        continue  # Condition is true, continue to the next line
                    else:
                        # logging.info("condition is false")
                        # Condition is false, skip to the next line after the endif
                        while not line.startswith("endif"):
                            line = next(code)
                except (SyntaxError, NameError):
                    is_solvable = False
                    break

            elif line.startswith("fail"):
                is_solvable = False
                break

            else:
                try:
                    # Assign the value as an integer explicitly
                    exec(line, {}, variables)
                    for key, value in variables.items():
                        if isinstance(value, float):
                            variables[key] = int(value)
                except (SyntaxError, NameError):
                    is_solvable = False
                    break

        outcome = {"is_solvable": is_solvable, "variables": variables}
        outcomes.append(outcome)

    result = {"outcomes": outcomes}
    # my code ends here

    # logging.info("My result :{}".format(result))
    return json.dumps(result)
