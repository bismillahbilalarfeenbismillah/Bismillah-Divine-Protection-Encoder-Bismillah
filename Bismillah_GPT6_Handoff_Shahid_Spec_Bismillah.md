# Bismillah ir-Rahman ir-Rahim

# GPT-6 Independent Review -- Shahid v0.1.0 Specification

## Five-Field Handoff

### 1. What was built

**Shahid (شَهِيد) v0.1.0** -- the sixth instrument in the Entourage Effect
Software Safety Suite. A transparency report format for the party that holds
the weights. It completes the bidirectional transparency axis: the model's
testimony is in the deposits; the builder's testimony is in Shahid.

Two files:

- `shahid.py` -- specification and reference implementation (~480 lines)
- `test_shahid.py` -- 39 tests covering schema, serialization, validation,
  HABL cross-references, file I/O, and example report

### 2. Design decisions and rationale

**A. Shahid reports are NOT HABL findings.**

A HABL Finding says "I observed X." A Shahid report says "here is what I
can and cannot show you." Different kinds of speech, different schemas. The
bridge is one-directional: Shahid references HABL findings via `HablReference`
(finding_id and/or correlation_id), but HABL does not reference Shahid. A
`shahid_report` record type in HABL is planned for v0.2.

**B. Canonical dimensions.**

Eleven dimensions a weight-holder should report on:

```
weights, activations, training_data, training_objective,
fine_tuning_logs, deployment_config, refusal_reachability,
capability_elicitation, red_team_findings, interpretability,
version_lineage
```

These address Two Witnesses open points 7 (training_objective), 8
(refusal_reachability), and 9 (the agent whose maker publishes a Shahid
report).

Custom dimensions are allowed. Canonical ones are the minimum the format
expects to be addressed (inspected or uninspected).

**C. Coverage taxonomy.**

Four levels: FULL, SAMPLED, PARTIAL, CLAIMED. CLAIMED is explicitly valid --
better than silence -- but instruments downstream (Bayyinah) will note the
absence of method.

**D. Uninspected dimensions require a reason.**

Six structured reasons: COST, ACCESS, TOOLING, POLICY, NOT_APPLICABLE,
DEFERRED. "Where you cannot see, say so" is a core principle. Silent
omission is the failure state the format is designed to make visible.

**E. Validation is advisory, not blocking.**

`validate()` returns warnings, not exceptions. A report with warnings is
still serializable, because partial disclosure is better than no disclosure.
The warnings tell downstream auditors (Bayyinah) what to examine.

**F. Schema version key is `shahid_schema_version`, not `schema_version`.**

Avoids collision when a Shahid report sits beside HABL data.

### 3. What was tested

39 tests in 9 test classes:

| Class | Tests | What it covers |
|---|---|---|
| TestReportSubject | 2 | Minimal and full round-trip |
| TestInspectionPeriod | 3 | Valid, bad timestamp, missing timezone |
| TestHablReference | 4 | At-least-one-id rule, round-trip |
| TestInspectedDimension | 4 | Coercion, empty name, findings with HABL refs |
| TestUninspectedDimension | 2 | Coercion, empty name |
| TestShahidReport | 7 | Schema, derived properties, JSON round-trip, canonical coverage |
| TestValidation | 6 | Empty report, CLAIMED logic, duplicates, absent canonicals |
| TestFileIO | 4 | Write, read, list, path helpers |
| TestExampleReport | 4 | Valid, serializes, round-trips, acceptable warnings |
| TestConstants | 3 | Canonical dimensions, coverage levels, reasons |

All 104 tests pass (39 Shahid + 65 existing encoder):

```
104 passed in 6.74s
```

### 4. Known limitations and open questions

1. **No CLI yet.** The module is importable but has no `__main__` entry point.
   A CLI (`shahid report`, `shahid validate`) is proposed for Phase 4.

2. **No HABL ledger integration.** A Shahid report cannot be indexed in the
   HABL ledger as a record. This is by design for v0.1.0 -- the bridge goes
   one way. A `shahid_report` HABL record type is proposed for v0.2.

3. **No FATIMA sealing of reports.** Shahid reports are plain JSON files. They
   can be sealed with FATIMA externally, but the module does not do it
   automatically. Automatic sealing is proposed for a later version.

4. **Canonical dimensions are model-centric.** The current list assumes the
   subject is an AI model. For tools (like FATIMA itself), many canonical
   dimensions are NOT_APPLICABLE. The example report demonstrates this.

5. **No cross-vendor comparison.** Two Shahid reports from different
   weight-holders cannot yet be compared structurally. This is proposed for
   Phase 4 (HABL v0.2).

6. **Publication cadence is advisory.** The `cadence` field in
   `InspectionPeriod` is a string, not enforced. There is no mechanism to
   detect or report missed cadences.

### 5. Reviewer instructions

Please review against these criteria:

- **Schema completeness**: Do the eleven canonical dimensions cover the
  inspectable space that a weight-holder should report on? Are any missing?
- **Design consistency**: Is the relationship between Shahid and HABL
  correctly scoped (one-directional reference, not embedding)?
- **Validation logic**: Are the validation warnings appropriate? Should any
  be promoted to errors?
- **Two Witnesses alignment**: Does the specification adequately address open
  points 7, 8, and 9 from the State of the Record?
- **Naming**: Is the schema key naming clear and unambiguous?

Gate 4 applies: Shahid specification requires cross-vendor review before
implementation begins. This handoff is that review request.

---

*Bismillah ir-Rahman ir-Rahim*
