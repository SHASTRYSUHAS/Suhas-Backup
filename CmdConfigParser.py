"""
    File Name            : CmdConfigParser.py
    Description          : Script with classes to parse the command line arguments for different scripts.
    Code Changes         : Initial Coding
    Author               : Suhas Shastry
    Initial Publish Date : 05/04/2021

Change History:
---------------
SI     Date           Modifier Name         Description
--     ----           ------------          -----------


"""

from optparse import OptionParser
import getpass
import re, sys
import os

"""
    -------------------------------------------------------------------
       Class to read the Command Line Arguments to create Build entry
    -------------------------------------------------------------------
"""

class AWSCliArgs:
    def __init__(self):
        self.parser = OptionParser()
        self.CLIargs = {}

    def setCLIArgs(self):
        self.parser.add_option('-l','--loc' ,dest="loc",help="<-AWS location              <Required>->")
        self.parser.add_option('-k','--acckey' ,dest="acckey",help="<-AWS Access Key              <Required>->")
        self.parser.add_option('-s','--secret' ,dest="secret",help="<-AWS secret key              <Required>->")
        self.parser.add_option('-r','--repo' ,dest="repo",help="<-ECR Repository Name     <Required>->")
        
            
        options, arguments = self.parser.parse_args()

        argsCount = 0
 
        if(options.loc):
            awsLocation = options.loc
            self.CLIargs.update({'Location':awsLocation})
            argsCount+=1
        else:
            self.CLIargs.update({'Location':None})
            
        if(options.acckey):
            accesskey = options.acckey
            self.CLIargs.update({'AccessKey':accesskey})
            argsCount+=1
        else:
           self.CLIargs.update({'AccessKey':None})            
            
        if(options.secret):
            secretKey = options.secret
            self.CLIargs.update({'SecretKey':secretKey})
            argsCount+=1
        else:
            self.CLIargs.update({'SecretKey':None})

        if(options.repo):
            repository = options.repo
            self.CLIargs.update({'Repository':repository})
            argsCount+=1
        else:
            self.CLIargs.update({'Repository':None})        

        if argsCount == 0:
            print ("\nERROR: No arguments provided!! Please provide the options as mentioned in Usage below\n")
            self.parser.print_help()
            sys.exit(-1)

    def printCmdArgs(self):
        cmdDictItems = self.CLIargs.items()

        for item in cmdDictItems:
            print (item[0],":",item[1])

    def verifyCmdArgs(self):
        missingInput = ''
        cmdDictItems = self.CLIargs.items()
                
        for item in cmdDictItems:
            key = item[0]
            argVal = item [1]

            if (argVal == None):                
                missingInput = missingInput + '\'' + str(key) + '\' '
                            
        if (missingInput != ''):
            self.printUsageMsg(missingInput)

        return missingInput

    def printUsageMsg(self,missingInput):
        print ("ERROR: Insufficient or Invalid Options!! Please provide the options as mentioned in Usage below\n")
        print ("Missing or wrong Input: ",missingInput,"\n")
        self.parser.print_help()
        sys.exit(-1)
