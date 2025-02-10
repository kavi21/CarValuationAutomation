import re

import pandas as pd


class FileReader:
    @staticmethod
    def read_reg_numbers(file_path):
        """
        Reads the input text file and extracts vehicle registration numbers using regex.
        Handles cases where there are missing or incorrect values.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Regular expression to extract UK vehicle registration numbers (with or without spaces)
            reg_numbers = re.findall(r"\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b", content)

            if not reg_numbers:
                print(f"⚠️ Warning: No registration numbers found in {file_path}.")

            print(
                f"📌 Extracted {len(reg_numbers)} registration numbers: {reg_numbers}"
            )
            return reg_numbers

        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return []

    @staticmethod
    def read_expected_results(file_path):
        """
        Reads the expected car valuation results from a CSV file.
        Ensures the expected results are properly indexed by 'VARIANT_REG'.
        """
        try:
            df = pd.read_csv(file_path)

            # Validate that required columns exist
            required_columns = {"VARIANT_REG", "MAKE_MODEL", "YEAR"}
            if not required_columns.issubset(df.columns):
                raise ValueError(
                    f"Missing required columns in {file_path}: {required_columns - set(df.columns)}"
                )

            df.set_index("VARIANT_REG", inplace=True)
            print(f"✅ Successfully loaded expected results from {file_path}.")
            return df

        except FileNotFoundError:
            print(f"❌ Error: File {file_path} not found.")
            return pd.DataFrame()  # Return empty DataFrame
        except pd.errors.EmptyDataError:
            print(f"❌ Error: {file_path} is empty.")
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Unexpected error reading {file_path}: {e}")
            return pd.DataFrame()
