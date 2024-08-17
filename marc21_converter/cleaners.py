import datetime
import locale
import copy

from marc21_converter._constants import LANGUAGE_TO_LOCALE


def clean_record(processed_record, mappings):
    mapped_clean_data = apply_data_mapping(processed_record, mappings)

    # set the locale to the given language
    language = mapped_clean_data.get("language", "eng")
    locale_code = LANGUAGE_TO_LOCALE.get(language)

    if locale_code:
        try:
            locale.setlocale(locale.LC_TIME, locale_code)
        except locale.Error as e:
            print(f"Couldn't set locale for {locale_code}: {e}")
            return mapped_clean_data
    
    clean_data = clean_dates(copy.deepcopy(mapped_clean_data))

    # reset locale
    locale.setlocale(locale.LC_TIME, "")

    return clean_data


def apply_data_mapping(processed_record, mappings):
    def clean_value(key, value, mappings):
        if isinstance(value, dict):
            return {k: clean_value(k, v, mappings) for k, v in value.items()}
        elif isinstance(value, list):
            return [clean_value(key, v, mappings) for v in value]
        else:
            return mappings.get(key, {}).get(value, value)

    def recursive_clean(data, mappings):
        if isinstance(data, dict):
            return {k: recursive_clean(clean_value(k, v, mappings), mappings) for k, v in data.items()}
        elif isinstance(data, list):
            return [recursive_clean(item, mappings) for item in data]
        else:
            return data

    return recursive_clean(processed_record, mappings)



def clean_dates(data):
    dates = data.get("publication_date")
    if not dates or len(dates) == 1:
        return data
    try:
        month_number = datetime.datetime.strptime(dates[1], "%B").month
        dates[1] = str(month_number)
    except ValueError as e:
        print(f"An error occurred during date conversion: {e}")
    
    return data