#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "DESCRIPTION:"
   echo "    This script will create new robotframework script, which update documentation and tags depended on user's option."
   echo
   echo "SYNTAX:"
   echo "    run.sh [-h|m] file.xlsx script1.robot script2.robot"
   echo
   echo "OPTIONS:"
   echo "    h   Print this Help."
   echo "    m   Merge tags from file.xlsx with scrip1.robot (keep only tags in file.xlsx by default)"
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

TAGOPTION=n
BASEDIR=$(dirname "$0")
SCRIPTNAME="robotframework_template_generator.py"
while getopts ":hm" option; do
    case $option in
        h ) # display Help
            Help
            exit;;
        m )
            TAGOPTION=y
            python3 $BASEDIR/$SCRIPTNAME $2 $3 $4 $TAGOPTION
            exit;;
        \? )
            echo "Error: Invalid option"
            exit;;
   esac
done
# If option is not set
python3 $BASEDIR/$SCRIPTNAME $1 $2 $3 $TAGOPTION
