# Multi-Bank Credit Card Statement Parser

A **robust, modular Python tool** that automates extraction of key financial data from credit card statements (PDFs). The system is built using the **Strategy Design Pattern**, enabling automatic bank detection and dispatching to the appropriate parser for reliable, structured data extraction.

---

## Key Features

* **Automatic Bank Detection**
  Identifies the issuing bank directly from raw PDF text.

* **Strategy Pattern Architecture**
  Clean, extensible design that allows adding new banks without modifying existing logic.

* **Critical Data Extraction**
  Extracts essential credit card statement details:

  * Payment Due Date
  * Billing Cycle
  * Total Balance / Amount Due
  * Card Variant & Last 4 Digits
  * Transaction Summary

* **Layout-Preserving PDF Parsing**
  Uses `pdfplumber` for accurate text and table extraction while preserving layout structure.

---

## 🏦 Supported Banks

* Chase Bank
* HDFC Bank
* American Express (Amex)
* SBI Card
* Citi Bank

*(New banks can be added easily by implementing a new parser class.)*

---

## Tech Stack

* **Language:** Python 3.x
* **PDF Parsing:** `pdfplumber`
* **Pattern Matching:** Regular Expressions (Regex)
* **Architecture:** Strategy Design Pattern

---

## Project Structure

```bash
├── sure-financials.py       # Main script (Router & Parser Logic)
├── requirements.txt         # Project dependencies
├── README.md                # Documentation
├── chase_statement.pdf      # Sample Chase statement
└── hdfc_statement.pdf       # Sample HDFC statement
```

---

## Architecture Overview

This project follows the **Strategy Design Pattern**:

* `BaseStatementParser` defines a common interface for all bank parsers.
* Each bank-specific parser (e.g., `ChaseParser`, `HDFCParser`) implements its own extraction logic.
* A central router automatically detects the bank and invokes the correct parser.

This design ensures:

* High maintainability
* Easy extensibility
* Clean separation of concerns

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/statement-parser.git
cd statement-parser
```

### Install Dependencies

```bash
pip install pdfplumber
```

---

## Usage

1. Place your credit card statement PDF inside the project directory.
2. Open `sure-financials.py` and update the `filename` variable inside:

```python
if __name__ == "__main__":
    filename = "your_statement.pdf"
```

3. Run the parser:

```bash
python sure-financials.py
```

---

## Example Output

The parser returns a clean **Python dictionary**, ready for:

* JSON serialization
* Database insertion
* API responses

---

### Chase Bank Example

**Input:** `chase_statement.pdf`

```json
{
  "bank_name": "Chase Bank",
  "card_variant": "Chase Credit Card",
  "card_last_4": "1415",
  "billing_cycle": "11/27/21-12/26/21",
  "payment_due_date": "01/23/22",
  "total_balance": "1,258.56",
  "transaction_info": "Total Purchases: $1,258.56"
}
```

---

### HDFC Bank Example

**Input:** `hdfc_statement.pdf`

```json
{
  "bank_name": "HDFC Bank",
  "card_variant": "HDFC Credit Card",
  "card_last_4": "3458",
  "billing_cycle": "Ends on 12/03/2023",
  "payment_due_date": "01/04/2023",
  "total_balance": "22,935.00",
  "transaction_info": "Summary not detected"
}
```

---

## Future Enhancements

* Export output directly to JSON / CSV
* Database integration (PostgreSQL / MongoDB)
* CLI support for batch PDF processing
* OCR support for scanned statements

---

## License

This project is open-source and available under the **MIT License**.

---

## Contributing

Contributions are welcome! Feel free to:

* Add support for new banks
* Improve regex accuracy
* Optimize parsing performance

Submit a pull request or open an issue 🚀
