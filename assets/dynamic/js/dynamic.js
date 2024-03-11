/*
 * File     :  dynamic.js
 * Desc     :  Entry file of the dynamic reports
 * Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
 * Date     :  31/12/2023
 * Version  :  1.0
 * License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
 *             Confidential and for internal use only. The content of this document constitutes proprietary
 *             information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
 *             of any part of the content of this document by unauthorized parties is strictly prohibited.
 */

// Wait for the DOM to be ready
document.addEventListener("DOMContentLoaded", () => {
  const parser = new Parser();
  const tests = parser.parse();

  const model = new Model(tests);
  const builder = new Builder(model);
  document.body.appendChild(builder.build());
});
