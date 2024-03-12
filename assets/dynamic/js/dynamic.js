/*
 * SPDX-License-Identifier: MIT
 * File     :  dynamic.js
 * Desc     :  Entry file of the dynamic reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 */

// Wait for the DOM to be ready
document.addEventListener("DOMContentLoaded", () => {
  const parser = new Parser();
  const tests = parser.parse();

  const model = new Model(tests);
  const builder = new Builder(model);
  document.body.appendChild(builder.build());
});
