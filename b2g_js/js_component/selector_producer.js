/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

'use strict';

function sniffer (e) {
  e = e||window.event;
  var triggered_node = e.target;
  var el = triggered_node;
  var info = "\n";
  info += "\t *<" + el.nodeName + "> clicked*\n";

  var attr = triggered_node.attributes;
  for (var i = 0 ; i < attr.length ; i++) {
    info += "\t->" + attr[i].name + "/" + attr[i].value + "\n";
  }

  //XPath Producer
  var xpath, segs;
  var allNodes = document.getElementsByTagName('*');
  for (segs = []; el && el.nodeType == 1; el = el.parentNode) {
    //XPath Build Rules By 
    if (el.hasAttribute('id')) {
      segs.unshift(el.tagName.toLowerCase() + '[@id="' + el.getAttribute('id') + '"]');
    } else if (el.hasAttribute('name')) {
      segs.unshift(el.tagName.toLowerCase() + '[@name="' + el.getAttribute('name') + '"]');
    } else {
      var sib, count;
      for (segs = []; el && el.nodeType == 1; el = el.parentNode) {
        for (count = 1, sib = el.previousSibling; sib; sib = sib.previousSibling) {
          if (sib.tagName == el.tagName) {
            count++;
          }
        }

        if (count == 1) {
          segs.unshift(el.tagName.toLowerCase() + '[1]');
        } else {
          segs.unshift(el.tagName.toLowerCase() + '[' + count + ']');
        }
      }
    }

    // This checks if webelement for this xpath is unique
    xpath = segs.length ? '//' + segs.join('/') : null;
    var paragraphCount = document.evaluate( 'count(' + xpath + ')', document, null, XPathResult.ANY_TYPE, null );
    if(paragraphCount.numberValue == 1) {
      break;
    }
  }
  info += "\tXPath: " + xpath + "\n";

  console.log(info);
}


var locator = {
  act: function() {
    document.body.addEventListener("click", sniffer, false);
  },

  deact: function() {
    document.body.removeEventListener("click", sniffer, false);
  },

  test: function() {
    console.log("test SUCESSFULLY!!!!");
  }
};
