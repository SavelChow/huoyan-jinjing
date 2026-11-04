"""Small shared invariants; no model or ground truth is read here."""

def validate_expected_counts(counts):
    if not isinstance(counts, dict) or set(counts) != {"1", "2", "3", "4", "5"}:
        raise ValueError("expected_counts must contain exactly string keys 1..5")
    if any(type(value) is not int or value < 0 for value in counts.values()):
        raise ValueError("expected counts must be non-negative integers")
    return dict(counts)


def decision_from_counts(observed, expected, non_catalogue_count, review_required=False):
    """Pure decision rule, never changes detection or counts."""
    observed = validate_expected_counts(observed)
    expected = validate_expected_counts(expected)
    if type(non_catalogue_count) is not int or non_catalogue_count < 0:
        raise ValueError("invalid non_catalogue_count")
    if review_required:
        return {"status": "REVIEW_REQUIRED", "predicted_label": None}
    passed = observed == expected and non_catalogue_count == 0
    return {"status": "OK", "predicted_label": "PASS" if passed else "FAIL"}
