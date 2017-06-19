from os import path
import subprocess as sub

class HostFileManger:
    def __init__( self ):
        self.hosts = []
        self.slots = []
        self.include = []
        self.allowedUsersToBeLoggedIn = []

    def read( self, templateFile ):
        """
        Reads all the hosts from the template file
        """
        self.hosts = []
        self.slots = []
        infile = open( templateFile, "r" )
        for line in infile.readlines():
            splitted = line.split(" ")
            self.hosts.append(splitted[0])
            self.slots.append(splitted[1])
            self.include.append(True)
        infile.close()
        print ("Total number of available hosts %d"%(len(self.hosts)))

    def createPasswordLessAccess( self, username ):
        """
        Loops accross all the IP addresses in the hosts array and adds the current key to the
        authorized key directory
        """
        home = path.expanduser("~")
        for host in self.hosts:
            # Create a directory named .ssh
            sub.call(["ssh", username+"@"+host, "mkdir", "-p", ".ssh"] )

            # Add the ID of this computer to the authorized keys
            sub.call('cat %s/.ssh/id_rsa.pub | ssh %s@%s \'cat >> .ssh/authorized_keys\''%(home,username,host), shell=True)
        print ( "All nodes can now be logged onto without password")

    def toggleIncludeFlag( self, node ):
        """
        Set the include flag to false for nodes where other users are logged in
        """
        who = open("who.txt", 'r' )
        lines = who.readlines()
        who.close()
        for line in lines:
            user = line.split(" ")[0]
            if ( not user in self.allowedUsersToBeLoggedIn ):
                self.include[node] = False
                print ("User %s was logged in. Disabling this node."%(user))

    def filterHostFile( self, username ):
        """
        Checks all the hosts and include all hosts where there are no users
        """
        for i in range(len(self.hosts)):
            print ("Checking host: %s"%(self.hosts[i]))
            sub.call( ["ssh", username+"@"+self.hosts[i], "who > who.txt"] )

            # Retrieve the output from who
            sub.call( ["scp", username+"@"+self.hosts[i]+":who.txt", "./"])
            self.toggleIncludeFlag(i)
            sub.call( ["ssh", username+"@"+self.hosts[i], "rm who.txt"] )

    def save( self, fname ):
        out = open( fname, 'w' )
        for i in range(len(self.hosts) ):
            if ( self.include[i] ):
                out.write("%s %s"%(self.hosts[i],self.slots[i]))
        out.close()
        print ("New host file written to %s"%(fname))
