def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Assumes code has exactly two words: department and number.
    Handles None, empty strings, extra/fewer parts, and non-string inputs safely.
    """
    if not code or not isinstance(code, str):
        return ""
    parts = code.strip().split()
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0].upper()
    return parts[0].upper() + "".join(parts[1:])


def total_credits(text):
    """
    Adds up comma-separated course credits.
    Assumes every value is a whole number.
    Handles None, empty strings, non-numeric values, and malformed inputs safely.
    """
    if not text or not isinstance(text, str):
        return 0
    total = 0
    for credit in text.split(','):
        cleaned = credit.strip()
        if cleaned:
            try:
                total += int(cleaned)
            except (ValueError, TypeError):
                continue
    return total


def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Assumes all three fields are present.
    Handles None, empty strings, missing fields, and extra fields safely.
    """
    default_record = {"srn": "", "name": "", "status": ""}
    if not line or not isinstance(line, str):
        return default_record
    parts = line.split('|')
    srn = parts[0].strip().upper() if len(parts) > 0 else ""
    name = parts[1].strip() if len(parts) > 1 else ""
    status = parts[2].strip().lower() if len(parts) > 2 else ""
    return {"srn": srn, "name": name, "status": status}


def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    print("Formatted course code:", format_course_code(value))

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    print("Total credits:", total_credits(value))

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    print("Student record:", parse_student_record(value))


if __name__ == "__main__":
    main()
