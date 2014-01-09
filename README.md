Stackify
========
Stackify manages your Cloudformation parameters for multiple AWS regions, environments and accounts. Stackify pulls necessary information about your current Cloudformation stacks, and then dynamically generates the necessary parameters for your next stack launch.  It does this through pulling resource information about a stack and storing it for you in SimpleDb, this information can then be passed as parameters for launching future dependent stacks. Stackify helps make launching servers in a VPC a breeze!   

Usage
-----
Stackify is made to integrate with simple\_deploy. After a stack is created with simple\_deploy, "stackify put ..." is then ran for the created stack and all resource information about the stack and outputs defined, are then stored in the region's simpleDB 'stacks' domain. This is especially useful for launching a Cloudformation stack for your VPC, and then launching a stack inside of that VPC. Non-AWS resource specific parameters should be stored using the alternate json method. Parameters from a json formatted file and/or from simpleDB are then provided to the CAP simple\_deploy job for the creation of new stacks.

Prerequisites
-------------

* Python 2.x version 2.6 or higher installed.
* Boto Version 2.9.9 or higher (will be installed automatically during the setup.py install)
* AWS account access key and secret key or IAM Instance Role with SimpleDB read/write and Cloudformation read-only access on the machine running stackify

Installation
------------

Install python if necessary (most current distributions will have python 2.6 or higher)

python setuptools and pip must be installed

If necessary run: 

```
yum install python-setuptools
easy_install pip
```

Run the setup.py installation from the stackify folder

```
python setup.py install
```

* this will install the necessary libraries, and the stackify command to: /usr/bin/stackify


AWS API Access
--------------

Set access and secret keys as environmental variables or use IAM instance role with access for simpledb (read/write) and cloudformation (read).

```
export AWS_ACCESS_KEY_ID=<AWS Access Key ID>
export AWS_SECRET_ACCESS_KEY=<AWS Secret Access key>
```

If using an IAM instance role with SDB and CF permission, then access should be provided automagically!


Documentation
-----------

### stackify put


The **'put'** argument is used to save stack resource and output information to SimpleDB.
This should be ran after succefully launching a stack using __'simple\_deploy'__ to enable the resources to be used as parameters for future stacks.
The __-s__ and __-r__ parameters are mandatory with this argument


Example:
``` 
./stackify put -s STACKNAME-VPC -r us-west-1        
```

* The __-n/--simpledeployname__ flag will put resource information about the stack into the SimpleDB namespace used by the simple\_deploy parameter store, and the simple\_deploy parameters of a stack will then also be passed to future stacks
* Stackify 'put' will force an overwrite of any old parameters in SimpleDB with the same key name and same stackname



### stackify get

The **'get'** argument is used to provide parameters to simple\_deploy when launching a stack.
By default, the 'get' argument will pull the saved resource information from simpledb to be used for launching a stack.



#### Passing Parameters from SimpleDB

* The __-d/--db__ option will be assumed unless __-f/--file__  option is used.  
* The __-s/--stack__ and __-r/--region__ options are mandatory when pulling parameters from SimpleDB
* The __-n/--simpledeployname__ flag will get the resource information about the stack from the SimpleDB namespace used by simple\_deploy to store parameters, this enables the simple\_deploy parameters to be passed to new stacks as well
* Cloudformation Outputs will take precedence over Cloudformation resources if they have the same name.

Example: 
```
./stackify get -s STACKNAME-VPC -r us-west-1        
```



#### Passing Parameters from a .json file

* If you would like to pull the parameters from a json formatted file you can use the options: **"-f filename(s) -p projectname -e environment  -r region"**
  
Example: 
1. Create a json formatted file with the projectname key(s), nesting environment(s) then region(s), with parameters as key value pairs:

```
file.json < '{ "projectname": { "prod": { "us-west-1" { "VPCID": "vpc-123456", "MinimumInstances": "1",}}}}'
```

2. Run stackify get with _'-f pathto/file.json'_ 

```
stackify get -f ./file.json -p projectname -e prod -r us-west-1
```

* This returns the key value pairs from the json file in a simple\_deploy compatible parameter format: '-a VPCID=123456 -a MinimumInstances=1'

* Multiple .json files may be passed using __-f__
 
* When using the __-f__ option, the __-p -e__ and __-r__ parameters are mandatory





#### Passing Parameters from both a File and Database

Parameters can be pulled from both a json file and the SimpleDB saved parameters. 

If you'd like to specify parameters from both a .json file and from simpledb, use __-f file.json__ and the __-d__ flag
    
Example:

```
stackify get -f ./file.json -p projectname -e prod -r us-west-1 -d -s STACKNAME-VPC
```

__'-d -s STACKNAME-VPC'__ was added. When using the database __-d__ flag, the stackname will need to be provided to pull a specific stack's information from simpledb. 

* Multiple stacknames may be provided to __-s__
* The __-n/--simpledeployname__ flag will pull resource information about the stack from the simple\_deploy parameter store namespace in SimpleDB, this enables the simple\_deploy parameters to be passed to future stacks along with the resources


#### Using with simple\_deploy:

 * We usually just use backticks to pass the output from stackify in-line to our simple\_deploy stack creation jobs as parameters:

Example:

```
simple_deploy create -e Simple_Deploy_Environment -n STACKNAME-VPC -t ./CloudFormation/ASG.json  `stackify get -p projectname -e prod -r us-west-1 -f ./params.json -d -s STACKNAME-VPC`
```
or 

```
parameters=`stackify get -p projectname -e prod -r us-west-1 -f ./params.json -d -s STACKNAME-VPC`
simple_deploy create -e Simple_Deploy_Environment -n STACKNAME-VPC -t ./CloudFormation/ASG.json ${parameters}
```

#### Using simple_deploy and Stackify in Jenkins

When running in a Jenkins job you may find that Jenkins adds extra quotes around the full key/value pairs in addition to just the values. For some reason Jenkins doesn't like the quotes when running stackify using backticks and adds extra single quotes around the key value pairs. To avoid this pass the simple_deploy job and stackify outputs to a shell script:

```
#Create Simple_Deploy creation shell script, use -n to remove trailing newline
echo -n 'simple_deploy create -e myenvironment -n stack -t Cloudformation-Templates/stack.json ' > ./simple_deploy_run.sh 

#Add stackify parameters to simple_deploy shell script
echo "`stackify get -f params.json -p projectname -e dev -r us-east-1 -d -s vpc-stack -n`" >> ./simple_deploy_run.sh

#Make Executable and Run simple_deploy
chmod 755 ./simple_deploy_run.sh
./simple_deploy_run.sh

```

