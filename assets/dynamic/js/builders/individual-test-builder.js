/*
 * SPDX-License-Identifier: MIT
 * File     :  individual-test-builder.js
 * Desc     :  IndividualTestBuilder class, to build the UI of the individual test containers of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 */

class IndividualTestBuilder {
  _root = null;
  _model = null;
  _test = null;
  _filtered_test = null;
  _selected_execution_table_model = null;
  _selected_execution = null;
  _selects = [];

  constructor(model) {
    this._model = model;
    this._model.register(this);
    this._test = this._model.get_test();
    this._filtered_test = this._model.get_filtered_test();
  }

  build() {
    if (this._root == null) {
      this._root = document.createElement("div");
    }

    if (this._filtered_test != null) {
      this._root.className = "individual-test";
      this._root.appendChild(this._title());
      this._root.appendChild(this._description());
      this._root.appendChild(this._ran_on());

      const execution_builder = new ExecutionBuilder(this._model.get_selected_execution_model());
      this._root.appendChild(execution_builder.build());
    }

    return this._root;
  }

  update() {
    while (this._root.firstChild) {
      this._root.removeChild(this._root.firstChild);
      this._root.className = "";
    }

    this._filtered_test = this._model.get_filtered_test();
    this._selects = [];

    this.build();
  }

  _title() {
    let title = document.createElement("h2");

    title.id = `test-${this._test.id}`;
    title.innerText = `Test: ${this._test.name}`;

    return title;
  }

  _description() {
    let description = document.createElement("div");
    description.className = "test-description";

    description.appendChild(this._description_title());
    description.appendChild(this._description_text());

    return description;
  }

  _description_title() {
    let title = document.createElement("h3");
    title.innerText = "Test description";
    return title;
  }

  _description_text() {
    let text = document.createElement("p");

    const descriptions = this._test.description.split("\n");

    for (let i = 0; i < descriptions.length; i++) {
      if (i == 0 && descriptions[i] == "") {
        continue;
      }

      text.innerHTML += descriptions[i] + "<br/>\n";
    }

    return text;
  }

  _ran_on() {
    let div = document.createElement("div");
    div.className = "ran-on";

    let ran_on = document.createElement("span");
    ran_on.className = "ran-on";
    ran_on.innerText = "ran on: ";

    div.appendChild(ran_on);
    div.appendChild(this._devices());

    return div;
  }

  _devices() {
    let devices = document.createElement("span");
    devices.className = "devices";

    if (this._filtered_test.executions.length == 1) {
      devices.appendChild(this._devices_single());
    } else {
      devices.appendChild(this._device_multiple());
    }

    return devices;
  }

  _devices_single() {
    let devices = document.createElement("span");
    devices.innerText = this._filtered_test.executions[0].device;
    return devices;
  }

  _device_multiple() {
    let devices = [];

    for (let i = 0; i < this._filtered_test.executions.length; i++) {
      const execution = this._filtered_test.executions[i];
      devices.push(new SelectOption(execution.id, execution.device, execution.outcome));
    }

    const select = new Select(devices, (id) => {
      this._model.set_selected_execution_id(id);
      this.update();
    });

    this._selects.push(select);
    return select.build(this._model.get_selected_execution_id());
  }
}
