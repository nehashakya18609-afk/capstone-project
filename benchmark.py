"""
Task 4 - Comparison Counting Benchmark

This benchmark uses synthetic in-memory task dictionaries with the
same fields used by the application's task endpoints:

    title
    priority
    due_date

Benchmark sizes:
    10
    500
    3000
"""


def insertion_sort_count(records, key):
    """
    Sort records in place exactly like insertion sort.

    Returns only the comparison count.
    """
    comparison_count = 0

    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0:
            comparison_count += 1

            if key(records[j]) <= key(current):
                break

            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return comparison_count


def binary_search_count(sorted_records, target_value, key):
    """
    Perform binary search on sorted records.

    Returns exactly:
        {
            "index": ...,
            "comparison_count": ...
        }
    """
    low = 0
    high = len(sorted_records) - 1
    comparison_count = 0

    while low <= high:
        mid = (low + high) // 2

        comparison_count += 1

        current_value = key(sorted_records[mid])

        if current_value == target_value:
            return {
                "index": mid,
                "comparison_count": comparison_count,
            }

        if current_value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "index": -1,
        "comparison_count": comparison_count,
    }


def linear_search_count(records, target_value, key):
    """
    Perform linear search.

    Returns exactly:
        {
            "index": ...,
            "comparison_count": ...
        }
    """
    comparison_count = 0

    for index, record in enumerate(records):
        comparison_count += 1

        if key(record) == target_value:
            return {
                "index": index,
                "comparison_count": comparison_count,
            }

    return {
        "index": -1,
        "comparison_count": comparison_count,
    }


def create_task_records(size):
    """
    Create synthetic task records using the same fields as the
    application's Task data.
    """

    priorities = ["low", "medium", "high"]

    records = [
        {
            "title": f"Task {i:05d}",
            "priority": priorities[i % 3],
            "due_date": f"2026-08-{(i % 28) + 1:02d}",
        }
        for i in range(size)
    ]

    # Reverse the records so insertion sort gets an unsorted,
    # realistic workload instead of already-sorted input.
    records.reverse()

    return records


def task_key(task):
    """
    Key function used by the sorting and searching engine.
    """
    return task["title"]


def run_benchmark():
    """
    Run the comparison-counting benchmark at three required sizes.
    """

    sizes = [10, 500, 3000]

    results = []

    for size in sizes:

        # Generate task-shaped records.
        records = create_task_records(size)

        # Keep a separate copy because insertion sort modifies
        # the records list in place.
        sort_records = list(records)

        # ---------------------------------------------------------
        # 1. INSERTION SORT
        # ---------------------------------------------------------

        insertion_count = insertion_sort_count(
            sort_records,
            task_key,
        )

        # ---------------------------------------------------------
        # 2. BINARY SEARCH
        # ---------------------------------------------------------

        # Binary search must operate on the sorted records.
        target_value = records[-1]["title"]

        binary_result = binary_search_count(
            sort_records,
            target_value,
            task_key,
        )

        # ---------------------------------------------------------
        # 3. LINEAR SEARCH
        # ---------------------------------------------------------

        # Linear search uses the original unsorted records.
        linear_result = linear_search_count(
            records,
            target_value,
            task_key,
        )

        result = {
            "size": size,
            "insertion_sort_comparisons": insertion_count,
            "binary_search": binary_result,
            "linear_search": linear_result,
        }

        results.append(result)

    return results


def print_results(results):
    """
    Print raw benchmark results.
    """

    print("Comparison-counting benchmark")
    print("=" * 60)

    for result in results:

        print()
        print(f"Size: {result['size']}")

        print(
            "Insertion sort comparisons:",
            result["insertion_sort_comparisons"],
        )

        print(
            "Binary search:",
            result["binary_search"],
        )

        print(
            "Linear search:",
            result["linear_search"],
        )


if __name__ == "__main__":
    benchmark_results = run_benchmark()
    print_results(benchmark_results)