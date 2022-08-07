import argparse

desc = 'Welcome to the analyzer script for the LucidLink Technical Support Engineer Level 3 practical assignment. You need to either parse Lucid.log or app.log for the script to work!'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("log", type=str, help="specify a log file")

args = parser.parse_args()


def report_log_in_log_out_and_user(log):

    """
    I'm using this function to find the amount of times when users logged in and logged out, and who logged in.
    FYI:
    At the first if condition If we used log.lower() with the build in function, we can use any name Lucid/LuCiD, etc.
    I didn't find this necesesarry as when I was testing locally the name stayed the same.
    If the name was changed it could be the user that provided the logs.

    There's no point to repeat the comments in each function, so I'll add them only if there's a major change.
    """

    if 'Lucid.log' in log: # Checking if we're passing the Lucid.log file. 
        try: #try/except is the best way to try your code block and raise an error if somethings goes wrong. I used this approach for each function.
            d_track = {} # Storing information we will print later on in dicts as key/value pairs are the best way to count for a specific occurance.
            d2_track = {} # Again, we're storing the information for the second condition.
            with open(log, "rb") as f: # Open the file as binary.
                contents = str(f.read()).rsplit('\\n') # Reading the file and making it pretty.
                for line in contents: # Iterating over the lines of the log file.
                    if 'logged in' in line: # Lookin for a specific key word, in this case logged in was the one I found met the criteria.
                        u = line.split("'")[1].rsplit("\\")[2] # Splitting the file until we have only the slice we need.
                        d_track[u] = d_track.get(u,0) + 1 # Populating the dict we defined earlier as this 
                    elif 'logged out' in line: # Checking for the other condition, in this case logged out.
                        u2 = line.split("|")[4].split(" ")[2].rsplit("\\")[2] # Splitting the output again, this one is different than the previous, because the line has a different format.
                        d2_track[u2] = d2_track.get(u2,0) + 1 # Populating the second dict, we defined earlier.

            for key,value in d_track.items(): # Iterating over a dict (don't forget you have items - keys and values)            
                print('Username {} has logged in {} times in {}.'.format(key, value, log)) # Populating the print with the information we stored in d_track
            
            for key,value in d2_track.items(): # Iterating over a dict (don't forget you have items - keys and values)               
                print('Username {} has logged out {} times in {}.'.format(key, value, log)) # Populating the print with the information we stored in d2_track

        except ValueError: # If something goes wrong with the block below the script will raise an error and quit.
            print("Something went wrong while processing Lucid.log")
            exit()
            
    elif 'app.log' in log:
        try:
            d_track = {}
            d2_track = {}
            with open(log, "r") as file:
                for line in file:
                    if 'Updating lastLogin' in line:
                        u = line.split(" | ")[3].split(":")[1].rstrip('\n')
                        d_track[u] = d_track.get(u,0) + 1
                    elif 'Logged out ' in line:
                        u2 = (line.split(" | ")[3].split(" ")[2].rstrip('\n'))
                        d2_track[u2] = d2_track.get(u2,0) + 1
    
            for key,value in d_track.items():            
                print('Username{}has logged in {} times in {}.'.format(key, value, log))

            for key,value in d2_track.items():            
                print('Username {} has logged out {} times in {}.'.format(key, value, log))

        except ValueError:
            print("Something went wrong while processing app.log")
            exit()
    else:
        print('You are parsing the wrong file to the analyzer, please use Lucid.log or app.log') # This is a safety net, if the user tries to parse something else then app/Lucid.log it will report it and exit.
        exit()

def change_local_config_and_which(log):

    """
    I'm using this function to check the amount of times when users changed local configuration and which.
    """
    
    if 'Lucid.log' in log:
        try:
            d = {}
            with open(log, "rb") as f: 
                contents = str(f.read()).rsplit('\\n') 
                for line in contents: 
                    if 'ClientConfigManager |  New config stored' in line:
                        new_line = line.split(" | ")[4].split("[")[1].split(":")[0]
                        d[new_line] = d.get(new_line,0) + 1

            for key,value in d.items():            
                print('Local config {} was changed {} times in {}.'.format(key, value, log))

        except ValueError:
            print("Something went wrong while processing app.log")
            exit()

    elif 'app.log' in log :
        print('No local configuration change is being tracked in app.log! Skipping...') # I examined the app.log and I may be wrong here, but I do thing that any exit code other than 0 should be a good condition.
    
    else:
        print('You are parsing the wrong file to the analyzer, please use Lucid.log or app.log')
        exit()

def find_ungraceful_exits(log):

    """
    I'm using this function to find the amount of times when the daemon exited without explicit user action from the app.
    """

    counter = 0 # Instead of using a dict, I just have a simple integer which is counting the amount of issues we find in this function.

    if 'Lucid.log' in log:
        try:
            with open(log, "rb") as f: 
                contents = str(f.read()).split('\\r\\n') 
                for line in contents:
                    if 'Ungraceful exit detected!' in line: # While 'Ungraceful exit' is not a daemon exit, I would classify it as a useful thing to look for in Lucid.log
                        counter += 1
            print('LucidLink had {} ungraceful exits in {}'.format(counter, log))

        except ValueError:
            print("Something went wrong processing Lucid.log!")
            exit()    

    elif 'app.log' in log:
        try:
            with open(log, 'r') as f:
                for i in f:
                    if "Lucid daemon closed with code 1 " in i: # I examined the app.log and I may be wrong here, but I do think that any exit code other than 0 should be a good condition.
                            counter += 1
            print("Lucid daemon had {} exits with code 1.".format(counter))

        except ValueError:
            print("Something went wrong processing app.log!")
            exit()    

    else:
        print('Wrong file, please use Lucid.log or app.log')
        exit()       
    
if __name__ == '__main__':
    print("############################")
    print("        STARTING WORK    ")
    print("############################")
    print("1.1 Checking the amount of times when users logged in and logged out, and who logged in.")
    print("Processing...")
    report_log_in_log_out_and_user(args.log)
    print("############################")
    print("1.2 Checking the amount of times when users changed local configuration and which.")
    print("Processing...")
    change_local_config_and_which(args.log)    
    print("############################")
    print("Checking for the amount of times when the daemon exited without explicit user action from the app.")
    print("Processing...")
    find_ungraceful_exits(args.log)
    print("############################")
    print("         END WORK    ")
    print("############################")



