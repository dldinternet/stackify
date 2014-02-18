##v1.4.1 (02/18/14)

* Fixed bug writing outputs to sdb 
* Added the sdb consistent_read option to ensure all data is available when a stacks information is accessed, immediately after it is written.

##v1.4.0 (11/6/13)

* Migrated from optparse to argparse to parse arguments for cleaner help output
* Now wrapping output values with double quotes, fixes issue passing parameters containing spaces
* Restructured functions. 
* Moved usage out to seperate file.
* Removed -d flag to make parameter usage less confusing

##v1.3.0 (6/5/13)

* Enable passing cloudformation outputs to SimpleDB.  This is useful when building inter-dependent projects 
* IAM Roles tested and work without having to define role (Boto 2.6+)
* The timestamp has changed for Cloudformation stacks, must use Boto >= 2.9.9, Updated setup.py (https://github.com/boto/boto/issues/1582)
