#!/bin/bash

function main() {
    cd "$(dirname "$0")"
    if [[ ! -d "./venv" ]]; then
        echo " [get_marc_21_records] Setting up virtual environment..."
        python3 -m venv venv
        echo " [get_marc_21_records] Virtual environment created."
    fi

    echo "[get_marc_21_records] Activating virtual environment..."
    source venv/bin/activate

    if are_requirements_satisfied; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    fi

    echo "[get_marc_21_records] Parsing MARC21XML data..."
    python get_marc21_records.py "$@"

    echo "[get_marc_21_records] Deactivating virtual environment..."
    deactivate
}

function are_requirements_satisfied() {
    while read requirement; do
        if pip show $requirement > /dev/null 2>&1; then
            return 1
        fi
    done < requirements.txt
    return 0
}

main "$@"
