import re


EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'


def validate_email(email):

    if not isinstance(email, str):
        return False

    return re.match(EMAIL_REGEX, email) is not None


def validate_email_column(df):

    invalid_count = 0

    for col in df.columns:

        if "email" in col.lower():

            status = []

            for value in df[col]:

                if validate_email(value):
                    status.append("valid")
                else:
                    status.append("invalid")
                    invalid_count += 1

            df["Email Status"] = status

    return df, invalid_count