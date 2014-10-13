/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

'use strict';

function sniffer(e) {
  var el = e.target;
  var info = "\n";
  info += "\tnodeName: " + el.nodeName + "\n";
  if (el.hasAttribute("className"))
    info += "\tnode ClassName: " + el.ClassName + "\n";
  if (el.hasAttribute("id"))
    info += "\tnode id: " + el.id + "\n";
  if (el.hasAttribute("name"))
    info += "\tnode name: " + el.name + "\n";

  var attr = el.attributes;
  for (var i = 0 ; i < attr.length ; i++) {
    info += "\t->" + attr[i].name + "/" + attr[i].value + "\n";
  }
  log(info);
}

function movesniffer(e) {
  var touches = e.changedTouches;
  for (var i = 0 ; i < touches.length ; i++) {
    log("Touch Moves from " + touches[i].pageX + " " + touches[i].pageY);
  }
}

var GaiaEventListener = {

  activateListener: function() {
    document.body.addEventListener("touchmove", movesniffer, false);
    document.body.addEventListener("click", sniffer, false);
  },

  testListener: function() {
    document.body.addEventListener("touchmove", movesniffer, false);
  },

  getClickedElement: function() {
    document.body.addEventListener("click", sniffer, false);
  },

  deactivateListener: function() {
    document.body.removeEventListener("click", sniffer, false);
    document.body.removeEventListener("touchmove", movesniffer, false);
  },

  test: function() {
    log("test SUCESSFULLY!!!!");
  }

};
