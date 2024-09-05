from utils import process_csv_and_add_encoded_query_string

def main():
    input_csv = "input.csv"  # Replace with your input CSV file path
    output_csv = "output.csv"  # Replace with your desired output CSV file path
    log_csv = "log.csv"  # Replace with your desired log CSV file path
    
    process_csv_and_add_encoded_query_string(input_csv, output_csv, log_csv)

if __name__ == "__main__":
    main()