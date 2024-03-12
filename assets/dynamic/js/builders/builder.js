/*
 * SPDX-License-Identifier: MIT
 * File     :  builder.js
 * Desc     :  Builder class, to build the UI of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 */

class Builder {
  _model = [];
  _overview_builder = null;
  _individual_test_builders = [];

  constructor(model) {
    this._model = model;
    this._overview_builder = new OverviewBuilder(model.overview_model);

    for (let i = 0; i < model.individual_test_models.length; i++) {
      this._individual_test_builders.push(new IndividualTestBuilder(model.individual_test_models[i]));
    }
  }

  build() {
    let div = document.createElement("div");

    div.appendChild(this._overview_builder.build());

    for (let i = 0; i < this._individual_test_builders.length; i++) {
      div.appendChild(this._individual_test_builders[i].build());
    }

    return div;
  }
}
