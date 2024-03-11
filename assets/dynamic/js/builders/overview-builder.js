/*
 * File     :  overview-builder.js
 * Desc     :  OverviewBuilder class, to build the UI of the overview container of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

class OverviewBuilder {
  _root = null;
  _model = null;
  _tests = null;
  _filtered_tests = null;
  _table_model = null;

  constructor(model) {
    this._model = model;
    this._model.register(this);
    this._tests = this._model.get_tests();
    this._filtered_tests = this._model.get_filtered_tests();
    this._table_model = this._model.get_model();
  }

  build() {
    if (this._root == null) {
      this._root = document.createElement("div");
    }

    this._root.id = "overview";

    this._root.appendChild(this._title());
    this._root.appendChild(this._action_bar());

    if (this._table_model.visible()) {
      this._root.appendChild(this._table_container());
    }

    return this._root;
  }

  update() {
    while (this._root.firstChild) {
      this._root.removeChild(this._root.firstChild);
    }

    this._filtered_tests = this._model.get_filtered_tests();

    this.build();
  }

  _title() {
    let title = document.createElement("h3");
    title.innerText = "Test overview";
    return title;
  }

  _action_bar() {
    let action_bar = document.createElement("div");
    action_bar.className = "action-bar";

    action_bar.appendChild(this._action_bar_visibility_button());
    action_bar.appendChild(this._action_bar_summary());

    return action_bar;
  }

  _action_bar_visibility_button() {
    let button = document.createElement("button");
    button.className = "show";

    if (this._table_model.visible()) {
      button.innerText = "Hide overview";
    } else {
      button.innerText = "Show overview";
    }

    button.onclick = () => {
      this._table_model.toggle_visible();
    };

    return button;
  }

  _action_bar_summary() {
    let summary = document.createElement("span");
    summary.className = "summary";

    let passed = 0;
    let failed = 0;
    let skipped = 0;

    for (let i = 0; i < this._tests.length; i++) {
      if (this._tests[i].get_outcome() == "passed") {
        passed++;
      } else if (this._tests[i].get_outcome() == "failed") {
        failed++;
      } else if (this._tests[i].get_outcome() == "skipped") {
        skipped++;
      }
    }

    const total = passed + failed + skipped;

    let total_button = this._action_bar_tile("total", total == 1 ? "1 test" : `${total} tests`);

    if (total == 0) {
      total_button.disabled = true;
    } else {
      total_button.className += this._table_model.total_active() ? " active" : "";
    }

    total_button.onclick = () => {
      this._table_model.toggle_total();
    };

    summary.appendChild(total_button);

    if (passed > 0) {
      let passed_button = this._action_bar_tile("passed", `${passed} passed`);
      passed_button.className += this._table_model.passed_active() ? " active" : "";

      passed_button.onclick = () => {
        this._table_model.toggle_passed();
      };

      summary.appendChild(passed_button);
    }

    if (failed > 0) {
      let failed_button = this._action_bar_tile("failed", `${failed} failed`);
      failed_button.className += this._table_model.failed_active() ? " active" : "";

      failed_button.onclick = () => {
        this._table_model.toggle_failed();
      };

      summary.appendChild(failed_button);
    }

    if (skipped > 0) {
      let skipped_button = this._action_bar_tile("skipped", `${skipped} skipped`);
      skipped_button.className += this._table_model.skipped_active() ? " active" : "";

      skipped_button.onclick = () => {
        this._table_model.toggle_skipped();
      };

      summary.appendChild(skipped_button);
    }

    return summary;
  }

  _action_bar_tile(type, text) {
    let tile = document.createElement("button");
    tile.className = `tile ${type}`;
    tile.innerText = text;
    return tile;
  }

  _table_container() {
    let container = document.createElement("div");

    if (this._filtered_tests.length == 0) {
      container.appendChild(this._table_placeholder("No tests found"));
    } else {
      container.appendChild(this._table());
    }

    return container;
  }

  _table_placeholder(text) {
    let placeholder = document.createElement("div");

    placeholder.className = "no-tests";
    placeholder.innerText = text;

    return placeholder;
  }

  _table() {
    let table = document.createElement("table");
    table.className = "test-table";

    table.appendChild(this._table_header());
    table.appendChild(this._table_body());

    return table;
  }

  _table_header() {
    let header = document.createElement("thead");
    header.appendChild(this._table_header_row());
    return header;
  }

  _table_header_row() {
    let row = document.createElement("tr");

    row.appendChild(this._table_header_cell("ID"));
    row.appendChild(this._table_header_cell("Status", { width: "50%" }));
    row.appendChild(this._table_header_cell("Device", { width: "50%" }));
    row.appendChild(this._table_header_cell("Name"));
    row.appendChild(this._table_header_cell("Duration"));
    row.appendChild(this._table_header_cell("Executions"));

    return row;
  }

  _table_header_cell(text, attributes = {}) {
    let cell = document.createElement("th");
    cell.innerText = text;

    for (const key in attributes) {
      cell.setAttribute(key, attributes[key]);
    }

    return cell;
  }

  _table_body() {
    let body = document.createElement("tbody");

    for (let i = 0; i < this._filtered_tests.length; i++) {
      const test = this._filtered_tests[i];
      for (let j = 0; j < test.executions.length; j++) {
        body.appendChild(this._table_body_row(test, test.executions[j], j));
      }
    }

    return body;
  }

  _table_body_row(test, execution, row_count) {
    let row = document.createElement("tr");
    row.className = "selectable";

    if (test.has_same_outcome()) {
      row.className += ` ${test.get_outcome()}`;
    } else {
      row.className += " mixed";
    }

    const is_last = test.executions.length == 1 || execution.id == test.executions.length - 1;
    if (!is_last) {
      row.className += " no-border";
    }

    row.onclick = () => {
      window.location.href = `#test-${test.id}`;
    };

    if (row_count == 0) {
      row.appendChild(this._table_body_cell(test.id, "", { rowspan: test.executions.length }));
      row.appendChild(this._table_body_cell(execution.outcome, execution.outcome));
      row.appendChild(this._table_body_cell(execution.device, execution.outcome));
      row.appendChild(this._table_body_cell(test.name, "", { rowspan: test.executions.length }));
      row.appendChild(this._table_body_cell(`${execution.duration.toFixed(2).toString()}s`, execution.outcome));
      row.appendChild(this._table_body_cell(test.executions.length, "", { align: "center", rowspan: test.executions.length }));
    } else {
      row.appendChild(this._table_body_cell(execution.outcome, execution.outcome));
      row.appendChild(this._table_body_cell(execution.device, execution.outcome));
      row.appendChild(this._table_body_cell(`${execution.duration.toFixed(2).toString()}s`, execution.outcome));
    }

    return row;
  }

  _table_body_cell(text, className = "", attributes = {}) {
    let cell = document.createElement("td");
    cell.innerText = text;

    if (className != "") {
      cell.className = className;
    }

    for (const key in attributes) {
      cell.setAttribute(key, attributes[key]);
    }

    return cell;
  }
}
