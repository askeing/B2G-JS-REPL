# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from optparse import OptionParser
from datetime import datetime
import readline
import re

from marionette import Marionette
from b2g_js.cmd.commands import *


class Runner(object):

    _INPUT_NONE = ''
    _INPUT_EXIT_COMMAND = 'exit'
    _INPUT_MULTIPLE_LINE = ' \\'
    _INPUT_COMMAND_PREFIX = ':'
    _INPUT_SYSTEM_APP_KEYWORD = 'system'

    _is_async = False
    _sync_prompt = '>>> '
    _async_prompt = 'a>> '
    _prompt = _sync_prompt

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
        parser.add_option('-c', '--connect',
                          action='store', type='string', dest='connect',
                          default=None,
                          help='Connect to the App iframe.' \
                               'Use # ID or App URL to connect.')

        (options, args) = parser.parse_args()
        self.connect = options.connect

        # start marionette session
        self.m = Marionette(options.address, options.port)
        self.m.start_session()

        # list all iframes
        if options.enable_list:
            self.list_all_iframes()
        # list active iframes
        elif self.connect == None:
            self.list_active_iframes()

        # connect to App
        if self.connect == None:
            exit(0)
        else:
            # connect App
            print 'Start...'
            if self.open_app(self.connect):
                self.start_js()
            else:
                exit(-1)

    def switch_sync_async(self):
        self._is_async = not self._is_async
        self._prompt = self._async_prompt if self._is_async else self._sync_prompt
        print 'Swith to', ('Async' if self._is_async else 'Sync'), 'JS execution'

    def start_js(self):
        print 'Enter \'%s\' or Crtl+D to exit the shell.' % self._INPUT_EXIT_COMMAND
        print 'And enter \':h\' for more commands.'
        try:
            while True:
                input = raw_input(self._prompt)
                # if input is EXIT command, exit this program
                if input.lower() == self._INPUT_EXIT_COMMAND:
                    self.goodbye()
                    break

                # if input is NONE, then do nothing and keep going...
                elif input == self._INPUT_NONE:
                    continue

                # if input start with ":", it should be the command.
                elif input.startswith(self._INPUT_COMMAND_PREFIX):
                    CmdDispatcher(self, input)

                # if the postfix of input is MULTIPLE_LINE, then record this line and wait the next line until no input with MULTIPLE_LINE.
                elif input.endswith(self._INPUT_MULTIPLE_LINE):
                    input_multiple = input[:len(input) - 1] + '; '
                    while True:
                        next_input = raw_input('... ')
                        if next_input.endswith(self._INPUT_MULTIPLE_LINE):
                            input_multiple = input_multiple + next_input[:len(next_input) - 1] + '; '
                            pass
                        else:
                            input_multiple = input_multiple + next_input + '; '
                            print self.execute_script(input_multiple)
                            break

                # if input is NOT above inputs, then run marionette.execute_script(INPUT)/marionette.execute_async_script(INPUT)
                # and print return value.
                else:
                    print self.execute_script(input)

        except EOFError:
            self.goodbye()
            exit()
        except Exception as e:
            print e
            if self.open_app(-1):
                self.start_js()
        exit()

    def execute_script(self, script):
        try:
            if self._is_async:
                return self.m.execute_async_script(script)
            else:
                return self.m.execute_script(script)
        except Exception as ex:
            print str(ex.message)

    def goodbye(self):
        print 'End. Bye!!'

    def open_app(self, input):
        try:
            # connect App by ID
            app_id = int(input)
            if app_id < 0:
                print 'Connect to', self._get_system_URL()
                self.set_current_frame(self._get_system_URL())
                self.m.switch_to_frame()
            else:
                iframes = self.get_all_iframes_id_name_pair()
                print 'Connect to', iframes[str(app_id)]
                self.set_current_frame(iframes[str(app_id)])
                if iframes[str(app_id)] == "app://keyboard.gaiamobile.org/index.html":
                    self.m.switch_to_frame(app_id, False)
                else:
                    self.m.switch_to_frame(app_id)
            return True

        except(ValueError):
            # connect to System app
            if (input.lower() == self._INPUT_SYSTEM_APP_KEYWORD) or (input.lower() in self._get_system_URL()):
                print 'Connect to', self._get_system_URL()
                self.set_current_frame(self._get_system_URL())
                self.m.switch_to_frame()
                return True

            # connect App by substring
            iframes = self.get_all_iframes_id_name_pair()
            suitable_iframes = {}
            for k, v in iframes.items():
                if input in v:
                    suitable_iframes[k] = v
            # connect to App if there is one fit
            if len(suitable_iframes) == 1:
                target = suitable_iframes.keys()[0]
                print 'Connect to', suitable_iframes.values()[0]
                self.set_current_frame(suitable_iframes.values()[0])
                if suitable_iframes.values()[0] == "app://keyboard.gaiamobile.org/index.html":
                    self.m.switch_to_frame(int(target), False)
                else:
                    self.m.switch_to_frame(int(target))
                return True
            # exit if there are more than one app fit the query
            elif len(suitable_iframes) > 1:
                print 'There are more than one Apps fit the query string [', input, '].'
                print '{0:2s} {1:s}'.format('#', 'App URL')
                for k, v in sorted(suitable_iframes.items()):
                    print '{0:2s} {1:s}'.format(k, v)
                return False
            # exit if there is no app fit the query
            else:
                print 'There is no App fit the query string [', input, '].'
                return False

    def set_current_frame(self, frame_name):
        self._current_frame = frame_name

    def get_current_frame(self):
        return self._current_frame

    def switch_to_system_frame(self):
        self.m.switch_to_frame()

    def _get_system_URL(self):
        self.switch_to_system_frame()
        system_URL = self.m.execute_script('return document.URL')
        return system_URL

    def _get_all_iframes(self):
        self.switch_to_system_frame()
        iframes = self.m.execute_script('return document.getElementsByTagName("iframe")')
        return iframes

    def get_all_iframes_id_name_pair(self):
        iframes = self._get_all_iframes()
        result = {}
        for idx in range(0, iframes['length']):
            iframe = iframes[str(idx)]
            result[str(idx)] = iframe.get_attribute('src')
        return result

    def list_all_iframes(self):
        iframes = self._get_all_iframes()
        print '{0:2s} {1:7s} {2:s}'.format('#', 'Status', 'App URL')
        print '{0:2s} {1:7s} {2:s}'.format('-1', '', self._get_system_URL())
        for idx in range(0, iframes['length']):
            iframe = iframes[str(idx)]
            print '{0:2s} {1:7s} {2:s}'.format(str(idx), ('active' if iframe.is_displayed() else ''), iframe.get_attribute('src'))

    def list_active_iframes(self):
        iframes = self._get_all_iframes()
        print '{0:2s} {1:7s} {2:s}'.format('#', 'Status', 'App URL')
        result = {}
        for idx in range(0, iframes['length']):
            iframe = iframes[str(idx)]
            if iframe.is_displayed():
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
            if iframe.is_displayed():
                result.append(iframe)
        for iframe in result:
            print iframe.get_attribute('src')


def main():
    Runner()

if __name__ == '__main__':
    main()
