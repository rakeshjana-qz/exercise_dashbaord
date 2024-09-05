# Exercise Dashboard Link Generator

This project generates encoded query strings based on input from a CSV file and appends these strings to the CSV file. It includes both a graphical user interface (GUI) and a command-line interface (CLI) for flexibility.

## Project Setup

### Prerequisites

- Python 3.7+
- Pipenv

### Installation

1. Clone the repository:

    ```bash
    gh repo clone rakeshjana-qz/exercise_dashbaord
    cd exercise_dashbaord
    ```

2. Install dependencies:

    ```bash
    pipenv install
    ```

3. Create a `.env` file in the project root:

    ```bash
    touch .env
    ```

4. Add the following to the `.env` file:

    ```
    EXERCISE_DASH_KEY=YourSecretKeyHere
    ```

### Usage

For detailed instructions on how to build and run the application as an executable for Windows, Linux, and macOS, please refer to the [APP_BUILDER.md](./APP_BUILDER.md) file.

### Example

#### Example Input CSV

Suppose your input CSV contains the following:

| ex_limit | questionified | specific_ids | textbook_chapters | textbook_isbns      | textbook_pages | exclude_isbns | verified | question_batches | question_subjects | question_owners |
|----------|---------------|--------------|-------------------|---------------------|----------------|---------------|----------|------------------|-------------------|-----------------|
| 5        | true          | 123          | 1,2,3             | 9783161484100    | 10-20          |               | false    | batch1           | math              | owner1          |

#### Example Output CSV

After running the script or using the GUI, the output CSV will look like this:

| ex_limit | questionified | specific_ids | textbook_chapters | textbook_isbns      | textbook_pages | exclude_isbns | verified | question_batches | question_subjects | question_owners | generated_encoded_query_string |
|----------|---------------|--------------|-------------------|---------------------|----------------|---------------|----------|------------------|-------------------|-----------------|---------------------------------|
| 5        | true          | 123          | 1,2,3             | 9783161484100    | 10-20          |               | false    | batch1           | math              | owner1          | YourEncodedStringHere           |

### Testing

Unit tests have been provided to ensure the functionality of the application.

1. To run the tests, use the following command:

    ```bash
    python -m unittest discover -s tests
    ```

2. This will run all tests located in the `tests` directory and ensure that the application is working as expected.

### Project Structure

- **`src/`**: Contains the main application code.
  - **`main.py`**: The entry point for the GUI application.
  - **`csv_processor.py`**: Contains the logic for processing CSV files, including the CLI interface.
  - **`encoder.py`**: Handles encoding and decoding of query strings.
- **`tests/`**: Contains unit tests for the application.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.