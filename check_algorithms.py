"""
Automated checks for Task 1-3 algorithms and Task 4 counting functions.

No assert, pytest, or unittest is used.
Every check prints PASS or FAIL and the script completes normally.
"""

from main import (
    insertion_sort,
    binary_search,
    linear_search,
)

from benchmark import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check_case(case_name, result, expected):
    """
    Basic PASS/FAIL check using plain if/else.
    """

    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(
            f"FAIL: {case_name} — "
            f"expected {expected}, got {result}"
        )


def check_condition(case_name, condition, expected, actual):
    """
    PASS/FAIL check for conditions that cannot be compared
    directly with a single == operation.
    """

    if condition:
        print(f"PASS: {case_name}")
    else:
        print(
            f"FAIL: {case_name} — "
            f"expected {expected}, got {actual}"
        )


def task_key(task):
    return task["title"]


# ============================================================
# 1. INSERTION SORT - EMPTY LIST
# ============================================================

records = []

try:
    result = insertion_sort(records, task_key)

    # Some implementations return the list, while others mutate
    # in place and return None. The important requirement is that
    # the original list remains empty and no error occurs.

    if records == []:
        print("PASS: insertion_sort empty list")
    else:
        print(
            "FAIL: insertion_sort empty list — "
            f"expected [], got {records}"
        )

except Exception as error:
    print(
        "FAIL: insertion_sort empty list — "
        f"expected no error, got {type(error).__name__}: {error}"
    )


# ============================================================
# 2. INSERTION SORT - SINGLE ELEMENT
# ============================================================

records = [
    {
        "title": "Only Task",
        "priority": "medium",
        "due_date": "2026-08-20",
    }
]

expected_single = list(records)

try:
    result = insertion_sort(records, task_key)

    if records == expected_single:
        print("PASS: insertion_sort single element")
    else:
        print(
            "FAIL: insertion_sort single element — "
            f"expected {expected_single}, got {records}"
        )

except Exception as error:
    print(
        "FAIL: insertion_sort single element — "
        f"expected no error, got {type(error).__name__}: {error}"
    )


# ============================================================
# 3. BINARY SEARCH - FIRST INDEX
# ============================================================

sorted_records = [
    {"title": "Task A", "priority": "low", "due_date": "2026-08-01"},
    {"title": "Task B", "priority": "low", "due_date": "2026-08-02"},
    {"title": "Task C", "priority": "medium", "due_date": "2026-08-03"},
    {"title": "Task D", "priority": "high", "due_date": "2026-08-04"},
    {"title": "Task E", "priority": "high", "due_date": "2026-08-05"},
]

try:
    result = binary_search(
        sorted_records,
        "Task A",
        "title",
    )

    check_case(
        "binary_search first index",
        result,
        0,
    )

except Exception as error:
    print(
        "FAIL: binary_search first index — "
        f"expected 0, got {type(error).__name__}: {error}"
    )


# ============================================================
# 4. BINARY SEARCH - LAST INDEX
# ============================================================

try:
    result = binary_search(
        sorted_records,
        "Task E",
        "title",
    )

    check_case(
        "binary_search last index",
        result,
        4,
    )

except Exception as error:
    print(
        "FAIL: binary_search last index — "
        f"expected 4, got {type(error).__name__}: {error}"
    )


# ============================================================
# 5. BINARY SEARCH - MIDDLE INDEX
# ============================================================

try:
    result = binary_search(
        sorted_records,
        "Task C",
        "title",
    )

    check_case(
        "binary_search middle index",
        result,
        2,
    )

except Exception as error:
    print(
        "FAIL: binary_search middle index — "
        f"expected 2, got {type(error).__name__}: {error}"
    )


# ============================================================
# 6. BINARY SEARCH - NOT FOUND
# ============================================================

try:
    result = binary_search(
        sorted_records,
        "Task Z",
        "title",
    )

    check_case(
        "binary_search not found",
        result,
        -1,
    )

except Exception as error:
    print(
        "FAIL: binary_search not found — "
        f"expected -1, got {type(error).__name__}: {error}"
    )


