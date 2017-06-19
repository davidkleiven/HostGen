from __future__ import print_function
import sys
import hostfileManager as hm

def main( argv ):
    manager = hm.HostFileManger()
    fname = ""
    username = ""
    for arg in argv:
        if ( arg.find("--file=") != -1 ):
            fname = arg.split("--file=")[1]
        elif ( arg.find("--user=") != -1 ):
            username = arg.split("--user=")[1]

    if ( fname == "" ):
        print ("No template filename given!")
        return
    elif ( username == "" ):
        print ("No username specified!")
        return

    manager.read(fname)
    # Check optinos
    for arg in argv:
        if ( arg.find("--init") != -1 ):
            # Create password less access
            manager.createPasswordLessAccess( username )

        elif ( arg.find("--out=") != -1 ):
            outfname = arg.split("--out=")[1]
            manager.filterHostFile( username )
            manager.save( outfname )

if __name__ == "__main__":
    main( sys.argv[1:] )
