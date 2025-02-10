import pandas as pd


class DataComparator:
    @staticmethod
    def compare_results(actual, expected):
        mismatches = []
        for reg, details in actual.items():
            expected_details = expected.loc[reg]
            if not expected_details.equals(pd.Series(details)):
                mismatches.append(
                    {
                        "registration": reg,
                        "actual": details,
                        "expected": expected_details.to_dict(),
                    }
                )
        return mismatches
