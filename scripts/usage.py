import sys

def usageget():
    print ""
    print "Usage:"
    print "The get argument is used To provide parameters to a stack launch"
    print "By default, the \"get\" argument will pull the information from simpledb"
    print ""
    print "  Example: "
    print "    %s get -s cto-mobile-VPC -r us-west-1" % (sys.argv[0])
    print "    -The -s and -r parameters are mandatory with this option"
    print ""
    print ""
    print "If you would like to pull the parameters from a file use the -f parameter and provide the filename(s)"
    print ""
    print "  Example: " 
    print "    file.json < \"{ \"cto-mobile\": { \"prod\": { \"us-west-1\" { \"VPCID\": \"vpc-123456\", \"MinimumInstances\": \"1\",}}}}\""
    print "    %s get -f ./file.json -p cto-mobile -e prod -r us-west-1"  % (sys.argv[0])
    print "    returns: \"-a VPCID=123456 -a MinimumInstances=1\""
    print "     -Multiple .json files may be passed using -f"
    print "     -When using \"-f file.json\", the -p -e and -r parameters are mandatory"
    print ""
    print ""
    print "For getting parameters from both a .json file and simpledb, use \"-f file.json\" and the \"-d\" flag"
    print ""
    print "  Example:"
    print "    %s get -f ./file.json -p cto-mobile -e prod -r us-west-1 -d -s cto-mobile-VPC" % (sys.argv[0])
    print "    -The stackname will need to be provided to pull the correct stack info from simpledb"
    print ""
    print " -n Flag will get the parameters from the simple_deploy based namespace in SimpleDB."
    print "    If the stack was launched with simple_deploy the stack cloudformation parameters will also be passed"
    print ""
    sys.exit(-1)

def usageput():
    print ""
    print "Usage:"
    print "The put argument will grab cloudformation stack resources and pass them to SimpleDB to be used as parameters for future stacks"
    print ""
    print "  Example: " 
    print "    %s put -s cto-mobile-prod-1 -r us-west-1" % (sys.argv[0])
    print ""
    print " -n Flag will store stack resources in the simple_deploy namespace also used for stack parameters."
    print "    This option enables both resources and parameters from this stack to be used as parameters"
    print "    for launching future stacks."
    sys.exit(-1)