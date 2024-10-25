# Draw.io Code Generator

<div>
    <img src="./github_assets/drawio.jpg" width="125" height="125" alt="drawio_logo">
    <img src="./github_assets/plus.png" width="125" height="125" alt="plus_sign"/>
    <img src="./github_assets/python.png" width="125" height="125" alt="python_logo">
    <img src="./github_assets/equal.png" width="125" height="125" alt="equal_sign">
    <img src="./github_assets/code.png" width="125" height="125" alt="code_logo">
</div>

### Generate source code in various programming languages from a [draw.io](https://draw.io/) UML class diagram

Supported target languages are: Java, C#, C++, Python, TypeScript, PHP and SQL.

<div>
    <img src="./github_assets/simple_class_diagram.jpg" width="400" height="400" alt="class_diagram"/>
</div>

## About this fork

* This is a fork of the https://github.com/Daandelange/DrawioCodeGenerator repository. 
* It adds a [wxPython](https://wxpython.org/) based GUI for an enhanced user experience.
* The original Java and TypeScript code generators were extended with new functionalities. 
* New code generators were added for C#, C++, PHP, Python and SQL with the same level of functionalities than the initial ones.
* The generated xml and json documents are no more stored in files but displayed on the GUI.
* Abstract classes are nomore identified by a name in italics. They should simply be annotated as **\<\<abstract\>\>** just like interfaces with **\<\<interface\>\>**.
* The **\<\<enum\>\>** annotation indicates that a class is in fact an enumeration.
* Properties can have a default value if their definition in the diagram ends with a _" = default_value"_, which is very practical for enum members.
* Code generators can produce a **package** or **namespace** directive if required. They will also automatically generate an **import** (or **using** or **#include** or **require_once**) directive for any symbol that the class being generated depends on.
* Users can define additional module and/or symbols to import in their class headers through a configuration dialog.
* If required code generators can also produce other members like accessors (encapsulated properties or getter/setter pairs), a default constructor, a fully parameterized constructor and overrides for the _equals_, _hashCode_ and _toString_ methods in languages that support those features.
* The SQL code generator doesn't conform to any particular dialect. It just tries to be at least compatible with MySQL and SQL Server in general. For the moment it doesn't define any key in the generated code. Allowing the user to select a SQL dialect may be added in the future.
* The program recognizes a set of pseudo data types that can be mapped to equivalent data types in each of the target languages. They are listed in the table bellow:

|Pseudo-type|Java equivalent|C# equivalent|C++ equivalent|TypeScript equivalent|SQL equivalent|
|-|-|-|-|-|-|
|boolean, bool|boolean|bool|bool|boolean|bit|
|char|char|char|char|string|char(1)|
|wchar|char|char|wchar_t|string|nchar(1)|
|sbyte, int8|byte|sbyte|signed char|number|tinyint|
|byte, uint8|byte|byte|unsigned char|number|tinyint|
|short, int16|short|short|short|number|smallint|
|ushort, uint16|short|ushort|unsigned short|number|smallint|
|integer, int, int32|int|int|int|number|int|
|uint, uint32|int|uint|unsigned int|number|int|
|long, int64|long|long|long long|number|bigint|
|ulong, uint64|long|ulong|unsigned long long|number|bigint|
|foat, single|float|float|float|number|float(24)|
|double|double|double|double|number|float(53)|
|bigint|BigInteger|BigInteger|_N/A_|bigint|decimal(30, 0)|
|decimal|BigDecimal|decimal|_N/A_|number|decimal(30, 10)|
|string|String|string|std::string|string|varchar(2000)|
|wstring|String|string|std::wstring|string|nvarchar(2000)|
|date|LocalDate|DateTime|time_t|Date|date|
|time|LocalTime|DateTime|time_t|Date|time|
|datetime, timestamp|LocalDateTime|DateTime|time_t|Date|datetime|

## Setup

Before all make sure that you have a python interpreter and a suitable development environment installed on your developper machine.
Then open a command prompt on the project's root folder and run the following commands. 

On Windows:

```shell
# create a virtual environment
python -m venv venv

# activate the virtual environment
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

On Unix based platforms:

```shell
# create a virtual environment
python3 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install the packages required to build the wxPython wheel
# works on ubuntu 24.04, you should adapt to your distribution
chmod +x ./install-packages.sh 
sudo ./install-packages.sh

# install dependencies
# building wxPython may take some time!
pip3 install -r requirements.txt
```

## Usage

To launch the program use the following command.

On Windows:

```shell
# uncomment to activate the virtual environment if not yet done
# venv\Scripts\activate

# invoke python interpreter
python main.py
```

On Unix based platforms:

```shell
# uncomment to activate the virtual environment if not yet done
# source venv/bin/activate

# invoke python interpreter
python3 main.py
```

## State

A continuous effort is made for the program to become compatible with the largest variety of class diagrams but at this stage
some may not be correctly parsed, especially those that feature special constructs like data tables.
More improvements are still to come.

#### Voilà, that's it!!
