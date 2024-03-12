/*
 * SPDX-License-Identifier: MIT
 * File     :  test-filter.js
 * Desc     :  OverviewFilter class, to filter the test data of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  02/01/2024
 * Version  :  1.0
 */

class TestFilter {
  tests(tests, passed_active, failed_active, skipped_active) {
    let filtered_tests = [];

    for (let i = 0; i < tests.length; i++) {
      const test = tests[i];
      const filtered_test = this.test(test, passed_active, failed_active, skipped_active);
      if (filtered_test) {
        filtered_tests.push(filtered_test);
      }
    }

    return filtered_tests;
  }

  test(test, passed_active, failed_active, skipped_active) {
    let filtered_executions = [];

    for (let i = 0; i < test.executions.length; i++) {
      const execution = test.executions[i];
      const filtered_execution = this.execution(execution, passed_active, failed_active, skipped_active);
      if (filtered_execution) {
        filtered_executions.push(filtered_execution);
      }
    }

    if (filtered_executions.length > 0) {
      return new Test(test.id, test.node_id, test.name, test.description, test.self_test, filtered_executions);
    }

    return null;
  }

  execution(execution, passed_active, failed_active, skipped_active) {
    if ((execution.outcome == "passed" && !passed_active) || (execution.outcome == "failed" && !failed_active) || (execution.outcome == "skipped" && !skipped_active)) {
      return null;
    }

    let filtered_steps = [];

    for (let i = 0; i < execution.steps.length; i++) {
      const step = execution.steps[i];
      filtered_steps.push(new Step(step.id, step.description, step.outcome));
    }

    return new Execution(execution.id, execution.device, execution.outcome, execution.duration, filtered_steps);
  }
}
