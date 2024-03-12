/*
 * SPDX-License-Identifier: MIT
 * File     :  parser.js
 * Desc     :  Parser class, to parser the JSON test data into objects
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 */

class Parser {
  parse() {
    let tests = [];

    const json = this._read();
    const test_data = json["tests"];

    let test_id = 0;

    for (const test_key in test_data) {
      let executions = [];
      const executions_json = test_data[test_key]["executions"];
      const test = test_data[test_key];

      for (const execution_key in executions_json) {
        const execution = executions_json[execution_key];

        let steps = [];
        const steps_json = executions_json[execution_key]["steps"];

        for (const steps_key in steps_json) {
          const step = steps_json[steps_key];

          steps.push(new Step(steps_key, step.description, step.outcome));
        }

        executions.push(new Execution(execution_key, execution.device, execution.outcome, execution.duration, steps));
      }

      tests.push(new Test(test_id, test.node_id, test.name, test.description, test.self_test, executions));
      test_id++;
    }

    return tests;
  }

  _read() {
    const json = document.getElementById("test_data").innerText;
    return JSON.parse(json);
  }
}
