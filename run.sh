#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "DESCRIPTION"
   echo "This script will create new robotframework script, which update documentation and tags depended on user's option."
   echo
   echo "Syntax: run.sh [-h|m] file.xlsx script1.robot script2.robot"
   echo
   echo "options:"
   echo "h     Print this Help."
   echo "m     Merge tags from file.xlsx with scrip1.robot.(keep only tags in file.xlsx by default)"
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

RUN=true
TAGOPTION=n
while getopts ":hm" option; do
    case $option in
        h ) # display Help
            Help
            RUN=false
            exit;;
        m )
            TAGOPTION=y
            python3 robotframework_template_generator.py $2 $3 $4 $TAGOPTION
            exit;;
        \? )
            echo "Error: Invalid option"
            RUN=false
            exit;;
   esac
done
# If option is not set
python3 robotframework_template_generator.py $1 $2 $3 $TAGOPTION
