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
   echo "    run.sh [-h|-m] test_cases_file.xlsx old_script.robot new_script.robot"
   echo
   echo "OPTIONS:"
   echo "    h   Print this Help."
   echo "    m   Merge tags from file.xlsx with scrip1.robot (keep only tags in file.xlsx by default)"
   echo
   echo "REMARKS:"
   echo "    1. When using scipt without option, tags in new script will always arrange in the following format"
   echo "    [Tags]    {Feature}    {SubFeature}    {TagsInExcel}    {Defects}"
   echo
   echo "    2. When using -m option, tags in new script will always arrange in the following format"
   echo "    [Tags]    {Feature}    {SubFeature}    {TagsInExcel}    {Defects}    {TagsInOldScript}"
   echo
   echo "    3. If tags are duplicated, new script will get each one of those duplicated tags will be generated one of each"
   echo "    ex. OLD  ->    [Tags]    DuplicatedTag    DuplicatedTag    NotDuplicatedTag"
   echo "        NEW ->    [Tags]    DuplicatedTag    NotDuplicatedTag"
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
