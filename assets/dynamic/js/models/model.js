/*
 * File     :  model.js
 * Desc     :  Model class, to hold the state of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

class Model {
  overview_model = null;
  individual_test_models = [];

  constructor(tests) {
    this.overview_model = new OverviewModel(tests, this.overview_filters_changed.bind(this));

    for (let i = 0; i < tests.length; i++) {
      this.individual_test_models.push(new IndividualTestModel(tests[i]));
    }
  }

  overview_filters_changed(model) {
    for (let i = 0; i < this.individual_test_models.length; i++) {
      this.individual_test_models[i].overview_filters_changed(model);
    }
  }
}
