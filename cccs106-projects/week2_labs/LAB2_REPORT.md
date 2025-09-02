# Lab 2 Report: Git Version Control and Flet GUI Development

**Student Name:** John Raymond Alba \
**Student ID:** 231002271 \
**Section:** BSCS 3A \
**Date:** September 9, 2025 

## Git Configuration

### Repository Setup
- **GitHub Repository:** https://github.com/JohnRaymondAlba/cccs106-projects.git
- **Local Repository:** ✅ Initialized and connected
- **Commit History:** [Number] commits with descriptive messages

### Git Skills Demonstrated
- ✅ Repository initialization and configuration
- ✅ Adding, committing, and pushing changes
- ✅ Branch creation and merging
- ✅ Remote repository management

## Flet GUI Applications

### 1. hello_flet.py
- **Status:** ✅ Completed
- **Features:** Interactive greeting, student info display, dialog boxes
- **UI Components:** Text, TextField, Buttons, Dialog, Containers
- **Notes:** In the original code, the "app info" button does not show the dialog box when clicked. The button does nothing therefore, some modification is made in the function "show_info".

### 2. personal_info_gui.py
- **Status:** ✅ Completed
- **Features:** Form inputs, dropdowns, radio buttons, profile generation
- **UI Components:** TextField, Dropdown, RadioGroup, Containers, Scrolling
- **Error Handling:** Input validation and user feedback
- **Notes:** The code worked well. It do generate the student profile as long as the name and age is filled. All fields works and both buttons that is present in the application does function as intended.

## Technical Skills Developed

### Git Version Control
- Understanding of repository concepts
- Basic Git workflow (add, commit, push)
- Branch management and merging
- Remote repository collaboration

### Flet GUI Development
- Flet 0.28.3 syntax and components
- Page configuration and layout management
- Event handling and user interaction
- Modern UI design principles

## Challenges and Solutions

I have a hard time in finding why the program shows that I did not install flet even though I installed it right. I have a hard time (almost an hour) finding where did I go wrong, tracing back every step that I took. Even chatgpts' answers won't solve the problem that I am having here at VSCode. Turns out, I just need to run the program in the dedicated terminal.

Another problem that I encountered is when I noticed that a button from the hello_flet.py won't work. The solution is just modifying a line in the code so that the dialog box would appear when the "app info" button is clicked.

## Learning Outcomes

[Reflect on what you learned about version control, GUI development, and collaborative programming]

## Screenshots

### Git Repository
- [ ] GitHub repository with commit history
- [ ] Local git log showing commits

### GUI Applications
- hello_flet.py running with all features
![](/cccs106-projects/week2_labs/lab2_screenshots/hello_flet.png "hello_flet")

- personal_info_gui.py with filled form and generated profile
![](/cccs106-projects/week2_labs/lab2_screenshots/personal_info_gui.png "personal_info_gui")

## Future Enhancements

[Ideas for improving the applications or additional features to implement]