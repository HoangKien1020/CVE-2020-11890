# Made by HK

# CVE-2020-11890: Improper input validations in the usergroup table class could lead to a broken ACL configuration to RCE
# Link
https://developer.joomla.org/security-centre/810-20200402-core-missing-checks-for-the-root-usergroup-in-usergroup-table.html

# PoC
## Affected version: Joomla core before 3.9.17
## User requirement: Admin account (Not superadmin)
## Gain access: Create a new Superadmin, then trigger RCE.
## Remote Code Execution (RCE) in Joomla
## Run *cve202011890.py* with your credentials and access link rce:
![image](https://user-images.githubusercontent.com/24661746/79949993-9f45b180-84a0-11ea-80bd-5b7aedbb3b64.png)

# Guide to use docker such as:
# #Step 1: 

# *docker pull hoangkien1020/joomla:3.9.16*

# #Step 2:

# *docker run -d --rm -it -p 8080:80 hoangkien1020/joomla:3.9.16*

# #Step 3: Access your domain/IP with port 8080:
![image](https://user-images.githubusercontent.com/24661746/75947931-9be86d80-5ed4-11ea-991d-f37309d4c41a.png)
# Inside this image with credentials

### *username: password*

### MySQL: root: root (can access via IP:8080/phpmyadmin)

### superadmin:1234 (Super Users)

### admin:1234 (Administrator)

### hacker:1234 (Manager) 
