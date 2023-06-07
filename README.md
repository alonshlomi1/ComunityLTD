
## How to Run App:
 - clone the repository on to your local host
 - in src create cert.pem and key.pem using openssl
 - in src create .env
 - open mysql and run the bellow script
 - enable self-signed certificate with the steps bellow
 - run 'python ./controller' on terminal
 
### get self-signed certificate from openssl:
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 3650

### enable self-signed certificate on chrome local host:
Open a new tab in Google Chrome and enter chrome://flags in the address bar.
Search for the flag called "Allow invalid certificates for resources loaded from localhost."
Enable this flag by clicking on the "Enable" button.
Relaunch Google Chrome to apply the changes.

### .env structure
 - email_sender = email you want to send from
 - email_password = password -> get password from https://www.youtube.com/watch?v=g_j6ILT-X0k&ab_channel=ThePyCoach
 - HOST = mysql host
 - USER = mysql user
 - PASSWORD = mysql password
 - DATABASE = mysql DataBase name
 - PORT = mysql port
 - AUTH_PLUGIN = 'mysql_native_password'
 - SYS_SECURITY_LVL = security state (SAFE/XSS/SQLI)

### init DataBase:
```text
CREATE SCHEMA `secure_network_project` ;
use `secure_network_project` ;
CREATE TABLE users (
	user_email VARCHAR (255) NOT NULL,
	user_password VARCHAR(100) NOT NULL,
    user_salt VARCHAR(100) NOT NULL,
	PRIMARY KEY (user_email)
	);
CREATE TABLE clients (
	client_id VARCHAR (255) NOT NULL,
	client_first_name VARCHAR(255),
    client_last_name VARCHAR(255),
    client_phone VARCHAR(255),
    client_email VARCHAR(255),
	PRIMARY KEY (client_id)
	);
CREATE TABLE users_history (
	user_email VARCHAR (255) NOT NULL,
	user_password VARCHAR(100) NOT NULL,
	PRIMARY KEY (user_email, user_password)
	);
CREATE TABLE login_tries (
	user_email VARCHAR (255) NOT NULL,
	tries numeric,
	PRIMARY KEY (user_email)
	);

insert into users (user_email, user_password, user_salt) values("alonasshlomi@gmail.com", "23ea2ab7e93f61ff8a9015eeed9e76546bb240a65da6c45ba769d7ed3f080912", "84b3048d37dd975a59f940fba89c6c3627fa782f837eb71b417333568cc48353");
insert into login_tries (user_email, tries) values("alonasshlomi@gmail.com", 0);
insert into clients (client_id, client_first_name, client_last_name, client_phone, client_email) values("123456789", "alon", "shlomi","0506666666", "hi@gmail.com");
insert into clients (client_id, client_first_name, client_last_name, client_phone, client_email) values("123456780", "alon1", "shlomi1","0506666661", "hi1@gmail.com");
```
    --      user email- alonasshlomi@gmail.com     user password- 1234



## Attacks:
### XSS to use in new client Last name on XSS mode
 - Change SYS_SECURITY_LVL=XSS
 - add new client and in the last name insert :
```text
<img onerror='alert("Hacked!");' src='invalid-image' /> 
```

 - click on show all clients to show the 'Hack'

### SQLi to use on login email in SQLI mode to drop table
 - Change SYS_SECURITY_LVL=SQLI
 - login and put in the email: 
```text
s' or 1=1; Drop table users_history; --  
```
 - watch users_history dropped in the DataBase

### SQLi to use on New Client email in SQLI mode to drop table
 - Change SYS_SECURITY_LVL=SQLI
 - add new client and put in the email: 
```text
a' ); Drop table users_history; -- 
```
 - watch users_history dropped in the DataBase

### SQLi to use on New User email in SQLI mode to drop table
 - Change SYS_SECURITY_LVL=SQLI
 - add new user and put in the email:
```text
aa'); Drop table users_history; -- 
```

 - watch users_history dropped in the DataBase



### bleach.clean():
The bleach.clean() function is a part of the bleach library,which is used for sanitizing and cleaning
HTML input in Python.
It helps to prevent Cross-Site Scripting (XSS) attacks by removing potentially malicious or unsafe HTML
codes from user-generated input.