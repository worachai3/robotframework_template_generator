#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Add description of the script functions here."
   echo
   echo "Syntax: scriptTemplate [-g|h|v|V]"
   echo "options:"
   echo "g     Print the GPL license notification."
   echo "h     Print this Help."
   echo "v     Verbose mode."
   echo "V     Print software version and exit."
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

# TAGOPTION=n
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
            exit;;
   esac
done

if [ "$RUN" = true ]
    then
        python robotframework_template_generator.py $1 $2 $3 "$TAGOPTION"
fi
