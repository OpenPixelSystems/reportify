/*
 * File     :  select.js
 * Desc     :  Select and SelectOption classes, to implement a custom select element (needed to have a custom style)
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

class SelectOption {
  id = 0;
  label = "";
  class_name = "";

  constructor(id, label, class_name) {
    this.id = id;
    this.label = label;
    this.class_name = class_name;
  }
}

class Select {
  _options = [];
  _on_selection_change = null;
  _selected_value = null;

  constructor(options, on_selection_change) {
    this._options = options;
    this._on_selection_change = on_selection_change;
  }

  build(selected_option_id) {
    let container = document.createElement("span");
    container.className = "custom-select";

    let button = document.createElement("button");
    button.className = "select-button";

    button.onclick = () => {
      container.classList.toggle("active");
    };

    this._selected_value = document.createElement("span");
    this._selected_value.className = "selected-value";

    for (let i = 0; i < this._options.length; i++) {
      const option = this._options[i];
      if (option.id == selected_option_id) {
        this._selected_value.innerText = option.label;
      }
    }

    let arrow = document.createElement("span");
    arrow.className = "arrow";

    button.appendChild(this._selected_value);
    button.appendChild(arrow);

    let ul = document.createElement("ul");
    ul.className = "select-dropdown";

    for (let i = 0; i < this._options.length; i++) {
      const li = this._option(this._options[i]);

      li.onclick = () => {
        this._selected_value.innerText = this._options[i].label;
        container.classList.remove("active");

        if (this._on_selection_change) {
          this._on_selection_change(this._options[i].id);
        }
      };

      ul.appendChild(li);
    }

    container.appendChild(button);
    container.appendChild(ul);

    return container;
  }

  _option(option) {
    let li = document.createElement("li");
    li.className = option.class_name;

    let input = document.createElement("input");
    input.type = "radio";

    let label = document.createElement("label");
    label.innerText = option.label;

    li.appendChild(input);
    li.appendChild(label);

    return li;
  }
}
