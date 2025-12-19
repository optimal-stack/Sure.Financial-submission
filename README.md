# 💳 Multi-Bank Credit Card Statement Parser

A robust, modular Python tool designed to automate the extraction of key financial data from credit card statements. Built with a **Strategy Design Pattern**, it automatically detects the bank provider and dispatches the PDF to the appropriate parser to extract structured data.

## 🚀 Features

* **Auto-Detection:** Automatically identifies the bank issuer (Chase, HDFC, Amex, SBI, Citi) from the raw PDF text.
* **Modular Architecture:** Uses an extensible class-based structure, making it easy to add support for new banks without breaking existing logic.
* **Key Data Extraction:** Parses critical fields including:
    * Payment Due Date & Billing Cycle
    * Total Balance / Amount Due
    * Card Variant & Last 4 Digits
    * Transaction Summaries
* **Layout Preservation:** Utilizes `pdfplumber` to maintain visual layout accuracy for reliable table parsing.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Core Library:** `pdfplumber` (Superior table extraction compared to PyPDF2)
* **Logic:** Regular Expressions (Regex) for pattern matching

## 📂 Project Structure

```text
├── sure-financials.py       # Main script (Router & Parser Logic)
├── requirements.txt         # Dependencies
├── README.md                # Documentation
└── statements/              # Folder for input PDFs
    ├── chase_statement.pdf
    └── hdfc_statement.pdf

Architecture
This project implements the Strategy Pattern. The BaseStatementParser defines the interface, while specific bank classes (e.g., ChaseParser, HDFCParser) implement the unique extraction logic for their respective formats.

Installation
Clone the repository:
git clone [https://github.com/yourusername/statement-parser.git](https://github.com/yourusername/statement-parser.git)
cd statement-parser
Install dependencies:
pip install pdfplumber


Usage
Place your PDF statement in the project directory.

Update the filename variable in the if __name__ == "__main__": block of sure-financials.py.

Run the script: python sure-financials.py



Example Output
The parser returns a clean Python dictionary ready for JSON serialization or database entry.

1. Chase Bank Example
Input: chase_statement.pdf

{
  "bank_name": "Chase Bank",
  "card_variant": "Chase Credit Card",
  "card_last_4": "1415",
  "billing_cycle": "11/27/21-12/26/21",
  "payment_due_date": "01/23/22",
  "total_balance": "1,258.56",
  "transaction_info": "Total Purchases: $1,258.56"
}

2. HDFC Bank Example
Input: hdfc_statement.pdf
{
  "bank_name": "HDFC Bank",
  "card_variant": "HDFC Credit Card",
  "card_last_4": "3458",
  "billing_cycle": "Ends on 12/03/2023",
  "payment_due_date": "01/04/2023",
  "total_balance": "22,935.00",
  "transaction_info": "Summary not detected"
}
