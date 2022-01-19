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
   echo "    1. If there are spaces in any field of excel, spaces will be removed"
   echo "    ex. Excel        ->    Feature With Spaces"
   echo "        New script   ->    FeatureWithSpaces"
   echo "    2. When using scipt without option, tags in new script will always arrange in the following format"
   echo "    [Tags]    {Feature}    {SubFeature}    {TagsInExcel}    {Defects}"
   echo
   echo "    3. When using -m option, tags in new script will always arrange in the following format"
   echo "    [Tags]    {Feature}    {SubFeature}    {TagsInExcel}    {Defects}    {TagsInOldScript}"
   echo
   echo "    4. If tags are duplicated in old script, new script will generate only one of each"
   echo "    ex. Old script   ->    [Tags]    DuplicatedTag    DuplicatedTag    NotDuplicatedTag"
   echo "        New script   ->    [Tags]    DuplicatedTag    NotDuplicatedTag"
   echo
   echo "    5. If tag in old script is sperated by one space, this tag will be generated into different tags"
   echo "    ex. Old script   ->    [Tags]    This is one tag"
   echo "        New script   ->    [Tags]    This    is    one    tag"
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
