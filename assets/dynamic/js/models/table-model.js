/*
 * SPDX-License-Identifier: MIT
 * File     :  table-model.js
 * Desc     :  TableModel and TableModelFilter classes, to hold the state of the test tables of the reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 */

class TableModelToggle {
  active = true;
  callback = null;

  constructor(active, callback) {
    this.active = active;
    this.callback = callback;
  }
}

class TableModel {
  _visible = null;
  _total = null;
  _passed = null;
  _failed = null;
  _skipped = null;

  constructor(visible, total, passed, failed, skipped) {
    this._visible = visible;
    this._total = total;
    this._passed = passed;
    this._failed = failed;
    this._skipped = skipped;
  }

  visible() {
    return this._visible.active;
  }

  total_active() {
    if (this._total) {
      return this._total.active;
    }

    return false;
  }

  passed_active() {
    if (this._passed) {
      return this._passed.active;
    }

    return false;
  }

  failed_active() {
    if (this._failed) {
      return this._failed.active;
    }

    return false;
  }

  skipped_active() {
    if (this._skipped) {
      return this._skipped.active;
    }

    return false;
  }

  toggle_visible() {
    this._set_visible(!this._visible.active);
  }

  toggle_total() {
    if (this._total) {
      const current_total = this._total.active;

      this._set_total(!current_total);
      this._set_passed(!current_total);
      this._set_failed(!current_total);
      this._set_skipped(!current_total);
    }
  }

  toggle_passed() {
    if (this._passed) {
      this._set_passed(!this._passed.active);

      if (this._all_individual_filters_active()) {
        this._set_total(true);
      } else if (this._none_individual_filters_active()) {
        this._set_total(false);
      }
    }
  }

  toggle_failed() {
    if (this._failed) {
      this._set_failed(!this._failed.active);

      if (this._all_individual_filters_active()) {
        this._set_total(true);
      } else if (this._none_individual_filters_active()) {
        this._set_total(false);
      }
    }
  }

  toggle_skipped() {
    if (this._skipped) {
      this._set_skipped(!this._skipped.active);

      if (this._all_individual_filters_active()) {
        this._set_total(true);
      } else if (this._none_individual_filters_active()) {
        this._set_total(false);
      }
    }
  }

  _set_visible(visible) {
    if (this._visible) {
      this._visible.active = visible;

      if (this._visible.callback) {
        this._visible.callback();
      }
    }
  }

  _set_total(active) {
    if (this._total) {
      this._total.active = active;

      if (this._total.callback) {
        this._total.callback();
      }
    }
  }

  _set_passed(active) {
    if (this._passed) {
      this._passed.active = active;

      if (this._passed.callback) {
        this._passed.callback();
      }
    }
  }

  _set_failed(active) {
    if (this._failed) {
      this._failed.active = active;

      if (this._failed.callback) {
        this._failed.callback();
      }
    }
  }

  _set_skipped(active) {
    if (this._skipped) {
      this._skipped.active = active;

      if (this._skipped.callback) {
        this._skipped.callback();
      }
    }
  }

  _all_individual_filters_active() {
    if (this._passed && !this._passed.active) {
      return false;
    }

    if (this._failed && !this._failed.active) {
      return false;
    }

    if (this._skipped && !this._skipped.active) {
      return false;
    }

    return true;
  }

  _none_individual_filters_active() {
    if (this._passed && this._passed.active) {
      return false;
    }

    if (this._failed && this._failed.active) {
      return false;
    }

    if (this._skipped && this._skipped.active) {
      return false;
    }

    return true;
  }
}
