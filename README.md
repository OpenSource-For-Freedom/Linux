Private tasklist, To-Do's prior to release (in no particular order):

-Study over successful system hardening scripts you come across. (ex: harbian-audit)
-Study setgid, setuid, and sticky permission removal on certain executables it would be safe on.
Removing these perms can break systems so this should be tread lightly.
-Study addition of console usergroup in Whonix, understand the advantages, how it can be improved,
if it's truly necessary  and more on additional groups for securing down a system.
-Example of showing every setgid perm this was ran as root:
find / * -mount -perm -2000 -type f -exec ls -ld {} \; > /home/user/setgid_.txt && chown -v user:user /home/user/setgid_.txt
-Hardening efforts continue in /etc/security, mopdifications in /etc/host.conf, hosts, host.[deny/allow], and so on.
-ie.cat /etc/host.conf
order bind,hosts
multi on
-More to come....
-Change project name to Hard3n_Linux ?
-Big one: Start  doing a basic apparmor config after too, but don't break the system, maintain useability
