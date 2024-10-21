# Draw.io Code Generator

<div>
    <img src="./github_assets/drawio.jpg" width="125" height="125" alt="drawio_logo">
    <img src="./github_assets/plus.png" width="125" height="125" alt="plus_sign" style="padding-left:15px; padding-right:15px;"/>
    <img src="./github_assets/python.png" width="125" height="125" alt="python_logo">
    <img src="./github_assets/equal.png" width="125" height="125" alt="equal_sign" style="padding-left:15px; padding-right:15px;">
    <img src="./github_assets/code.png" width="125" height="125" alt="java_logo">
</div>

### Generate source code from [draw.io](https://draw.io/) UML class diagrams

Supported languages are: Java, C#, C++, Python, TypeScript, PHP and SQL.

<div>
    <img src="./github_assets/simple_class_diagram.jpg" width="400" height="400" alt="drawio_logo"/>
</div>

## About this fork

* This is a fork of the https://github.com/Daandelange/DrawioCodeGenerator repository. 
* It adds a [wxPython](https://wxpython.org/) based GUI.
* Code generators were added for C#, C++, PHP, Python and SQL.
* There are also improvements on the generation of property accessors.
* The generated style and syntax trees are displayed on the GUI.

## Setup

````bash
# pipenv was replaced by virtualenv
python -m venv ./venv

# activate the virtual environment
./venv/Scripts/activate # or activate.bat or activate.ps1 according to your shell

# Install dependencies
pip install -r requirements.txt
````

## Usage

Run the example :
````bash
# Compiles the diagram to both Java an Typescript code
python3 main.py # python main.py on Windows
````

## State

The generator still crashes on some UML class diagrams, but it can be very helpful as compared to manually implementing all classes.
