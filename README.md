
# Description
---
This project is for generating robotframework script file. Supporting both new test file and existing file. In case of existing file, this script will update the existing one according to the excel.  

## Prerequisite
---
Install required package
```shell
pip install -r requirement.txt
```

## Excel File Structure
---

![alt text](https://www.img.in.th/images/46f85264e853bfdc14ba83d8b738eefa.png)

Excel file must has column name and column index according to table below  

|Column Index|Column Name|
|--|--|
|D|Test Cases No.|
|E|Test Cases Name|
|M|Priority|
|Q|Tag / Requirement Ref.|
|Y|Defects|  

## Result File
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

## How to run
---  

- Clone this repository  
```shell
git clone https://github.com/worachai3/robotframework_template_generator.git
```  

- Required files  
```
{testcases}.xlsx
{old_robot_file}.robot
{new_robot_file}.robot (this file will be created if not already exists)
```  

- Run shell script  
```shell
./run.sh [-h|m] {testcase_file_name}.xlsx {old_robot_file}.robot {new_robot_file}.robot
```

## Note
---

For more detail, please run command.
```shell
./run.sh -h
```
