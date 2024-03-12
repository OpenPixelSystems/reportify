/*
 * SPDX-License-Identifier: MIT
 * File     :  execution-model.js
 * Desc     :  ExecutionModel class, to hold the state of the individual test execution container of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  02/01/2024
 * Version  :  1.0
 */

class ExecutionModel {
  _execution = null;
  _filtered_execution = null;
  _builder = null;
  _model = null;
  _filter = null;

  constructor(execution) {
    this._execution = execution;
    this._filtered_execution = execution;
    this._filter = new ExecutionFilter();

    let passed = null;
    let failed = null;
    let skipped = null;

    for (let i = 0; i < execution.steps.length; i++) {
      const step = execution.steps[i];

      if (step.outcome == "passed") {
        passed = new TableModelToggle(true, this._filters_changed.bind(this));
      } else if (step.outcome == "failed") {
        failed = new TableModelToggle(true, this._filters_changed.bind(this));
      } else if (step.outcome == "skipped") {
        skipped = new TableModelToggle(true, this._filters_changed.bind(this));
      }
    }

    const visible = new TableModelToggle(true, this._visible_changed.bind(this));
    const total = new TableModelToggle(passed || failed || skipped, this._filters_changed.bind(this));

    this._model = new TableModel(visible, total, passed, failed, skipped);
  }

  register(builder) {
    this._builder = builder;
  }

  update() {
    if (this._builder != null) {
      this._builder.update();
    }
  }

  get_execution() {
    return this._execution;
  }

  get_filtered_execution() {
    return this._filtered_execution;
  }

  get_model() {
    return this._model;
  }

  _visible_changed() {
    this.update();
  }

  _filters_changed() {
    this._filtered_execution = this._filter.execution(this._execution, this._model.passed_active(), this._model.failed_active(), this._model.skipped_active());
    this.update();
  }
}
