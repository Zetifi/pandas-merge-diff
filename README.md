# Pandas Merge Diff

Small utility that takes two identically shaped Pandas DataFrames and diffs them by a list of keys.

```
merge_diff(compare: pd.DataFrame, reference: pd.DataFrame, keys) -> pd.DataFrame:
```

Will return a new DataFrame with an `action` columns which will be set to `new|deleted|changed|identical`

| Action    | Explanation                                                                       |
| --------- | --------------------------------------------------------------------------------- |
| new       | The key(s) was not found in the reference rows.                                   |
| deleted   | The key(s) was not found in the compare rows.                                     |
| changed   | The key(s) was found in both rows, but one or more compared values are different. |
| identical | The key(s) was found in both rows, and the compared values are identical.         |

## Example Usage

Given two frames:

```
compare_df = pd.DataFrame(
    [
        {
            "key1": "AABB",
            "key2": "AABB",
            "email": "b@zetifi.com",
            "name": "BL",
        },
        {
            "key1": "FFAA",
            "key2": "FFBB",
            "email": "c@zetifi.com",
            "name": "CM",
        },
        {
            "key1": "BBCC",
            "key2": "BBCC",
            "email": "m@zetifi.com",
            "name": "Mik Warnakulasuriya Patabendige Ushantha Joseph Chaminda Vaas",
        },
        {
            "key1": "KKOO",
            "key2": "KKOO",
            "email": "m@zetifi.com",
            "name": "Mik Warnakulasuriya Patabendige Ushantha Joseph Chaminda Vaas",
        },
    ]
)

reference_df = pd.DataFrame(
    [
        {
            "key1": "AABB",
            "key2": "AABB",
            "email": "b@zetifi.com",
            "name": "BL",
        },
        {
            "key1": "FFAA",
            "key2": "CCFF",
            "email": "c@zetifi.com",
            "name": "CM",
        },
        {
            "key1": "KKOO",
            "key2": "KKOO",
            "email": "m@zetifi.com.au",
            "name": "Mik Warnakulasuriya Patabendige Ushantha Joseph Chaminda Vaas",
        },
    ]
)

assert_frame_equal(
    pandas_merge_diff.merge_diff(compare_df, reference_df, keys=["key1", "key2"]),
    pd.DataFrame(
        [
            {
                "key1": "AABB",
                "key2": "AABB",
                "email": "b@zetifi.com",
                "name": "BL",
                "action": "identical",
            },
            {
                "key1": "BBCC",
                "key2": "BBCC",
                "email": "m@zetifi.com",
                "name": "Mik Warnakulasuriya Patabendige Ushantha Joseph Chaminda Vaas",
                "action": "new",
            },
            {
                "key1": "FFAA",
                "key2": "CCFF",
                "email": "c@zetifi.com",
                "name": "CM",
                "action": "deleted",
            },
            {
                "key1": "FFAA",
                "key2": "FFBB",
                "email": "c@zetifi.com",
                "name": "CM",
                "action": "new",
            },
            {
                "key1": "KKOO",
                "key2": "KKOO",
                "email": "m@zetifi.com",
                "name": "Mik Warnakulasuriya Patabendige Ushantha Joseph Chaminda Vaas",
                "action": "changed",
            },
        ]
    ),
)
```
