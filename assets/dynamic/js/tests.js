/*
 * File     :  tests.js
 * Desc     :  Test, Execution and Step classes, to hold the test data of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * SPDX-License-Identifier: MIT
 */

class Step {
  id = 0;
  description = "";
  outcome = "";

  constructor(id, description, outcome) {
    this.id = id;
    this.description = description;
    this.outcome = outcome;
  }
}

class Execution {
  id = 0;
  device = "";
  outcome = "";
  duration = 0.0;
  steps = [];

  constructor(id, device, outcome, duration, steps) {
    this.id = id;
    this.device = device;
    this.outcome = outcome;
    this.duration = duration;
    this.steps = steps;
  }
}

class Test {
  id = 0;
  node_id = "";
  name = "";
  description = "";
  self_test = "";
  executions = [];

  constructor(id, node_id, name, description, self_test, executions) {
    this.id = id;
    this.node_id = node_id;
    this.name = name;
    this.description = description;
    this.self_test = self_test;
    this.executions = executions;
  }

  get_outcome() {
    for (let i = 0; i < this.executions.length; i++) {
      if (this.executions[i].outcome == "failed") {
        return "failed";
      } else if (this.executions[i].outcome == "passed") {
        return "passed";
      } else if (this.executions[i].outcome == "skipped") {
        return "skipped";
      }
    }

    return "unknown";
  }

  has_same_outcome() {
    const outcome = this.get_outcome();

    for (let i = 0; i < this.executions.length; i++) {
      if (this.executions[i].outcome != outcome) {
        return false;
      }
    }

    return true;
  }
}
