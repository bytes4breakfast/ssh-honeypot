# ssh-honeypot
Log all SSH username/password attempts.

### **Requirements**
* ssh-keygen
* paramiko https://github.com/paramiko/paramiko

### **Description**
This is a fake SSH server intended for logging bruteforce login attempts. Upon receiving a connection, it stores the username, password, IP address and time. Usernames and passwords containing non alphanumeric characters are filtered out, to avoid malicious input.\
I built this program in order to be able to produce wordlists of usernames and passwords, and to see what wordlists are used in the wild. The amount of interaction an attacker is allowed is minimal, since only password-based authentication is allowed and every password is of course rejected.

### **Instructions**
Change your real SSH server to a non-standard port, and run this program on port 22 to start logging bruteforce attempts. You will need to generate new host keys using *ssh-keygen*.\
Obtaining access to a machine through this server shouldn't be possible as it always rejects all credentials without even bothering to look them up in the system. Nevertheless, you should NEVER interact with it using your real credentials, as they will be stored in plaintext in a file.

## **Known Bugs**
*[1] The program leaks sockets when receiving a large ammount of connections in a small time window and eventually (hours) freezes and stops accepting new connections. As a workaround, it is possible to kill and restart the program every day or so.
