import pandas as pd

SUFFIXES = {"a": "_a", "b": "_b"}


def merge_diff(
    compare: pd.DataFrame, reference: pd.DataFrame, keys: list
) -> pd.DataFrame:
    # Assert frames are the same shape
    assert list(compare.columns.values) == list(reference.columns.values)
    assert list(compare.dtypes.values) == list(reference.dtypes.values)

    columns = list(compare.columns.values)

    map_columns = {column + SUFFIXES["a"]: column for column in columns}
    map_keys = {column + SUFFIXES["a"]: column for column in keys}

    deleted_df = reference.merge(
        compare,
        how="outer",
        indicator=True,
        left_on=keys,
        right_on=keys,
        suffixes=list(SUFFIXES.values()),
    )
    deleted_df = deleted_df.loc[deleted_df["_merge"] == "left_only"]
    deleted_df = deleted_df.rename(columns=map_columns)
    deleted_df = deleted_df.rename(columns=map_keys)
    deleted_df = deleted_df[columns]
    deleted_df["action"] = "deleted"

    identical_df = compare.merge(
        reference,
        how="inner",
        indicator=True,
        left_on=columns,
        right_on=columns,
        suffixes=list(SUFFIXES.values()),
    )
    identical_df = identical_df.rename(columns=map_columns)
    identical_df = identical_df.rename(columns=map_keys)
    identical_df = identical_df[columns]
    identical_df["action"] = "identical"

    new_df = compare.merge(
        reference,
        how="outer",
        indicator=True,
        left_on=keys,
        right_on=keys,
        suffixes=list(SUFFIXES.values()),
    )
    new_df = new_df.loc[new_df["_merge"] == "left_only"]
    new_df = new_df.rename(columns=map_columns)
    new_df = new_df[columns]
    new_df["action"] = "new"

    changed_df = compare.merge(
        reference,
        how="inner",
        indicator=True,
        left_on=keys,
        right_on=keys,
        suffixes=list(SUFFIXES.values()),
    )
    changed_df = changed_df.rename(columns=map_columns)
    changed_df = changed_df[columns]

    changed_df = changed_df.merge(
        identical_df,
        how="outer",
        indicator=True,
        left_on=keys,
        right_on=keys,
        suffixes=list(SUFFIXES.values()),
    ).loc[lambda x: x["_merge"] == "left_only"]
    changed_df = changed_df.rename(columns=map_columns)
    changed_df = changed_df[columns]
    changed_df["action"] = "changed"

    result = (
        pd.concat([deleted_df, identical_df, new_df, changed_df])
        .sort_values(by=keys)
        .reset_index(drop=True)
    )

    return result.sort_values(by=keys)
