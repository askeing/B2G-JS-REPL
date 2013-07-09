/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

// This function is made to be like dir() in Python
function dir(object) {
  var list = [];
  for(var s in object) {
    list.push(s);
  }
  list.sort();
  return list;
}
