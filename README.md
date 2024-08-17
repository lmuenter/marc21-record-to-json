# marc21-record-to-json
A tool for record extraction and JSON serialization for MARC21 XML data.

# Installation

## Prerequisits
- This tool requires **Python3.7+**. If you do not have Python on your system, follow the installation instructions of Python's official [website](https://www.python.org/).
- You should have git installed to clone this repo.

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

# Usage
- Run the commandline script using the python interpreter:
```
python /path/to/cloned/repo/get_marc21_records.py -f myfile.xml -o myjson.json
```
