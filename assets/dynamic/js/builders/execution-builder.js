/*
 * File     :  execution-builder.js
 * Desc     :  ExecutionBuilder class, to build the UI of the individual test containers of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

class ExecutionBuilder {
  _root = null;
  _model = null;
  _execution = null;
  _filtered_execution = null;
  _table_model = null;

  constructor(model) {
    this._model = model;
    this._model.register(this);
    this._execution = this._model.get_execution();
    this._filtered_execution = this._model.get_filtered_execution();
    this._table_model = this._model.get_model();
  }

  build() {
    if (this._root == null) {
      this._root = document.createElement("div");
    }

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

    this._execution = this._model.get_execution();
    this._filtered_execution = this._model.get_filtered_execution();

    this.build();
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
      button.innerText = "Hide execution";
    } else {
      button.innerText = "Show execution";
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

    for (let i = 0; i < this._execution.steps.length; i++) {
      if (this._execution.steps[i].outcome == "passed") {
        passed++;
      } else if (this._execution.steps[i].outcome == "failed") {
        failed++;
      } else if (this._execution.steps[i].outcome == "skipped") {
        skipped++;
      }
    }

    const total = passed + failed + skipped;
    const total_button = this._action_bar_tile("total", total == 1 ? "1 step" : `${total} steps`);

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

    if (this._filtered_execution.steps.length == 0) {
      container.appendChild(this._table_placeholder("No steps found"));
    } else {
      container.appendChild(this._table());
    }

    return container;
  }

  _table_placeholder(text) {
    let placeholder = document.createElement("div");

    placeholder.className = "no-steps";
    placeholder.innerText = text;

    return placeholder;
  }

  _table() {
    let table = document.createElement("table");
    table.className = "test-table individual-test-table";

    table.appendChild(this._table_header());
    table.appendChild(this._table_body());
    table.appendChild(this._table_footer());

    return table;
  }

  _table_header() {
    let header = document.createElement("thead");
    header.appendChild(this._table_header_row());
    return header;
  }

  _table_header_row() {
    let row = document.createElement("tr");

    row.appendChild(this._table_header_cell("Step"));
    row.appendChild(this._table_header_cell("Description", { width: "100%" }));
    row.appendChild(this._table_header_cell("Status"));

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

    for (let i = 0; i < this._filtered_execution.steps.length; i++) {
      const step = this._filtered_execution.steps[i];
      body.appendChild(this._table_body_row(step));
    }

    return body;
  }

  _table_body_row(step) {
    let row = document.createElement("tr");
    row.className = step.outcome;

    row.appendChild(this._table_body_cell(`${parseInt(step.id) + 1}/${this._execution.steps.length}`));
    row.appendChild(this._table_body_cell(step.description));
    row.appendChild(this._table_body_cell(step.outcome));

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

  _table_footer() {
    let footer = document.createElement("tfoot");
    footer.className = this._execution.outcome;

    footer.appendChild(this._table_footer_row());

    return footer;
  }

  _table_footer_row() {
    let row = document.createElement("tr");
    row.appendChild(
      this._table_footer_cell(`Test on ${this._execution.device} ${this._execution.outcome} in ${this._execution.duration.toFixed(2).toString()}s`, {
        colspan: 3,
      })
    );
    return row;
  }

  _table_footer_cell(text, attributes = {}) {
    let cell = document.createElement("td");
    cell.innerText = text;

    for (const key in attributes) {
      cell.setAttribute(key, attributes[key]);
    }

    return cell;
  }
}
