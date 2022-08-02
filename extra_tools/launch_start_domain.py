#! /usr/bin python
import os

# Function to get the domain1 running status
def is_domain_running(log_file):
    res = False
    with open(log_file,"r") as op:
        line = op.readlines()
        try:
            run = line[1]
            split = run.split(" ")
            if split[1] == "not":
                res = False
            else:
                res = True
        except:
            res = False

    return res

# Output the domain status in domain.log file
os.system("(date;/usr/local/payara5/bin/asadmin list-domains) > domain.log")

# Check if domain running and start domain if any
running = is_domain_running("domain.log")
if running == True:
    os.system("echo '******** OK: system still running *********' >> domain.log")
else:
    os.system("/usr/local/payara5/bin/asadmin start-domain >> domain.log")


