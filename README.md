# HostGen
Generates a hostfile based on a template hostfile

# Usage
First, create a template host file with the following setup (here we call this file *templateHosts.txt*)
```
host1 slots=<number of proc>
host2 slots=<number of proc>
...
```
where <number of proc> is the number of processors on that node.
To enable login without typing the password create a public/private key pair.
```bash
cd ~
ssh-keygen -t rsa
```
do not type any passphrase when promted (just hit enter).

Then run
```bash
python manageHosts.py --file=templateHosts.txt --user=<username> --init
```
where <username> is your username on the remote host.
Here you will have to enter the passphrase twice per node when prompted.
However, this step is only required to do one time.

Finally, to create a hostfile containing only nodes where no other user is logged in run
```bash
python manageHosts.py --file=templateHosts.txt --user=username --out=<availableHosts.txt>
```
