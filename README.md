#B2G-JS-REPL

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

```bash
$ b2g_js -l
```

### Multi-line JS

Add " \" after javascript.


## Example
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
#  Status  App URL
1  active  app://homescreen.gaiamobile.org/index.html#root
2  active  app://settings.gaiamobile.org/index.html#root
Start...
Connect to app://settings.gaiamobile.org/index.html#root
Enter 'exit' or Crtl+D to exit the shell.
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
