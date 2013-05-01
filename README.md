Stackify
========

The goal of Stackify is to easily keep track of cloudformation parameters for multiple regions and AWS environments.

 Stackify has a few options for managing cloudformation parameters. Parameters can be stored in a json format, or can be stored in simpleDB. Stackify will pull resource id information about a stack and store it for us in SimpleDb, these can later be passed as parameters for launching future stacks.   Stackify is made to integrate with simple\_deploy. After a stack is created with simple\_deploy stackify is then ran using the stack name and region, all resource information about the stack is added to simpleDB under the 'stacks' domain. This is especially useful for launching a cloudformation stack for your VPC/Subnets, and then launching a stack inside of the VPC. Non AWS resource specific parameters should be stored using the json alternative.
 Stackify has a few options for managing cloudformation parameters. Parameters can be stored in a json format, or can be stored in simpleDB. Stackify will pull resource id information about a stack and store it for us in SimpleDb, these can later be passed as parameters for launching future stacks.   Stackify is made to integrate with simple_deploy. After a stack is created with simple_deploy stackify is then ran using the stack name and region, all resource information about the stack is added to simpleDB under the 'stacks' domain. This is especially useful for launching a cloudformation stack for your VPC/Subnets, and then launching a stack inside of the VPC. Non AWS resource specific parameters should be stored using the json alternative.

Prerequisites
-------------

* Python version 2.6 or higher installed.
* Boto Version 2.5 or higher
* AWS account access key and secret key (or IAM role but currently untested).

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
```
* an IAM role can be defined using the -i parameter during the script run instead of setting the keys as environmental variables.

Set the stackify file as executable

```
chmod 550 ./stackify
```

Documentation
-----------

### stackify put


The **'put'** argument is used to save stack resource information to SimpleDB.
This should be ran after succefully launching a stack using __'simple\_deploy'__ to enable the resources to be used as parameters for future stacks.
The __-s__ and __-r__ parameters are mandatory with this option

Example:
``` 
./stackify put -s cto-mobile-VPC -r us-west-1        
```

### stackify get

The **'get'** argument is used to provide parameters to simple\_deploy when launching a stack.
By default, the 'get' argument will pull the saved resource information from simpledb to be used for launching a stack.

#### Passing Parameters from SimpleDB

* The __-d/--db__ option will be assumed unless __-f/--file__  option is used.  
* The __-s/--stack__ and __-r/--region__ options are mandatory when not using __-f/--file__
* The __-n/--simpledeployname__ option will store resource information about the stack in the same place simple\_deploy stores parameters, this enables the simple\_deploy parameters to be passed to future stacks also

Example: 
```
./stackify get -s cto-mobile-VPC -r us-west-1        
```

#### Passing Parameters from a .json file

* If you would like to pull the parameters from a json formatted file you can use the options: **"-f filename(s) -p project -e environment  -r region"**
  
Example: 
1. Create json formatted file parameters with project, environment, region and key value pairs.

```
file.json < '{ "cto-mobile": { "prod": { "us-west-1" { "VPCID": "vpc-123456", "MinimumInstances": "1",}}}}'
```

2. Run stackify with _'-f pathto/file.json'_

```
stackify get -f ./file.json -p cto-mobile -e prod -r us-west-1
```

* This returns the key value pairs from the json file in a simple\_deploy compatible parameter format: '-a VPCID=123456 -a MinimumInstances=1'

* Multiple .json files may be passed using __-f__
 
* When using the __-f__ option, the __-p -e__ and __-r__ parameters are mandatory

* The __-n/--simpledeployname__ option will pull resource information about the stack from the simple\_deploy parameter store, this enables the simple\_deploy parameters to be passed to future stacks along with the resources
  

#### Passing Parameters from both a File and Database

Parameters can be pulled from both a json file and the SimpleDB saved parameters. 

If you'd like to specify parameters from both a .json file and from simpledb, use __-f file.json__ and the __-d__ flag
    
Example:

```
stackify get -f ./file.json -p cto-mobile -e prod -r us-west-1 -d -s cto-mobile-VPC
```

__'-d -s cto-mobile-VPC'__ was added. The stackname will need to be provided to pull the correct stack info from simpledb when using the database __-d__ flag. 

* Multiple stacknames may be provided to __-s__

* __-i__ <iam role name> may be used to use an iam role instead of passing access & secret keys (currently untested)

#### Using with simple\_deploy:

 * We use backticks to pass the output from stackify in-line to our simple\_deploy stack creation jobs as parameters:

Example:

```
simple_deploy create -e cto-mobile-prod-us-west-1 -n cto-mobile-cd-us-west-1 -t ./CloudFormation/ASG.json  `stackify get -r us-west-1 -p cto-mobile -e prod -f ./params.json -d -s cto-mobile-VPC`
```
