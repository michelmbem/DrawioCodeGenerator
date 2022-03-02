# Java Code Generator

<div style="display: inline-block">
    <img src="./github_assets/drawio.jpg" width="125" height="125" alt="drawio_logo"/>
    <img src="./github_assets/plus.png" width="125" height="125" alt="plus_sign" style="padding-left:15px; padding-right:15px;"/>
    <img src="./github_assets/python.png" width="125" height="125" alt="python_logo"/>
    <img src="./github_assets/equal.png" width="125" height="125" alt="equal_sign" style="padding-left:15px; padding-right:15px;"/>
    <img src="./github_assets/java.png" width="125" height="125" alt="java_logo"/>
</div>

### Generate Java code from [draw.io](https://draw.io/) UML class diagrams

<div style="display: inline-block">
    <img src="./github_assets/simple_class_diagram.jpg" width="400" height="400" alt="drawio_logo"/>
</div>

### check examples/ folder for output of style tree, syntax tree and code for the above diagram

## Fork information
This fork adds a Typescript generator, whoms syntax is slightly different and which can then be transpiled to javascript.  
The work on getters and setters ahs been stripped in the TypeScript part.

## Setup
````bash
# if pipenv is not installed :
pip install --user pipenv

# Install dependencies
python -m pipenv install

# Install missing deps & codecs
pip install BeautifulSoup4
pip install lxml

````

## Usage
Run the example :
````bash
# Compiles the diagram to both Java an Typescript code
python3 main.py
````

## State
The implementation is very minimal and not all UML Class Diagram syntax is parsed.  
Meanwhile, basic class structures are greatly generated and this script provides a quick starting point for implementing a diagram.  
Think semi-automatic.
