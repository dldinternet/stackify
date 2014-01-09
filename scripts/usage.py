import sys

def usageget():
    print '''
    Usage:
    The get argument is used To provide parameters to a stack launch
    
      Example: 
        stackify get -s cto-mobile-VPC -r us-west-1

      * The -s and -r parameters are mandatory with this option
    
    
    If you would like to pull the parameters from a file use the -f parameter and provide the filename(s)
    
      Example: 
        file.json < \"{ \"cto-mobile\": { \"prod\": { \"us-west-1\" { \"VPCID\": \"vpc-123456\", \"MinimumInstances\": \"1\",}}}}\"
        stackify get -f ./file.json -p cto-mobile -e prod -r us-west-1 
        
      * Multiple .json files may be passed using -f. (-p -e and -r parameters are mandatory)
    
    
    For getting parameters from both a .json file and simpledb, use \"-f\" and \"-s\" options
    
      Example:
        stackify get -f ./file.json -p cto-mobile -e prod -r us-west-1 -s cto-mobile-VPC 
      
      * -The stackname will need to be provided to pull the correct stack info from simpledb
      * The -n Flag will get the parameters from the simple_deploy namespace in SimpleDB.
    '''
    sys.exit(-1)

def usageput():
    print '''
    Usage:
    The put argument will grab cloudformation stack resources and pass them to SimpleDB to be used as parameters for future stacks
    
      Example: 
        stackify put -s cto-mobile-prod-1 -r us-west-1
    
      * The -n Flag will store stack resources in the simple_deploy namespace also used for stack parameters.
        This option enables both resources and parameters from this stack to be used as parameters
        for launching future stacks.
    '''
    sys.exit(-1)