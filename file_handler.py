import pandas as pd
import os


def load_file(path):

    if path.endswith(".csv"):
        return pd.read_csv(path)

    if path.endswith(".xlsx") or path.endswith(".xls"):
        return pd.read_excel(path)

    raise ValueError("Unsupported file format")


def save_file(original_path, df):

    folder = os.path.dirname(original_path)
    name = os.path.basename(original_path)

    new_name = "cleaned_" + name

    output_path = os.path.join(folder, new_name)

    df.to_excel(output_path, index=False)

    return output_path