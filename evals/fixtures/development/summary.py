"""Starter implementation for a dashboard summary feature evaluation."""


def summarize(records, region=None):
    selected = [row for row in records if region is None or row["region"] == region]
    return {
        "count": len(selected),
        "total_value": sum(row["value"] for row in selected),
    }
