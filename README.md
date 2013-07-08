#B2G-JS-REPL

The tool for interacting with B2G by JS.


## Prepare
```bash
$ adb forward tcp:2828 tcp:2828
$ easy_install virtualenv
$ virtualenv .env
$ source .env/bin/activate
$ python setup.py develop
$ b2g_js -h
```

## Tips

### List all apps

User can list all apps' frame by b2g_js.
```bash
$ b2g_js -l
```

In interaction mode, user also can list apps by ```:l``` command.
```bash
>>> :l
#  Status  App URL
-1         app://system.gaiamobile.org/index.html
0          app://costcontrol.gaiamobile.org/widget.html
1  active  app://homescreen.gaiamobile.org/index.html#root
2  active  app://communications.gaiamobile.org/contacts/index.html
3          app://keyboard.gaiamobile.org/index.html
# Current
Connect to app://system.gaiamobile.org/index.html
>>> 
```


### Multi-line JS

Add " \" (space & backslash) after javascript.
```
>>> var str_01 = 'hello ' \
... var str_02 = 'world!' \
... return str_01 + str_02
hello world!
>>> 
```


### Import JS

Add the JS files under ```js_component``` folder, then import them by ```:i``` command.
```bash
$ b2g_js -c -1
#  Status  App URL
-1         app://system.gaiamobile.org/index.html
0          app://costcontrol.gaiamobile.org/widget.html
1          app://homescreen.gaiamobile.org/index.html#root
2          app://keyboard.gaiamobile.org/index.html
Start...
Connect to app://system.gaiamobile.org/index.html
Enter 'exit' or Crtl+D to exit the shell.
And enter ':h' for more commands.
>>> :i 
gaia_data_layer.js
>>> :i gaia_data_layer.js
Imported: /home/askeing/other-projects/B2G-JS-REPL/b2g_js/js_component/gaia_data_layer.js
>>> :s
Swith to Async JS execution
a>> return GaiaDataLayer.getAllContacts();
[...ALL_CONTACTS...]
a>> 
```


## Examples

Multi-line example:
```bash
(.env)user@host:~/workspace/B2G-JS-REPL$ adb devices
List of devices attached 
full_unagi      device
(.env)user@host:~/workspace/B2G-JS-REPL$ adb forward tcp:2828 tcp:2828
(.env)user@host:~/workspace/B2G-JS-REPL$ b2g_js -l
#  Status  App URL
0          app://costcontrol.gaiamobile.org/widget.html
1  active  app://homescreen.gaiamobile.org/index.html#root
2  active  app://settings.gaiamobile.org/index.html#root
3          app://sms.gaiamobile.org/index.html
4          app://keyboard.gaiamobile.org/index.html
(.env)user@host:~/workspace/B2G-JS-REPL$ b2g_js -c2
Start...
Connect to app://settings.gaiamobile.org/index.html#root
Enter 'exit' or Crtl+D to exit the shell.
And enter ':h' for more commands.
>>> var str_1 = "Hello World " \
... var str_2 = document.URL \
... return str_1 + str_2
Hello World app://settings.gaiamobile.org/index.html#root
>>> 
>>> 
>>> exit
End. Bye!!
(.env)user@host:~/workspace/B2G-JS-REPL$ 
```

Async JS execution example:
```bash
(.env)user@host:~/workspace/B2G-JS-REPL$ b2g_js -l
#  Status  App URL
0          app://costcontrol.gaiamobile.org/widget.html
1  active  app://homescreen.gaiamobile.org/index.html#root
2          app://settings.gaiamobile.org/index.html#root
3          app://clock.gaiamobile.org/index.html
4  active  app://communications.gaiamobile.org/contacts/index.html
5          app://keyboard.gaiamobile.org/index.html
(.env)user@host:~/workspace/B2G-JS-REPL$ b2g_js -c4
Start...
Connect to app://communications.gaiamobile.org/contacts/index.html
Enter 'exit' or Crtl+D to exit the shell.
And enter ':h' for more commands.
>>> :s
Swith to Async JS execution
a>> var req = window.navigator.mozContacts.find({}) \
... req.onsuccess = function () { \
...   marionetteScriptFinished(req.result) \
... }
[{u'honorificPrefix': [], u'tel': None, ..., u'givenName': [u'TestName']}]
a>> :s
Swith to Sync JS execution
>>> :q
End. Bye!!
(.env)user@host:~/workspace/B2G-JS-REPL$ 
```

