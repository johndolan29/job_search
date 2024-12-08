import yaml
import re


def load_config(filename):
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def extract_salary(description):
    if isinstance(description, str):
        salary = re.findall(r"£\d{1,3}(?:,\d{3})*(?:\d{3})?", description)
        if salary:
            return salary[0]
    return None


def extract_days_per_week(description):
    # Ensure input is a string
    if not isinstance(description, str):
        description = ""

    # Replace written numbers with digits
    description = re.sub(r"\btwo\b", "2", description, flags=re.IGNORECASE)
    description = re.sub(r"\bthree\b", "3", description, flags=re.IGNORECASE)
    description = re.sub(r"\bfour\b", "4", description, flags=re.IGNORECASE)
    description = re.sub(r"\bfive\b", "5", description, flags=re.IGNORECASE)
    description = re.sub(r"\bsix\b", "6", description, flags=re.IGNORECASE)
    description = re.sub(r"\bseven\b", "7", description, flags=re.IGNORECASE)
    description = re.sub(r"\beight\b", "8", description, flags=re.IGNORECASE)
    description = re.sub(r"\bnine\b", "9", description, flags=re.IGNORECASE)
    description = re.sub(r"\bten\b", "10", description, flags=re.IGNORECASE)

    # Match patterns for "X days per week" or "X day a week"
    matches = re.findall(
        r"(\d{1,2})\s*days\s*(?:per|a)\s*week|(\d{1,2})\s*day\s*(?:per|a)\s*week",
        description,
    )

    # Flatten the matches to extract the number (ignore empty groups)
    days = [int(day) for match in matches for day in match if day]
    # Return the first match if found, or None otherwise
    return days[0] if days else None


def convert_salary_to_float(salary):
    if salary is None or isinstance(salary, float):
        if float(salary) < 1000:
            salary = float(salary) * 1000
        return salary

    if isinstance(salary, str):
        # Remove any non-numeric characters except for the decimal point
        salary = "".join(c for c in salary if c.isdigit() or c == ".")

        if "-" in salary:
            salary = salary.split("-")[1]

    if float(salary) < 1000:
        salary = float(salary) * 1000
    if type(salary) == str:
        salary = float(salary)
    return float(salary)


def make_clickable(val):
    if val is None or not isinstance(val, str) or not val.startswith("http"):
        return val
    return f'<a href="{val}" target="_blank">Click</a>'


def truncate_string(val):
    if val is None or not isinstance(val, str):
        return val
    return val[:30] + "..." if len(val) > 30 else val
