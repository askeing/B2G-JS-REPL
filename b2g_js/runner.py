# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from optparse import OptionParser
from datetime import datetime
import re

from marionette import Marionette


class Runner(object):

    def __init__(self, **kwargs):
        # Added parser
        parser = OptionParser()
        parser.add_option('-a', '--address',
                          action='store', type='string', dest='address',
                          default='localhost',
                          help='The host address of b2g instance. Default=localhost')
        parser.add_option('-p', '--port',
                          action='store', type='int', dest='port',
                          default=2828,
                          help='The port of b2g instance.')
        parser.add_option('-l', '--list',
                          action='store_true', dest='enable_list',
                          default='False',
                          help='List all apps of b2g instance. Default=False')
        (options, args) = parser.parse_args()

        # start marionette session
        self.m = Marionette(options.address, options.port)
        self.m.start_session()

        # list iframes
        if options.enable_list == True:
            self.list_all_iframes()
        # list active iframes
        else:
            self.list_active_iframes()

    def _get_all_iframes(self):
        iframes = self.m.execute_script('return document.getElementsByTagName("iframe")')
        return iframes

    def list_all_iframes(self):
        iframes = self._get_all_iframes()
        for idx in range(0, iframes['length']):
            iframe = iframes[str(idx)]
            print '{0:2s} {1:7s} {2:s}'.format(str(idx), ('active' if iframe.is_displayed() else ''), iframe.get_attribute('src'))

    def list_active_iframes(self):
        iframes = self._get_all_iframes()
        result = {}
        for idx in range(0, iframes['length']):
            iframe = iframes[str(idx)]
            if iframe.is_displayed() == True:
                result[str(idx)] = iframe
        for idx, iframe in result.items():
            print '{0:2s} {1:7s} {2:s}'.format(idx, ('active' if iframe.is_displayed() else ''), iframe.get_attribute('src'))

    # TODO: seems like should using Javascript to get the idx of each iframe!?
    def get_all_iframes_by_marionette(self):
        iframes = self.m.find_elements('css selector', 'iframe')
        return iframes

    def list_all_iframes_by_marionette(self):
        iframes = self.get_all_iframes_by_marionette()
        for iframe in iframes:
            print iframe.get_attribute('src')

    def list_active_iframes_by_marionette(self):
        iframes = self.get_all_iframes_by_marionette()
        result = []
        for iframe in iframes:
            if iframe.is_displayed() == True:
                result.append(iframe)
        for iframe in result:
            print iframe.get_attribute('src')


def main():
    Runner()

if __name__ == '__main__':
    main()
