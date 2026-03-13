import re
import pandas as pd


COUNTRY_MAP = {
    "polska": "Poland",
    "poland": "Poland",
    "germany": "Germany",
    "deutschland": "Germany",
    "spain": "Spain",
    "portugal": "Portugal",
    "netherlands": "Netherlands",
    "france": "France",
    "italy": "Italy"
}


def capitalize_names(df):

    for col in df.columns:

        if "name" in col.lower():
            df[col] = df[col].astype(str).str.title()

    return df


def lowercase_emails(df):

    for col in df.columns:

        if "email" in col.lower():
            df[col] = df[col].astype(str).str.lower()

    return df


def normalize_phone_numbers(df):

    for col in df.columns:

        if "phone" in col.lower():

            df[col] = df[col].astype(str).apply(
                lambda x: re.sub(r"[^\d+]", "", x)
            )

    return df


def standardize_country_names(df):

    for col in df.columns:

        if "country" in col.lower():

            df[col] = df[col].astype(str).str.lower().map(COUNTRY_MAP).fillna(df[col])

    return df


def standardize_dates(df):

    for col in df.columns:

        if "date" in col.lower():

            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

    return df