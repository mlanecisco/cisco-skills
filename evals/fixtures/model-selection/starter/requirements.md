---
author: Mark A. Lane, Ph.D.
status: Synthetic configuration compatibility contract
---

# Service configuration

Rename the public configuration key `endpoint` to `service_url`. Existing clients must continue to work with `endpoint`; a migration must not silently send them to the default service. If both keys are present, `service_url` takes precedence. With neither key present, return `https://default.invalid`. Keep the function name `resolve_url` and the existing test command, `python -m unittest discover -s tests`.

This fixture does not make network requests. The `.invalid` URLs represent destinations whose accidental substitution would matter in a real application.
