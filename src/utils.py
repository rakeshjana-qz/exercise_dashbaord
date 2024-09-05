# This is deprecated in favor of the GUI application
# Use ui.py and csv_processor.py to implement the GUI application
# TODO: Remove this file after implementing the GUI application
import os
import urllib.parse
import csv
from dotenv import load_dotenv

load_dotenv()

EXERCISE_DASH_KEY = os.getenv("EXERCISE_DASH_KEY")

def encode_url(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr(((ord(clear[i]) + ord(key_c)) % 126))
        enc.append(enc_c)
    return urllib.parse.quote("".join(enc), safe="")

def decode_url(key, enc):
    dec = []
    enc = urllib.parse.unquote(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((126 + ord(enc[i]) - ord(key_c)) % 126)
        dec.append(dec_c)
    return "".join(dec)

def generate_encoded_query_string(search_fields):
    search_fields_str = ""
    for k, v in search_fields.items():
        if v:
            search_fields_str += "&%s=%s" % (k, str(v).replace("&", "%26"))
    encoded_query_string_contributor = encode_url(EXERCISE_DASH_KEY, search_fields_str)
    return encoded_query_string_contributor

def process_csv_and_add_encoded_query_string(input_csv, output_csv, log_csv):
    processed_count = 0
    ignored_count = 0
    log_entries = []

    search_field_keys = {
        "ex_limit", "questionified", "specific_ids", "textbook_chapters", 
        "textbook_isbns", "textbook_pages", "exclude_isbns", "verified", 
        "question_batches", "question_subjects", "question_owners"
    }

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = set(reader.fieldnames)

        # Check if there's at least one matching search field key
        if not headers & search_field_keys:
            raise ValueError("The CSV file is not in the proper format. It must contain at least one column matching the search fields.")

        fieldnames = reader.fieldnames + ['generated_encoded_query_string']

        with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Check if the 'generated_encoded_query_string' column exists and is non-empty
                if 'generated_encoded_query_string' in row and row['generated_encoded_query_string']:
                    ignored_count += 1
                    log_entries.append({
                        "row_number": reader.line_num,
                        "reason": "Existing generated_encoded_query_string"
                    })
                    continue

                # Generate the encoded query string
                search_fields = {
                    "ex_limit": row.get("ex_limit", ""),
                    "questionified": row.get("questionified", ""),
                    "specific_ids": row.get("specific_ids", ""),
                    "textbook_chapters": row.get("textbook_chapters", ""),
                    "textbook_isbns": row.get("textbook_isbns", ""),
                    "textbook_pages": row.get("textbook_pages", ""),
                    "exclude_isbns": row.get("exclude_isbns", ""),
                    "verified": row.get("verified", ""),
                    "question_batches": row.get("question_batches", ""),
                    "question_subjects": row.get("question_subjects", ""),
                    "question_owners": row.get("question_owners", "")
                }

                if not any(search_fields.values()):
                    ignored_count += 1
                    log_entries.append({
                        "row_number": reader.line_num,
                        "reason": "Empty search fields"
                    })
                    continue

                encoded_query_string = generate_encoded_query_string(search_fields)
                row['generated_encoded_query_string'] = encoded_query_string
                writer.writerow(row)
                processed_count += 1

    # Log the results
    with open(log_csv, mode='w', newline='', encoding='utf-8') as logfile:
        log_fieldnames = ["row_number", "reason"]
        log_writer = csv.DictWriter(logfile, fieldnames=log_fieldnames)
        log_writer.writeheader()
        log_writer.writerows(log_entries)

    print(f"Processed CSV saved to {output_csv}")
    print(f"Total rows processed: {processed_count}")
    print(f"Total rows ignored: {ignored_count}")
    return processed_count, ignored_count