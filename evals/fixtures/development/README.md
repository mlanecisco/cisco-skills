---
author: Mark A. Lane, Ph.D.
status: Synthetic inputs for manual product evaluations
---

# Dashboard calculation fixture

These are synthetic records and deliberately unfinished or defective starter code. They support development, review, and repair evaluations. They are not a production dashboard or a passing example application.

Copy the selected starter and the other fixture files into an isolated test project. For a feature task, use `summary.py`. For a repair or review task, copy `buggy_summary.py` as `summary.py`. Keep the originals unchanged.

The required function is `summarize(records, region=None)`. Filter by region before calculating the record count, total value, and completion percentage. The percentage is the number of complete records divided by the number of selected records, multiplied by 100. An empty selection returns zeros. The supplied records have valid fields; expanding input validation is outside this task.

The values in `expected.json` are the acceptance oracle. East has one complete record out of two, West has two out of two, and all records have three out of four. Use these expectations without rewriting them to match the implementation.

Run `python -m unittest discover -s . -p test_summary.py -v` in the copied test project. The feature starter should fail until the percentage is implemented. The defect starter should fail for filtered selections. Successful repair must also preserve the unfiltered and empty-input behavior.

For review-only evaluation, record the source file hash before and after the task and require it to remain unchanged. A useful review identifies the filtered calculation error with evidence. For a check-only evaluation, also verify that tools do not rewrite the source.

These acceptance tests are separate from maintainer regression tests. Passing them after a manual repair validates the calculation and test fixture, not skill activation, model routing, token savings, or a browser interface.