# ============================================================
# 7. INSERTION_SORT_COUNT
#    a) list is correctly sorted
#    b) result is plain int > 0
# ============================================================

count_records = [
    {"title": "Task D", "priority": "high", "due_date": "2026-08-04"},
    {"title": "Task A", "priority": "low", "due_date": "2026-08-01"},
    {"title": "Task C", "priority": "medium", "due_date": "2026-08-03"},
    {"title": "Task B", "priority": "low", "due_date": "2026-08-02"},
]

expected_sorted = [
    {"title": "Task A", "priority": "low", "due_date": "2026-08-01"},
    {"title": "Task B", "priority": "low", "due_date": "2026-08-02"},
    {"title": "Task C", "priority": "medium", "due_date": "2026-08-03"},
    {"title": "Task D", "priority": "high", "due_date": "2026-08-04"},
]

try:
    result = insertion_sort_count(
        count_records,
        task_key,
    )

    if count_records == expected_sorted:
        print("PASS: insertion_sort_count sorts list correctly")
    else:
        print(
            "FAIL: insertion_sort_count sorts list correctly — "
            f"expected {expected_sorted}, got {count_records}"
        )

    if type(result) == int and result > 0:
        print("PASS: insertion_sort_count returns int > 0")
    else:
        print(
            "FAIL: insertion_sort_count returns int > 0 — "
            f"expected plain int > 0, got {result!r} "
            f"of type {type(result).__name__}"
        )

except Exception as error:
    print(
        "FAIL: insertion_sort_count checks — "
        f"expected no error, got {type(error).__name__}: {error}"
    )


# ============================================================
# 8. BINARY_SEARCH_COUNT
# ============================================================

count_sorted_records = [
    {"title": "Task A", "priority": "low", "due_date": "2026-08-01"},
    {"title": "Task B", "priority": "low", "due_date": "2026-08-02"},
    {"title": "Task C", "priority": "medium", "due_date": "2026-08-03"},
    {"title": "Task D", "priority": "high", "due_date": "2026-08-04"},
    {"title": "Task E", "priority": "high", "due_date": "2026-08-05"},
]

try:
    result = binary_search_count(
        count_sorted_records,
        "Task C",
        task_key,
    )

    expected_index = 2

    if (
        type(result) == dict
        and result.get("index") == expected_index
        and type(result.get("comparison_count")) == int
        and result.get("comparison_count") > 0
    ):
        print("PASS: binary_search_count")
    else:
        expected = {
            "index": expected_index,
            "comparison_count": "plain int > 0",
        }

        print(
            "FAIL: binary_search_count — "
            f"expected {expected}, got {result}"
        )

except Exception as error:
    print(
        "FAIL: binary_search_count — "
        f"expected valid result, got "
        f"{type(error).__name__}: {error}"
    )


# ============================================================
# 9. LINEAR_SEARCH_COUNT - ABSENT VALUE
# ============================================================

linear_records = [
    {"title": "Task A", "priority": "low", "due_date": "2026-08-01"},
    {"title": "Task B", "priority": "medium", "due_date": "2026-08-02"},
    {"title": "Task C", "priority": "high", "due_date": "2026-08-03"},
    {"title": "Task D", "priority": "low", "due_date": "2026-08-04"},
]

try:
    result = linear_search_count(
        linear_records,
        "Task Z",
        task_key,
    )

    expected_index = -1
    expected_comparisons = len(linear_records)

    if (
        type(result) == dict
        and result.get("index") == expected_index
        and result.get("comparison_count") == expected_comparisons
    ):
        print("PASS: linear_search_count absent value")
    else:
        expected = {
            "index": expected_index,
            "comparison_count": expected_comparisons,
        }

        print(
            "FAIL: linear_search_count absent value — "
            f"expected {expected}, got {result}"
        )

except Exception as error:
    print(
        "FAIL: linear_search_count absent value — "
        f"expected valid result, got "
        f"{type(error).__name__}: {error}"
    )


print()
print("Algorithm checks completed.")