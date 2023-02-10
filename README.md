
# Description
---
This project is for generating robotframework script file. Supporting both new test file and existing file. In case of existing file, this script will update the existing one according to the excel.  

## Excel File Structure
---

Excel file must has column name and column index according to table below  

|Column Name|Mandatory/Optional|
|--|--|
|Feature|M|
|Sub Feature|M|
|Test Cases No.|M|
|Test Objective|M|
|Priority|M|
|Tag / Requirement Ref.|O|
|Defects|O|

## Result Robot Script File
---
Robotframework script generated by this project will be in format below.
```
*** Settings ***
{Existing Script}

*** Variables *** (If exists in old robot file)
{Existing Script}

*** Test Cases ***
{Test Cases No. in excel}
    [Documentation]    {Test Case Name in excel}
    [Tags]    {Priority in Excel File}    {Tags in Excel File}    {Defects}    NotReady
    {Existing Script}

{Existing Script}
.
.
.

*** Keywords *** (If exists in old robot file)
{Existing Script}
```

## How to install
---  

- Clone this repository  
```shell
git clone https://github.com/worachai3/robotframework_template_generator.git
```  

- Double click RobotTemplateGenerator.dmg then drag RobotTemplateGenerator into Applications


- Required files  
```
{testcases}.xlsx
{old_robot_file}.robot (Optional)
```  