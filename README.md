Stackify
========

The goal of Stackify is to easily keep track of cloudformation parameters for multiple regions and AWS environments.

 Stackify has a few options for managing cloudformation parameters. Parameters can be stored in a json format, or can be stored in simpleDB. Stackify will pull resource id information about a stack and store it for us in SimpleDb, these can later be passed as parameters for launching future stacks.   Stackify is made to integrate with simple_deploy. After a stack is created with simple_deploy stackify is then ran using the stack name and region, all resource information about the stack is added to simpleDB under the 'stacks' domain. This is especially useful for launching a cloudformation stack for your VPC/Subnets, and then launching a stack inside of the VPC. Non AWS resource specific parameters should be stored using the json alternative.

Prerequisites
-------------

* Python version 2.6 or higher installed.
* Boto Version 2.5 or higher
* AWS account access key and secret key or IAM role.

Installation
------------

Install python if necessary (most current distributions will have python 2.6 or higher)
Install boto

```
easy_install boto
```

Set access and secret keys as environmental variables or use IAM roles if using in amazon (simpledb and cloudformation access).

```
export AWS_ACCESS_KEY_ID=<AWS Access Key ID>
export AWS_SECRET_ACCESS_KEY=<AWS Secret Access key>
  
# an IAM role can be defined using the -i parameter during the script run instead of setting the keys as environmental variables.

```
Set the stackify file as executable

'''
chmod 550 ./stackify
'''

Documentation
-------------

$ stackify put

The "put" argument is used to save stack resource information to SimpleDB for launching future stacks.
This can be ran after succefully launching a stack using simple_deploy.
The -s and -r parameters are mandatory with this option

'''
      Example: 
        ./stackify put -s cto-mobile-VPC -r us-west-1
        
'''

$ stackify get

The "get" argument is used to provide parameters to simple_deploy when launching a stack.
By default, the "get" argument will pull the saved resource information from simpledb to be used for launching a stack.  
The -s and -r parameters are mandatory with this option when not using -f


	  Example: 
'''
        ./stackify get -s cto-mobile-VPC -r us-west-1
        
'''

    If you would like to pull the parameters from a file you can use the parameters: -f filename(s) -p project -e environment  -r region
    
      Example: 
      '''
        file.json < '{ "cto-mobile": { "prod": { "us-west-1" { "VPCID": "vpc-123456", "MinimumInstances": "1",}}}}'

        stackify get -f ./file.json -p cto-mobile -e prod -r us-west-1
      '''
        This returns the key value pairs from the json file in a simple_deploy compatible parameter format: "-a VPCID=123456 -a MinimumInstances=1"
         -Multiple .json files may be passed using -f
         -When using "-f file.json", the "-p" "-e" and "-r" parameters are mandatory
    
    For getting parameters from both a .json file and simpledb parameter information, use "-f file.json" and the "-d" flag
    
      Example:
      '''
        stackify get -f ./file.json -p cto-mobile -e prod -r us-west-1 -d -s cto-mobile-VPC
      '''
        "-d -s cto-mobile-VPC" was added. The stackname will need to be provided to pull the correct stack info from simpledb when using the database -d call. 
        -Multiple stacknames may be provided to -s
    
     -i <iam role name> may be used to use an iam role instead of passing access & secret keys"


Using with simple_deploy:
	We use backticks to pass the parameters from stackify to our simple_deploy stack creation jobs:

	  Example:
	  '''
		simple_deploy create -e cto-mobile-prod-us-west-1 -n cto-mobile-cd-us-west-1 -t ./CloudFormation/ASG.json  `stackify get -r us-west-1 -p cto-mobile -e prod -f ./params.json -d -s cto-mobile-VPC`
	  '''

