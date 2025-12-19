import pdfplumber
import re
import logging
from typing import Dict

# Suppress internal PDF warnings (like "invalid float value")
logging.getLogger("pdfminer").setLevel(logging.ERROR)


# --- 1. BASE PARSER (The Interface) ---
class BaseStatementParser:
    def __init__(self, text_content):
        self.text = text_content

    def parse(self) -> Dict[str, str]:
        """Orchestrates the extraction of the 6 requested fields."""
        return {
            "bank_name": self.get_bank_name(),
            "card_variant": self.extract_card_variant(),
            "card_last_4": self.extract_card_last_4(),
            "billing_cycle": self.extract_billing_cycle(),
            "payment_due_date": self.extract_due_date(),
            "total_balance": self.extract_total_balance(),
            "transaction_info": self.extract_transaction_summary()
        }

    # Abstract methods - defaults to "Not Found" if not implemented
    def get_bank_name(self): return "Unknown Bank"

    def extract_card_variant(self): return "Standard Credit Card"

    def extract_card_last_4(self): return None

    def extract_billing_cycle(self): return None

    def extract_due_date(self): return None

    def extract_total_balance(self): return None

    def extract_transaction_summary(self): return "Summary not detected"


# --- 2. HDFC PARSER ---
class HDFCParser(BaseStatementParser):
    def get_bank_name(self):
        return "HDFC Bank"

    def extract_card_variant(self):
        # Look for common HDFC card names
        keywords = ["Infinia", "Regalia", "Millennia", "MoneyBack", "Diners Club", "Business MoneyBack"]
        for card in keywords:
            if card.upper() in self.text.upper():
                return f"HDFC {card}"
        return "HDFC Credit Card"

    def extract_card_last_4(self):
        # HDFC often masks as XXXXXXXX1234
        match = re.search(r"[X\d]{8,12}(\d{4})", self.text)
        return match.group(1) if match else None

    def extract_billing_cycle(self):
        # Statement Date often implies the cycle end
        match = re.search(r"Statement\s+Date\s*[:\-\s]*(\d{2}/\d{2}/\d{4})", self.text, re.IGNORECASE)
        return f"Ends on {match.group(1)}" if match else None

    def extract_due_date(self):
        match = re.search(r"Payment\s+Due\s+Date\s*[:\-\s]*(\d{2}/\d{2}/\d{4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_total_balance(self):
        match = re.search(r"Total\s+Amount\s+Due\s*[:\-\s]*.*?([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_transaction_summary(self):
        # Look for "Debits" or "Purchases" count/amount
        match = re.search(r"Debits\s+([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return f"Total Debits: {match.group(1)}" if match else None


# --- 3. CHASE PARSER ---
class ChaseParser(BaseStatementParser):
    def get_bank_name(self):
        return "Chase Bank"

    def extract_card_variant(self):
        keywords = ["Sapphire", "Freedom", "Ink", "Slate", "Amazon"]
        for card in keywords:
            if card.upper() in self.text.upper():
                return f"Chase {card}"
        return "Chase Credit Card"

    def extract_card_last_4(self):
        # "Account ending in 1234"
        match = re.search(r"(?:Account|ending)\s+(?:Number)?\s*(?:in|:)?\s*(\d{4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_billing_cycle(self):
        # "Opening/Closing Date 12/24/21 - 01/23/22"
        match = re.search(r"Opening/Closing\s+Date\s+(\d{2}/\d{2}/\d{2,4}\s*-\s*\d{2}/\d{2}/\d{2,4})", self.text,
                          re.IGNORECASE)
        return match.group(1) if match else None

    def extract_due_date(self):
        match = re.search(r"Payment\s+Due\s+Date\s+(\d{1,2}/\d{1,2}/\d{2,4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_total_balance(self):
        match = re.search(r"New\s+Balance\s.*?\$([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_transaction_summary(self):
        # "Purchases $1,200.50"
        match = re.search(r"Purchases\s+(?:and Adjustments)?\s*\$([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return f"Total Purchases: ${match.group(1)}" if match else None


# --- 4. SBI PARSER ---
class SBIParser(BaseStatementParser):
    def get_bank_name(self):
        return "SBI Card"

    def extract_card_variant(self):
        keywords = ["Elite", "Prime", "SimplyClick", "SimplySave", "Aurum"]
        for card in keywords:
            if card.upper() in self.text.upper():
                return f"SBI {card}"
        return "SBI Credit Card"

    def extract_card_last_4(self):
        # SBI: "Card Number: XXXX XXXX XXXX 1234"
        match = re.search(r"XXXX\s+(\d{4})", self.text)
        return match.group(1) if match else None

    def extract_billing_cycle(self):
        match = re.search(r"Statement\s+Date\s*[:\-\s]*(\d{2}/\d{2}/\d{4})", self.text, re.IGNORECASE)
        return f"Statement generated on {match.group(1)}" if match else None

    def extract_due_date(self):
        match = re.search(r"Payment\s+Due\s+Date\s*[:\-\s]*(\d{2}/\d{2}/\d{2,4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_total_balance(self):
        match = re.search(r"Total\s+Amount\s+Due\s*[:\-\s]*.*?([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_transaction_summary(self):
        match = re.search(r"Debits\s+([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return f"Total Debits: {match.group(1)}" if match else None


# --- 5. AMEX PARSER ---
class AmexParser(BaseStatementParser):
    def get_bank_name(self):
        return "American Express"

    def extract_card_variant(self):
        keywords = ["Platinum", "Gold", "Green", "EveryDay", "Blue Cash"]
        for card in keywords:
            if card.upper() in self.text.upper():
                return f"Amex {card}"
        return "Amex Card"

    def extract_card_last_4(self):
        # Amex uses 5 digits usually, but lets look for "ending in 12345"
        match = re.search(r"ending\s+in\s+(\d{4,5})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_billing_cycle(self):
        match = re.search(r"Closing\s+Date\s+([A-Za-z]{3}\s\d{1,2},?\s\d{4})", self.text, re.IGNORECASE)
        return f"Closing Date: {match.group(1)}" if match else None

    def extract_due_date(self):
        match = re.search(r"Payment\s+Due\s+Date\s+([A-Za-z]{3}\s\d{1,2},?\s\d{4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_total_balance(self):
        match = re.search(r"New\s+Balance\s.*?\$([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_transaction_summary(self):
        match = re.search(r"New\s+charges\s.*?\$([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return f"New Charges: ${match.group(1)}" if match else None


# --- 6. CITI PARSER ---
class CitiParser(BaseStatementParser):
    def get_bank_name(self):
        return "Citibank"

    def extract_card_variant(self):
        keywords = ["Premier", "Prestige", "Double Cash", "Rewards", "Simplicity"]
        for card in keywords:
            if card.upper() in self.text.upper():
                return f"Citi {card}"
        return "Citi Card"

    def extract_card_last_4(self):
        match = re.search(r"(?:Account|Card)\s+.*(\d{4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_billing_cycle(self):
        match = re.search(r"Statement\s+Date\s+(\d{2}/\d{2}/\d{4})", self.text, re.IGNORECASE)
        return f"Statement Date: {match.group(1)}" if match else None

    def extract_due_date(self):
        match = re.search(r"Payment\s+Due\s+Date\s+(\d{2}/\d{2}/\d{4})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_total_balance(self):
        match = re.search(r"New\s+Balance\s.*?\$([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_transaction_summary(self):
        match = re.search(r"Purchases\s.*?\$([\d,]+\.\d{2})", self.text, re.IGNORECASE)
        return f"Purchases: ${match.group(1)}" if match else None


# --- MAIN ROUTER ---
def parse_credit_card_statement(pdf_path: str):
    try:
        text_content = ""
        with pdfplumber.open(pdf_path) as pdf:
            # Check first 2 pages
            for i in range(min(2, len(pdf.pages))):
                text_content += pdf.pages[i].extract_text() + "\n"

        # Router Logic
        if "HDFC" in text_content or "H.D.F.C" in text_content:
            parser = HDFCParser(text_content)
        elif "CHASE" in text_content.upper() or "JPMORGAN" in text_content.upper():
            parser = ChaseParser(text_content)
        elif "SBI Card" in text_content or "State Bank of India" in text_content:
            parser = SBIParser(text_content)
        elif "American Express" in text_content or "AMEX" in text_content:
            parser = AmexParser(text_content)
        elif "Citi" in text_content or "Citibank" in text_content:
            parser = CitiParser(text_content)
        else:
            return {"error": "Bank not detected. Supported: HDFC, Chase, SBI, Amex, Citi"}

        return parser.parse()

    except Exception as e:
        return {"error": f"Error reading PDF: {str(e)}"}


# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Update this to your file name
    filename = "hdfc_bank.pdf"

    print(f"Processing file: {filename}...\n")

    # 2. Run
    result = parse_credit_card_statement(filename)

    # 3. Print Results
    print("--- PARSED DATA ---")
    if "error" in result:
        print(f"FAILED: {result['error']}")
    else:
        for key, value in result.items():
            print(f"{key}: {value}")