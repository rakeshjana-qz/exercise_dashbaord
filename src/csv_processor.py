# src/csv_processor.py
import csv

def validate_csv_format(input_csv, search_field_keys):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = set(reader.fieldnames)

        if not headers & search_field_keys:
            raise ValueError("The CSV file is not in the proper format. It must contain at least one column matching the search fields.")
        
        return [row for row in reader]

def process_csv_and_add_encoded_query_string(input_csv, output_csv, log_csv, search_field_keys):
    processed_count = 0
    ignored_count = 0
    log_entries = []

    data = validate_csv_format(input_csv, search_field_keys)

    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=data[0].keys() + ['generated_encoded_query_string'])
        writer.writeheader()

        for row in data:
            if row.get('generated_encoded_query_string'):
                ignored_count += 1
                log_entries.append({
                    "row_number": reader.line_num,
                    "reason": "Existing generated_encoded_query_string"
                })
                continue

            # Generate encoded query string logic (use your existing logic)
            search_fields = {k: row.get(k, "") for k in search_field_keys}
            encoded_query_string = generate_encoded_query_string(search_fields)
            row['generated_encoded_query_string'] = encoded_query_string

            writer.writerow(row)
            processed_count += 1

    with open(log_csv, mode='w', newline='', encoding='utf-8') as logfile:
        log_fieldnames = ["row_number", "reason"]
        log_writer = csv.DictWriter(logfile, fieldnames=log_fieldnames)
        log_writer.writeheader()
        log_writer.writerows(log_entries)

    return processed_count, ignored_count, data  # Return the data for UI display