# Exercise Dashboard Link Generator

This project generates encoded query strings based on input from a CSV file and appends these strings to the CSV file.

## Project Setup

### Prerequisites

- Python 3.7+
- Pipenv

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/csv_link_generator.git
    cd csv_link_generator
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

1. Place your input CSV file in the project directory.

2. Run the script:

    ```bash
    pipenv run python src/main.py
    ```

3. The output CSV file will be saved with the encoded query strings appended.

### Example

Suppose your input CSV contains the following:

| ex_limit | questionified | specific_ids | textbook_chapters | textbook_isbns      | textbook_pages | exclude_isbns | verified | question_batches | question_subjects | question_owners |
|----------|---------------|--------------|-------------------|---------------------|----------------|---------------|----------|------------------|-------------------|-----------------|
| 5        | true          | 123          | 1,2,3             | 978-3-16-148410-0    | 10-20          |               | false    | batch1           | math              | owner1          |

After running the script, the output CSV will look like this:

| ex_limit | questionified | specific_ids | textbook_chapters | textbook_isbns      | textbook_pages | exclude_isbns | verified | question_batches | question_subjects | question_owners | generated_encoded_query_string |
|----------|---------------|--------------|-------------------|---------------------|----------------|---------------|----------|------------------|-------------------|-----------------|---------------------------------|
| 5        | true          | 123          | 1,2,3             | 978-3-16-148410-0    | 10-20          |               | false    | batch1           | math              | owner1          | YourEncodedStringHere           |
```

 