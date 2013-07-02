/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

'use strict';

function sniffer (e) {
  var el = e.target;
  var info  = "\n";
  info += "\tnodeName: " + el.nodeName + "\n";
  if (el.hasAttribute("className"))
    info += "\tnode ClassName: " + el.ClassName + "\n";
  if (el.hasAttribute("id"))
    info += "\tnode id: " + el.id + "\n";
  if (el.hasAttribute("name"))
    info += "\tnode name: " + el.name + "\n";

  var attr = el.attributes;
  for (var i = 0 ; i < attr.length ; i++) {
    info += "->" + attr[i].name + "/" + attr[i].value + "\n";
  }
  console.log(info);
}

var GaiaElementListener = {

  activateListener: function() {
  
    document.body.addEventListener("click", sniffer, true);
  },

  deactivateListener: function() {

  },

  getClickedElement: function() {
  }

};
