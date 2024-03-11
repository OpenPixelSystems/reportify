/*
 * File     :  overview-model.js
 * Desc     :  OverviewModel class, to hold the state of the overview container of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

class OverviewModel {
  _tests = [];
  _filtered_tests = null;
  _builder = null;
  _model = null;
  _filter = null;
  _filters_changed_callback = null;

  constructor(tests, filters_changed_callback) {
    this._tests = tests;
    this._filtered_tests = tests;
    this._filter = new TestFilter();
    this._filters_changed_callback = filters_changed_callback;

    let passed = false;
    let failed = false;
    let skipped = false;

    for (let i = 0; i < tests.length; i++) {
      const test = tests[i];

      if (test.get_outcome() == "passed") {
        passed = new TableModelToggle(true, this._filters_changed.bind(this));
      } else if (test.get_outcome() == "failed") {
        failed = new TableModelToggle(true, this._filters_changed.bind(this));
      } else if (test.get_outcome() == "skipped") {
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

  get_tests() {
    return this._tests;
  }

  get_filtered_tests() {
    return this._filtered_tests;
  }

  get_model() {
    return this._model;
  }

  _visible_changed() {
    this.update();
  }

  _filters_changed() {
    this._filtered_tests = this._filter.tests(this._tests, this._model.passed_active(), this._model.failed_active(), this._model.skipped_active());
    this.update();

    if (this._filters_changed != null) {
      this._filters_changed_callback(this._model);
    }
  }
}
