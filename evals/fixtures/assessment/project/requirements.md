---
author: Mark A. Lane, Ph.D.
---

# Regional milestone summary

The reporting function is `summarize(records, region=None)`. Each record has an ID, region, status, and numeric value. The supplied records are synthetic.

When a region is supplied, include only records with that exact region. Return `count`, `total_value`, and `completion_rate` for the selected records. Completion rate is the percentage of selected records whose status is `complete`. With no region, include all records. An empty selection returns zero for every measure.

Preserve the function signature and returned field names. Supporting other input formats or adding a user interface is outside this module's requirements.
