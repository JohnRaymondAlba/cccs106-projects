# Lab 1 Report: Environment Setup and Python Basics

**Student Name:** John Raymond Alba\
**Student ID:** 231002271\
**Section:** 3A\
**Date:** August 2,2025

## Environment Setup

### Python Installation
- **Python Version:** 3.13.5
- **Installation Issues:** None
- **Virtual Environment Created:** ✅ cccs106_env_alba

### VS Code Configuration
- **VS Code Version:** 1.103.2
- **Python Extension:** ✅ Installed and configured
- **Interpreter:** ✅ Set to cccs106_env_alba/Scripts/python.exe

### Package Installation
- **Flet Version:** 0.28.3
- **Other Packages:** 
anyio==4.10.0\
certifi==2025.8.3\
flet==0.28.3\
h11==0.16.0\
httpcore==1.0.9\
httpx==0.28.1\
idna==3.10\
oauthlib==3.3.1\
repath==0.9.0\
six==1.17.0\
sniffio==1.3.1


## Programs Created

### 1. hello_world.py
- **Status:** ✅ Completed
- **Features:** Student info display, age calculation, system info
- **Notes:** The template that was given works fine. I did not encounter any errors / difficulties in changing the details of the code.

### 2. basic_calculator.py
- **Status:** ✅ Completed
- **Features:** Basic arithmetic, error handling, min/max calculation
- **Notes:** The challenge in this part was to modify the code by adding advanced operations and making it handle errors.

## Challenges and Solutions

I was clueless when I encountered an error in which it was said that I cannot load the cccs106_env_alba\Scripts\activate since the running scripts is disabled on the system. The solution was simple, I just need to bypass the policy thru this command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser". I would like to thank Google for this wonderful solution.

## Learning Outcomes

From this activity, I learned how to install python and set up the virtual environment. I also learn how to modify the the settings on VS Code. Lastly, I learned how to create a markdown and what are some of its syntaxes.

## Screenshots
"Add Week 2 labs: Flet GUI applications

- hello_flet.py: Basic Flet introduction with interactive elements
- personal_info_gui.py: Enhanced personal information manager with GUI
- Both applications use Flet 0.28.3 syntax and modern UI components"

### 2. VS Code Setup
![VS Code Setup](/cccs106-projects/week1_labs/lab1_screenshots/vscode_setup.png "VS Code Setup")

### 3. Hello World Output
![Hello World](/cccs106-projects/week1_labs/lab1_screenshots/hello_world_output.png "Hello World")

### 4. Basic Calculator (advanced) Output
![Basic Calculator](/cccs106-projects/week1_labs/lab1_screenshots/basic_calculator_output.png "Basic Calculator")