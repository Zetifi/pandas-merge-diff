import pandas as pd
from pandas._testing import assert_frame_equal

from .context import pandas_merge_diff

FRAME_A = pd.DataFrame(
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

FRAME_B = pd.DataFrame(
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


def test_merge_diff():
    keys = ["key1", "key2"]
    results = pandas_merge_diff.merge_diff(FRAME_A, FRAME_B, keys=["key1", "key2"])
    assert_frame_equal(
        results,
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
