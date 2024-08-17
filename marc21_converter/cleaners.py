def clean_record(processed_record, mappings):
    cleaned_record = {}
    for key, value in processed_record.items():
        if key in mappings:
            cleaned_value = mappings[key].get(value, value)
            cleaned_record[key] = cleaned_value
        else:
            cleaned_record[key] = value
    return cleaned_record

