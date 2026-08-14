# Capstone Task Manager

A full-stack Task Manager application built with FastAPI, SQLAlchemy, PostgreSQL/Supabase, HTML, CSS and JavaScript.

## Requirements

- Python 3.x
- PostgreSQL/Supabase database
- FastAPI
- Uvicorn
- SQLAlchemy
- psycopg2-binary

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
## Git Workflow

Feature branch workflow completed.
## Algorithm Complexity and Benchmark Analysis

### Time Complexity

| Algorithm | Best Case | Worst Case |
|---|---|---|
| `insertion_sort` | O(n) | O(n²) |
| `binary_search` | O(1) | O(log n) |
| `linear_search` | O(1) | O(n) |

### Benchmark Evidence

The benchmark results show that insertion sort required 45 comparisons for 10 tasks, 124,750 comparisons for 500 tasks, and 4,498,500 comparisons for 3,000 tasks in the reverse-ordered case. In comparison, binary search required only 3, 8, and 11 comparisons at those same sizes, while linear search required 10, 500, and 3,000 comparisons for the selected targets. Although sorting the task list has an upfront cost, TaskFlow users are expected to list and sort tasks repeatedly throughout the day while adding or renaming tasks less frequently, so paying the sorting cost can be worthwhile when the sorted list is reused for multiple searches or views. Therefore, for repeated task-list operations, the initial sorting cost is justified because binary search scales much better than repeatedly scanning the entire list with linear search.