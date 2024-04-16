import subprocess
from time import sleep
import pyperclip


RUN_DIR = "C:\Program Files\Oracle\VirtualBox"
LIST_VMS =  'VBoxManage list vms'
vm_list = []

def start(vm_in):
    strt_vm = f'VBoxManage startvm {vm_in} --type headless'
    res3 = subprocess.run(strt_vm, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
    print('\n' + res3.stdout.decode('utf-8').strip())

def shutdown(vm_in):
    shut_vm = f'VBoxManage controlvm {vm_in} acpipowerbutton'
    res4 = subprocess.run(shut_vm, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
    print('\n' +  f'Shutting down VM {vm_in}...This might take few seconds.!!' )
    sleep(2)

def reboot(vm_in):
    reb_vm = f'VBoxManage controlvm {vm_in} reboot'
    res5 = subprocess.run(reb_vm, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
    print('\n' + f'Rebooting the VM {vm_in}...!' )
    sleep(2)

def get_VM_state(vm_in):
    state_details = f'VBoxManage showvminfo {vm_in}|findstr State'
    res6 = subprocess.run(state_details, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
    state = res6.stdout.decode('utf-8').strip('State: ')
    print('\n' + f'\n Current state of VM: {state.strip()}' )
    sleep(2)

def get_IP_address(vm_in):
    ip_ad = f'VBoxManage guestproperty get {vm_in} /VirtualBox/GuestInfo/Net/0/V4/IP'
    res7 = subprocess.run(ip_ad, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
    pyperclip.copy(res7.stdout.decode('utf-8')[7:].strip())
    print('\n' + res7.stdout.decode('utf-8')[7:].strip() + '\t\t' + '[IP Copied to clipboard]')
    sleep(2)

print('\nFollowing are the list of VMs: \n')
res = subprocess.run(LIST_VMS, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
for num, each in enumerate(res.stdout.decode('utf-8').splitlines(), 1):
    vm = each.split(' ')[0].strip("\"")
    vm_list.append(vm)
    VM_STATE = f'VBoxManage showvminfo {vm}|findstr State'
    res2 = subprocess.run(VM_STATE, shell=True,cwd=RUN_DIR, stdout=subprocess.PIPE)
    state = res2.stdout.decode('utf-8').strip('State: ')
    print('\n' + f'{num}. {vm}  ==> {state.strip()}' )
input_vm = int(input('\nPlease select the VM to proceed : '))-1
if (input_vm + 1) < len(vm_list):
    print(f'\nSeleted VM : ' +  f'{vm_list[input_vm]}' )
else:
    print('\nPlease select valid input to proceed !!')

operations = {'a': start, 'b': shutdown, 'c': reboot, 'd': get_IP_address, 'e': get_VM_state}

is_end =  True
while is_end:
    print('\nList of Operations : \na. start\nb. shutdown\nc. reboot\nd. get_IP_address\ne. get_VM_state\nf. Exit')
    fun_input = input('\nPlease select the operation to proceed: ').lower()
    if fun_input.strip() == 'f':
        is_end = False
    elif fun_input.strip() in operations.keys():
        operations[fun_input.strip()](vm_list[input_vm])
    else:
        print('\nPlease select valid operation !!')


