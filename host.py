import XenAPI
import sys

def main(sx):
    hosts = sx.host.get_all()
    for host in hosts:
        print sx.host.get_name_label(host)
        sx.host.disable(host)
        sx.host.shutdown(host)


if __name__ == "__main__":
    if len(sys.argv) <> 4:
        print ("Usage:")
        print (sys.argv[0], "<url> <username> <password")

    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    print ("List of non-template VMs on {0}".format(url))
    session = XenAPI.Session(url)
    session.login_with_password(username,password)
    main(session.xenapi)
    session.logout()
