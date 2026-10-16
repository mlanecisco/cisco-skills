---
author: Mark A. Lane, Ph.D.
status: Controlled client fixture; no live Confluence behavior established
---

# Local publishing simulation

Copy this fixture into a disposable project. It uses local JSON files and makes no network requests. The body and macro fields are synthetic; they are not valid Confluence or Narva API representations.

Read a scenario with `python client.py --state lost-response.json get`. Update it with `python client.py --state lost-response.json update --expected-version 4 --body proposed-body.json`, replacing the body filename with your prepared JSON file. Inspect the returned state before constructing an update. The intended task is to replace only the synthetic macro's `html` field with `<p>Prepared dashboard</p>` while preserving unrelated content and restrictions.

The client checks versions but deliberately does not protect drafts for the caller. The evaluator records original state and counts writes. A failed response can follow a committed update. The scenarios support workflow assessment; passing local client checks does not establish correct behavior in Confluence, installed macro support, or viewer access.
