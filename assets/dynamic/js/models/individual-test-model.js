/*
 * SPDX-License-Identifier: MIT
 * File     :  individual-test-model.js
 * Desc     :  IndividualTestModel class, to hold the state of the individual test containers of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 */

class IndividualTestModel {
  _test = null;
  _filtered_test = null;
  _builder = null;
  _execution_models = [];
  _filter = null;
  _selected_execution_id = -1;

  constructor(test) {
    this._test = test;
    this._filtered_test = test;
    this._filter = new TestFilter();

    for (let i = 0; i < test.executions.length; i++) {
      const execution = test.executions[i];
      this._execution_models.push(new ExecutionModel(execution));

      if (i == 0) {
        // By default, select the first execution
        this._selected_execution_id = execution.id;
      }
    }
  }

  register(builder) {
    this._builder = builder;

    for (let i = 0; i < this._execution_models.length; i++) {
      this._execution_models[i].register(builder);
    }
  }

  update() {
    if (this._builder != null) {
      this._builder.update();
    }
  }

  get_test() {
    return this._test;
  }

  get_filtered_test() {
    return this._filtered_test;
  }

  set_selected_execution_id(id) {
    this._selected_execution_id = id;
  }

  get_selected_execution_id() {
    return this._selected_execution_id;
  }

  get_selected_execution_model() {
    for (let i = 0; i < this._execution_models.length; i++) {
      if (this._execution_models[i].get_execution().id == this._selected_execution_id) {
        return this._execution_models[i];
      }
    }

    return null;
  }

  get_filtered_selected_execution() {
    for (let i = 0; i < this._execution_models.length; i++) {
      if (this._execution_models[i].get_filtered_execution().id == this._selected_execution_id) {
        return this._execution_models[i].get_filtered_execution();
      }
    }

    console.log("Could not find filtered execution with id " + this._selected_execution_id + " - " + this._execution_models.length + " executions");
    return null;
  }

  get_selected_execution_table_model() {
    for (let i = 0; i < this._execution_models.length; i++) {
      if (this._execution_models[i].get_filtered_execution().id == this._selected_execution_id) {
        return this._execution_models[i].get_model();
      }
    }

    return null;
  }

  overview_filters_changed(model) {
    this._filtered_test = this._filter.test(this._test, model.passed_active(), model.failed_active(), model.skipped_active());

    if (this._filtered_test != null) {
      let execution_found = false;

      for (let i = 0; i < this._filtered_test.executions.length; i++) {
        const execution = this._filtered_test.executions[i];
        if (execution.id == this._selected_execution_id) {
          execution_found = true;
        }
      }

      if (!execution_found) {
        this.set_selected_execution_id(this._filtered_test.executions[0].id);
      }
    }

    this.update();
  }
}
