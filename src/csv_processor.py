# src/csv_processor.py
import csv
from encoder import generate_encoded_query_string

def validate_csv_format(input_csv, search_field_keys):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames

        if headers is None:
            raise ValueError("The CSV file is empty or does not contain headers.")

        headers_set = set(headers)
        if not headers_set & search_field_keys:
            raise ValueError("The CSV file is not in the proper format. It must contain at least one column matching the search fields.")
        
        return [row for row in reader]

def process_csv_and_add_encoded_query_string(input_csv, output_csv, log_csv, search_field_keys=None):
    processed_count = 0
    ignored_count = 0
    log_entries = []
    if(search_field_keys is None):
        search_field_keys = {
            "ex_limit", "questionified", "specific_ids", "textbook_chapters", 
            "textbook_isbns", "textbook_pages", "exclude_isbns", "verified", 
            "question_batches", "question_subjects", "question_owners"
        }
    
    data = validate_csv_format(input_csv, search_field_keys)
    
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=list(data[0].keys()) + ['generated_encoded_query_string'])
        writer.writeheader()

        for i, row in enumerate(data, start=1):
            if row.get('generated_encoded_query_string'):
                ignored_count += 1
                log_entries.append({
                    "row_number": i,  # Manually track the row number
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
    

    print(f"Processed CSV saved to {output_csv}")
    print(f"Total rows processed: {processed_count}")
    print(f"Total rows ignored: {ignored_count}")
    
    return processed_count, ignored_count


def convert_csv(input_csv, output_csv, log_csv):
    search_field_keys = {
        "ex_limit", "questionified", "specific_ids", "textbook_chapters", 
        "textbook_isbns", "textbook_pages", "exclude_isbns", "verified", 
        "question_batches", "question_subjects", "question_owners"
    }

    processed_count, ignored_count = process_csv_and_add_encoded_query_string(
        input_csv, output_csv, log_csv, search_field_keys)

    print(f"Rows processed: {processed_count}")
    print(f"Rows ignored: {ignored_count}")
    print(f"Output CSV: {output_csv}")
    print(f"Log CSV: {log_csv}")

# This allows the script to be run directly from the command line
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert a CSV file by adding encoded query strings.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("log_csv", help="Path to the log CSV file")

    args = parser.parse_args()

    convert_csv(args.input_csv, args.output_csv, args.log_csv)