"""Intentionally defective input for the dashboard repair evaluation."""


def summarize(records, region=None):
    selected = [row for row in records if region is None or row["region"] == region]
    completed = sum(row["status"] == "complete" for row in records)
    return {
        "count": len(selected),
        "total_value": sum(row["value"] for row in selected),
        "completion_rate": completed / len(records) * 100 if records else 0.0,
    }
