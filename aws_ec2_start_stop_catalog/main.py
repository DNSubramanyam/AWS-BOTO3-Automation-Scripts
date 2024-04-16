import itertools
import threading
import time
import sys
import boto3


con = boto3.session.Session(profile_name='subbu')
ec2 = con.resource('ec2', region_name='ap-south-1')
done = False


def animate():
    for c in itertools.cycle(["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]):
        if done:
            break
        sys.stdout.write('\rWorking on the instruction....' + c)
        # sys.stdout.flush()
        time.sleep(0.1)
    #sys.stdout.write('\rDone!     ')
    return


t = threading.Thread(target=animate)



def action_instance_id(action):
    inst_id = input("Enter you instance ID : ")
    instance = ec2.Instance(inst_id)
    if action == "start":
        #instance.start()
        for i in tqdm(range(100), desc='loading...')
        time.sleep(5)
        #instance.wait_until_running()
    elif action == "stop":
        #instance.stop()
        time.sleep(5)
        #instance.wait_until_stopped()
    elif action == "restart":
        instance.restart()


# long process here

while True:
    print("""
    ************************
    * Choose your option : *
    * 1. Start             *
    * 2. Stop              *
    * 3. Restart           *
    * 4. Exit              *
    ************************
    \n""")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        done = False
        action_instance_id("start")
        done = True
        print("\ninstance started...!")
    elif choice == 2:
        done = False
        action_instance_id("stop")
        done = True
        print("\ninstance stopped...!")
    elif choice == 3:
        print("Restarting the instance...!")
        action_instance_id("restart")
        print("instance restarted...!")
    elif choice == 4:
        print("Exiting ..Good Bye !!")
        sys.exit()
    else:
        print("Wrong choice ,,choose again!!")
