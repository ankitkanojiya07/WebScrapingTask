# Web Scraping Task

This project is a Python script designed to scrape data from the TINXSYS website for a given TIN number. The script extracts relevant information such as CST Number, Dealer Name, Dealer Address, State Name, PAN Number, Registration Date, Valid Upto, and Registration Status,and returns the extracted information in JSON format.

## Features

- Scrapes data using XPath and Python libraries.
- Implements Object-Oriented Programming (OOP) concepts.
- Handles CAPTCHA manually by prompting the user to enter the CAPTCHA value.
- Returns the extracted data in a structured JSON format.

## Requirements

- Python 3.x
- `requests` library
- `lxml` library
- `Pillow` library

## Installation
Install the required Python libraries using pip:

    ```sh
    pip install requests lxml Pillow
    ```

## Usage

1. **Set the TIN number**: In the script, set the `tin_number` variable to the desired TIN number.
2. **Run the script**: Execute the script in your Python environment.

    ```sh
    python index.py
    ```

3. **Enter the CAPTCHA**: The script will display the CAPTCHA image. Manually enter the CAPTCHA value when prompted.
4. **View the output**: The script will scrape the required data and output it in JSON format.

## Example

Here is an example of how to run the script and the expected output:

### Input

Set the `tin_number` variable in the script:

```python
tin_number = "09137500718"
