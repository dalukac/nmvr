import os

def main():
    print('Main Node initialized')
    mydir = os.getcwd() 
    os.system("terminal -e 'bash -c \"python3 " + mydir + "subscriber.py; bash\"'")
    os.system("terminal -e 'bash -c \"python3 " + mydir + "publisher.py; bash\"'")
    os.system("terminal -e 'bash -c \"python3 " + mydir + "map_plot.py; bash\"'")
    print(mydir)

if __name__ == '__main__':
    main()