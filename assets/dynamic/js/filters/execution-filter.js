/*
 * File     :  execution-filter.js
 * Desc     :  ExecutionFilter class, to filter the execution data of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  02/01/2024
 * Version  :  1.0
 * License  :  Copyright (C) 2024 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

class ExecutionFilter {
  execution(execution, passed_active, failed_active, skipped_active) {
    let filtered_steps = [];

    for (let i = 0; i < execution.steps.length; i++) {
      const step = execution.steps[i];
      const filtered_step = this.step(step, passed_active, failed_active, skipped_active);
      if (filtered_step) {
        filtered_steps.push(filtered_step);
      }
    }

    // Returns empty Execution if no steps are left
    return new Execution(execution.id, execution.device, execution.outcome, execution.duration, filtered_steps);
  }

  step(step, passed_active, failed_active, skipped_active) {
    if ((step.outcome == "passed" && !passed_active) || (step.outcome == "failed" && !failed_active) || (step.outcome == "skipped" && !skipped_active)) {
      return null;
    }

    return new Step(step.id, step.description, step.outcome);
  }
}
