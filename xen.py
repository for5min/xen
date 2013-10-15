import XenAPI
import sys
from collections import OrderedDict

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

def super_mode(sx):
    print ("Holy! You are now in super mode, now one click to shutdown all VMs and host.")
    vms = sx.VM.get_all()
    hosts = sx.host.get_all()
    print ("Your really wanna do this?(Y/N)")
    answer = raw_input("Y/N>")

    if answer == "Y" or answer == "Yes" or answer == "YES" or answer == "y":
        for vm in vms:
             if not sx.VM.get_is_a_template(vm) and not sx.VM.get_is_control_domain(vm) and sx.VM.get_power_state(vm) == "Running":
                 sx.VM.hard_shutdown(vm)
        print ("Job Done!")
        print ("Whether you want to shutdown the host? Y/N")
        answer_host = raw_input("Y/N >")
        if answer_host == "Y":
            # host shutdown function, not tested with shutdown sequence.
            for host in hosts:
                sx.host.disable(host)
                sx.host.shutdown(host)
                print ("Job Done!")
        else:
            sys.exit(0)
    elif answer ==  "N" or answer == "NO" or answer == "No" or answer == "n":
        print ("The answer is {0}".format(answer))
        sys.exit(0)
    else:
        print ("Bye")
        sys.exit(0)


def select(sx):
    get_vm(sx)
    print ("Which action(start/shutdown/reboot/supermode) you want to take?")
    action = raw_input(">")
    if action == "start":
        start_vm(sx)
    elif action == "shutdown":
        shutdown_vm(sx)
    elif action == "reboot":
        reboot_vm(sx)
    elif action == "super" or action == "supermode":
        super_mode(sx)
    else:
        print("I don't understand your action!")
        main(sx)

    print("Your actions are token, Thanks for using the script!")

def main():

    if len(sys.argv) <> 3:
        print ("Usage:")
        print (sys.argv[0], "<username> <password")

    username = sys.argv[1]
    password = sys.argv[2]


    pool = {
        "test01":"https://test001.sh",
        "test02":"https://test006.sh",
        "test03":"https://test022.sh",
        "test04":"https://test027.sh",
        "test05":"https://test016.sh",
        "test06":"https://test020.sh",
        "test07":"https://test039.sh",
        "test08":"https://test044.sh",
        "test09":"https://test047.sh",
        "test10":"https://test021.sh",
    }

    pool_stored = OrderedDict(sorted(pool.items(), key=lambda t:t[0]))

    number = 0

    for k in pool_stored:
        number = number + 1
        print number, k
    print("Which pool you want to connect?")
    #print pool_stored.values()[2]
    cn = raw_input(">")
    if int(cn) > number:
        sys.exit(1)
    else:
        i = int(cn) - 1
        print (pool_stored.values()[i])
        url = pool_stored.values()[i]

    print ("List of non-template VMs on {0}".format(url))
    session = XenAPI.Session(url)
    session.login_with_password(username,password)
    sx = session.xenapi
    select(sx)

    session.logout()




if __name__ == "__main__":
    main()

