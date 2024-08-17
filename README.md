# marc21-record-to-json
A tool for record extraction and JSON serialization for MARC21 XML data.

# Installation and Usage

## Prerequisits
- This tool requires **Python3.7+**. If you do not have Python on your system, follow the installation instructions of Python's official [website](https://www.python.org/).
- You should have git installed to clone this repo.


## Installation
1. **Just Clone the repo:**
```
git clone "lmuenter/marc21-record-to-json"
```

## Usage
To run the program, you can simply use the included command line tools.

1. **Running under Windows:**
```
path\to\get_marc21_records.bat -f myfile.xml -o myoutput.json
```

2. **Running under Unix (incl. MacOS)**
```
path/to/get_marc21_records.sh -f myfile.xml -o myoutput.json
```

## Development Setup
1. **Clone the repo:**
```
git clone "lmuenter/marc21-record-to-json"
```
2. **Set up the virtual environment**
```
python -m venv venv
```
3. **Activate virtual environment**
- Under Windows:
```
venv\Scripts\activate
```
- Unix (incl. MacOS):
```
source venv/bin/activate
```
4. **Install Dependencies**
```
pip install -r requirements.txt
```
5. **Deactivate venv when done**
```
deactivate
```
6. **Run Unit Tests:**
```
pytest
```
