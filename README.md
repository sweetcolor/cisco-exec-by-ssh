# Cisco Wireless Controller script executor by ssh

This python script allow you execute file with list of commands for Cisco Wireless
Controller using ssh.

## Dependencies

Script was written on python 3 and using `paramiko` library for ssh.

For installing `paramiko` you can use:

    pip install paramiko

## Using

For using you need create own file with Cisco Wireless Controller
commands list. Also you need write login information at the first line
in file. Login information must require following rules:

    ip-address,user-name,password

Example:

    192.168.0.100,admin,secret

From the second line start Cisco Wireless Controller commands, each in
own line.

For starting execute just run script:

    python3 cisco_exec_by_ssh.py <commands input file>

## Licence

This script was writen with MIT licence.
