import pandas as pd
from validators import validate_email_column
from normalizers import *


def clean_dataframe(df, options):

    original_rows = len(df)

    duplicates_removed = 0
    empty_rows_removed = 0

    if options["trim_spaces"]:
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    if options["remove_duplicates"]:
        before = len(df)
        df = df.drop_duplicates()
        duplicates_removed = before - len(df)

    if options["remove_empty_rows"]:
        before = len(df)
        df = df.dropna(how="all")
        empty_rows_removed = before - len(df)

    if options["remove_empty_columns"]:
        df = df.dropna(axis=1, how="all")

    if options["capitalize_names"]:
        df = capitalize_names(df)

    if options["lowercase_emails"]:
        df = lowercase_emails(df)

    if options["normalize_phones"]:
        df = normalize_phone_numbers(df)

    if options["standardize_countries"]:
        df = standardize_country_names(df)

    if options["standardize_dates"]:
        df = standardize_dates(df)

    invalid_emails = 0

    if options["validate_emails"]:
        df, invalid_emails = validate_email_column(df)

    report = f"""
Rows processed: {original_rows}
Duplicates removed: {duplicates_removed}
Empty rows removed: {empty_rows_removed}
Invalid emails: {invalid_emails}
"""

    return df, report