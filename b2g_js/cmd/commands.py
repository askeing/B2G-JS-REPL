# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import codecs
import re
import subprocess

from marionette import Marionette


class CmdDispatcher(object):

    _MSG_NO_CMD = 'No such command.'

    _CMD_EXIT = ':q'
    _CMD_HELP = ':h'
    _CMD_IMPORT_JS_COMPONENT = ':i'
    _CMD_LAST_MARIONETTE_LOG = ':m'
    _CMD_LIST_FRAMES = ':l'
    _CMD_OPEN_FRAME = ':o'
    _CMD_SWITCH_SYNC_ASYNC = ':s'
    _CMD_WRITE_SOURCE_TO_FILE = ':w'

    def __init__(self, runner, command):
        self.super_runner = runner
        self.m = runner.m
        self.command = command
        self()

    def __call__(self):
        if self.command.lower().startswith(self._CMD_EXIT):
            raise EOFError()

        elif self.command.lower().startswith(self._CMD_HELP):
            PrintUsageCmd()

        elif self.command.lower().startswith(self._CMD_WRITE_SOURCE_TO_FILE):
            args = self.command.split()
            target = 'output.txt'
            if len(args) > 1:
                target = re.sub(r'[^a-zA-Z0-9\.]', '_', args[1])
            WritePageSourceToFileCmd(self.m, target)

        elif self.command.lower().startswith(self._CMD_SWITCH_SYNC_ASYNC):
            SwitchJSExecutionCmd(self.super_runner)

        elif self.command.lower().startswith(self._CMD_IMPORT_JS_COMPONENT):
            args = self.command.split()
            file = None
            if len(args) > 1:
                file = args[1]
            ImportJSComponentCmd(self.m, file)
            pass

        elif self.command.lower().startswith(self._CMD_LIST_FRAMES):
            ListFramesCmd(self.m, self.super_runner)

        elif self.command.lower().startswith(self._CMD_OPEN_FRAME):
            args = self.command.split()
            if len(args) > 1:
                OpenFrameCmd(self.m, self.super_runner, args[1])
            else:
                OpenFrameCmd(self.m, self.super_runner)

        elif self.command.lower().startswith(self._CMD_LAST_MARIONETTE_LOG):
            args = self.command.split()
            if len(args) > 1:
                ListLastMarionetteLog(args[1])
            else:
                ListLastMarionetteLog()

        else:
            print self._MSG_NO_CMD, self.command


class PrintUsageCmd(object):
    def __init__(self):
        self()

    def __call__(self):
        output_head_format = '{0:13s}{1:s}'
        output_format = '{0:2s} {1:9s} {2:s}'
        print output_head_format.format('#Commands', '#Description')
        print output_format.format(CmdDispatcher._CMD_HELP, '', 'Print usage.')
        print output_format.format(CmdDispatcher._CMD_EXIT, '', 'Exit.')
        print output_format.format(CmdDispatcher._CMD_WRITE_SOURCE_TO_FILE, '<FILE>', 'Print page source to file. Default <FILE> is output.txt.')
        #print output_format.format(':e', '<FILE>', 'Read javascript from file. Do nothing if no <FILE>.')
        print output_format.format(CmdDispatcher._CMD_SWITCH_SYNC_ASYNC, '', 'Switch sync/async javascript execution.')
        print output_format.format(CmdDispatcher._CMD_IMPORT_JS_COMPONENT, '<FILE>', 'Import javascript from file. List all components if no <FILE>.')
        print output_format.format(CmdDispatcher._CMD_LIST_FRAMES, '', 'List all apps of b2g instance.')
        print output_format.format(CmdDispatcher._CMD_OPEN_FRAME, '<KEYWORD>', 'Connect to the App iframe. Using # ID or App_URL as <KEYWORD>.')
        print output_format.format(CmdDispatcher._CMD_LAST_MARIONETTE_LOG, '<LINES>', 'Print out last few lines of marionette log information.')
        print output_format.format('', 'exit', 'Exit.')


class SwitchJSExecutionCmd(object):
    def __init__(self, runner):
        self(runner)

    def __call__(self, runner):
        runner.switch_sync_async()


class WritePageSourceToFileCmd(object):
    def __init__(self, marionette, dest):
        self.m = marionette
        self.dest = dest
        self()

    def __call__(self):
        f = codecs.open(self.dest, 'w', 'utf8')
        f.write(self.m.page_source)
        f.close()


class ImportJSComponentCmd(object):

    _FOLDER_JS_COMPONENT = 'js_component'

    def __init__(self, marionette, file=None):
        self.js_dir = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, self._FOLDER_JS_COMPONENT))
        self.m = marionette
        self.file = file
        self()

    def __call__(self):
        if os.path.exists(self.js_dir):
            js_files = [f for f in os.listdir(self.js_dir) if os.path.isfile(os.path.join(self.js_dir, f))]
            # list all js components
            if self.file == None:
                for js_file in js_files:
                    print js_file
            else:
                js_file = os.path.abspath(os.path.join(self.js_dir, self.file))
                indices = [ i for i, s in enumerate(js_files) if self.file in s ]
                # if file exists, import it
                if os.path.exists(js_file) and os.path.isfile(js_file):
                    self.m.import_script(js_file)
                    print 'Imported:', js_file
                # if only one file partially matches, ask if user want to import it
                elif indices.__len__() == 1:
                    predicted_file = os.path.abspath(os.path.join(self.js_dir, js_files[indices[0]]))
                    self.m.import_script(predicted_file)
                    print 'Imported:', predicted_file
                # if there are more than one partially matched, print out reference file list
                elif indices.__len__() > 1:
                    print 'More than one partial file names found:'
                    for i in indices:
                        print js_files[i]
                # nothing partially matched, print out warning
                else:
                    print 'No JS components "%s" under "%s" folder.' % (self.file, self.js_dir)
        else:
            print 'No JS components under "%s" folder.' % self.js_dir


class ListFramesCmd(object):
    def __init__(self, marionette, super_runner):
        self.m = marionette
        self.runner = super_runner
        self.current_frame = self.runner.get_current_frame()
        self()

    def __call__(self):
        self.runner.switch_to_system_frame()
        self.runner.list_all_iframes()
        print '# Current'
        if self.runner.open_app(self.current_frame):
            pass
        else:
            self.runner.open_app(-1)


class OpenFrameCmd(object):
    def __init__(self, marionette, super_runner, input=None):
        self.m = marionette
        self.runner = super_runner
        if input == None:
            self.input = self.runner.get_current_frame()
        else:
            self.input = input
        self()

    def __call__(self):
        self.runner.switch_to_system_frame()
        if self.runner.open_app(self.input):
            pass
        elif self.runner.open_app(self.current_frame):
            pass
        else:
            self.runner.open_app(-1)

class ListLastMarionetteLog(object):
    def __init__(self, number=5):
        self.number = number
        self()

    def __call__(self):
        print subprocess.Popen("adb logcat -d | grep \"MARIONETTE LOG\" |tail -" + str(self.number), stdout=subprocess.PIPE, shell=True).stdout.read() 
