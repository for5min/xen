import XenAPI
import sys

def choose_pool():

    """If new pool needs to add, the dict pool needs to update. If pool master had been switched,it has
    to be modified as well"""


    pool = ( ("CNSHHUB01","https://ecnshxen001.sh.cn.ao.ericsson.se"),
             ("CNSHHUB02","https://ecnshxen006.sh.cn.ao.ericsson.se"),
             ("CNSHHUB03","https://ecnshxen022.sh.cn.ao.ericsson.se"),
             ("CNSHHUB04","https://ecnshxen027.sh.cn.ao.ericsson.se"),
             ("CNSHHUB06","https://ecnshxen020.sh.cn.ao.ericsson.se"),
             ("CNSHHUB07","https://ecnshxen039.sh.cn.ao.ericsson.se"),
             ("CNSHHUB08","https://ecnshxen044.sh.cn.ao.ericsson.se"),
             ("CNSHHUB09","https://ecnshxen047.sh.cn.ao.ericsson.se"),
             ("CNSHHUB10","https://ecnshxen021.sh.cn.ao.ericsson.se")
    )
    for i in range(len(pool)):
        print ("{0} {1}".format(i+1, pool[i][0]))

    print ("Which pool you want to manage?")
    pool_name=raw_input(">")
    url = pool[i][int(pool_name)-1]
    print url






def get_vm(sx):
    vms = sx.VM.get_all()

    total = 0
    print ("The Pool are having those machines")
    print ("=" * 20)
    for vm in vms:

        if not sx.VM.get_is_a_template(vm) and not sx.VM.get_is_control_domain(vm):
            total = total + 1
            name_label = sx.VM.get_name_label(vm)
            power_state = sx.VM.get_power_state(vm)

            print total, name_label, power_state

def start_vm(sx):

    print ("Type hostname you want to start.")
    hostname = raw_input(">")
    vm = sx.VM.get_by_name_label(hostname)[0]

    if sx.VM.get_power_state(vm) == "Running":
        print("Sorry Mate, the VM is up and running")
        sys.exit(1)
    else:
        sx.VM.start(vm,False,True)


def shutdown_vm(sx):

    print ("Type hostname you want to force shutdown one of the VMs?")
    hostname = raw_input('>')
    vm = sx.VM.get_by_name_label(hostname)[0]

    if sx.VM.get_power_state(vm) == "Halted":
        print ("Sorry Mate, the VM is already down.")
        sys.exit(1)
    else:
        sx.VM.hard_shutdown(vm)


def reboot_vm(sx):
    print ("Do you want to reboot VMs?")
    hostname = raw_input('>')
    vm = sx.VM.get_by_name_label(hostname)[0]

    if sx.VM.get_power_state(vm) == "Halted":
        sx.VM.start(vm,False,True)
    else:
        sx.VM.hard_reboot(vm)


def main(sx):
    get_vm(sx)
    print ("Which action(start/shutdown/reboot) you want to take?")
    action = raw_input(">")
    if action == "start":
        start_vm(sx)
    elif action == "shutdown":
        shutdown_vm(sx)
    elif action == "reboot":
        reboot_vm(sx)
    else:
        print("I don't understand your action!")
        main(sx)

    print("Your actions are token, Thanks for using the script")



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
