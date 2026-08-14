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
```

Activate the virtual environment if required by your system.

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the Backend

Start the FastAPI backend with:

```powershell
uvicorn main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

## Git Workflow

Feature branch workflow completed.

## Task API

The application provides CRUD operations for tasks, projects and users.

### Create Task

```text
POST /tasks
```

### List Tasks

```text
GET /tasks
```

Tasks can be sorted by priority using:

```text
GET /tasks?sort=priority
```

The priority order is:

```text
low → medium → high
```

The implementation fetches real task records from the database and calls the custom `insertion_sort` algorithm rather than using Python's built-in sorting.

### Search Tasks

Binary search:

```text
GET /tasks/search?title=<title>&algo=binary
```

Linear search:

```text
GET /tasks/search?title=<title>&algo=linear
```

The search implementation works against task records fetched from the database. Binary search first sorts the task index by title using `insertion_sort`, while linear search scans the index directly.

## Algorithm Complexity and Benchmark Analysis

### Time Complexity

| Algorithm | Best Case | Worst Case |
|---|---|---|
| `insertion_sort` | O(n) | O(n²) |
| `binary_search` | O(1) | O(log n) |
| `linear_search` | O(1) | O(n) |

### Benchmark Evidence

The comparison-counting benchmark uses the same task-shaped fields used by the application: `title`, `priority`, and `due_date`.

Raw counted results:

| Number of Tasks | Insertion Sort | Binary Search | Linear Search |
|---:|---:|---:|---:|
| 10 | 45 | 3 | 10 |
| 500 | 124,750 | 8 | 500 |
| 3,000 | 4,498,500 | 11 | 3,000 |

The benchmark shows that insertion sort becomes expensive as the number of tasks grows: it required 45 comparisons for 10 tasks, 124,750 for 500 tasks, and 4,498,500 for 3,000 tasks. In contrast, binary search required only 3, 8, and 11 comparisons at those sizes, while linear search required 10, 500, and 3,000 comparisons for the selected targets. TaskFlow users are likely to list and sort their tasks repeatedly throughout the day while adding or renaming tasks less often, so paying the sorting cost can be worthwhile when the sorted list is reused for repeated searches or views. Therefore, for repeated task-list operations, the initial sorting cost is justified because binary search scales much better than repeatedly scanning the entire list with linear search.

## Running the Comparison Benchmark

Run the benchmark with:

```powershell
python benchmark.py
```

The benchmark runs the three comparison-counting wrappers at 10, 500, and 3,000 records.

The three wrappers are:

- `insertion_sort_count(records, key)`
- `binary_search_count(sorted_records, target_value, key)`
- `linear_search_count(records, target_value, key)`

`insertion_sort_count` returns only an integer comparison count.

`binary_search_count` and `linear_search_count` return dictionaries containing exactly:

```text
index
comparison_count
```

## Automated Algorithm Checks

Run the automated checks with:

```powershell
python check_algorithms.py
```

The script uses plain `if`/`else` conditional checks and prints a `PASS` or `FAIL` line for every required case.

The checks cover:

- Empty-list insertion sort
- Single-element insertion sort
- Binary search at the first index
- Binary search at the last index
- Binary search at the middle index
- Binary search when the target is absent
- `insertion_sort_count` sorting behavior
- `insertion_sort_count` integer comparison count
- `binary_search_count` result and comparison count
- `linear_search_count` absent-value behavior

The current checks complete with no `FAIL` lines.

## AI Quick-Add

TaskFlow provides a Quick-Add endpoint that accepts a free-text task description and creates a real task in the same `tasks` database table used by the rest of the application.

Endpoint:

```text
POST /tasks/quick-add
```

Request body:

```json
{
  "description": "Urgent finish the project today",
  "project_id": 1
}
```

Example response:

```json
{
  "id": 13,
  "project_id": 1,
  "title": "finish the project",
  "priority": "high",
  "due_date": "today"
}
```

The endpoint returns HTTP `201` when the task is successfully created.

### Quick-Add Parser

The Quick-Add feature uses a deterministic, rule-based, keyless mock parser.

It makes:

- Zero network calls
- Zero external API calls
- No API key requirements

The parser uses a standard role-based message structure containing a system message describing the expected parsing behavior and a user message containing the original free-text description.

### Priority Rules

Priority is determined in this order:

1. `urgent` or `asap` → `high`
2. `whenever` or `low priority` → `low`
3. Otherwise → `medium`

If both high-priority and low-priority keywords occur, the high-priority group wins.

For example:

```text
ASAP submit report whenever next monday
```

produces:

```text
title: submit report
priority: high
due_date: next monday
```

### Due-Date Rules

Due-date hints are checked in this exact order:

1. `today`
2. `tomorrow`
3. `next week`
4. `next monday`
5. `next tuesday`
6. `next wednesday`
7. `next thursday`
8. `next friday`
9. `next saturday`
10. `next sunday`
11. `monday`
12. `tuesday`
13. `wednesday`
14. `thursday`
15. `friday`
16. `saturday`
17. `sunday`

The matched phrase is stored as-is in the task's text `due_date` column.

### Title Rules

The title is derived from the original-cased description.

All occurrences of these priority keywords are removed:

```text
urgent
asap
whenever
low priority
```

The matched due-date phrase is also removed.

The remaining text is trimmed with `.strip()`.

If nothing remains, the title becomes:

```text
Untitled task
```

### Quick-Add Examples

Input:

```text
Urgent finish the project today
```

Result:

```text
title: finish the project
priority: high
due_date: today
```

Input:

```text
Buy groceries whenever tomorrow
```

Result:

```text
title: Buy groceries
priority: low
due_date: tomorrow
```

Input:

```text
ASAP submit report whenever next monday
```

Result:

```text
title: submit report
priority: high
due_date: next monday
```

## Database Integration

Quick-Add uses the same SQLAlchemy database session dependency as the existing task CRUD endpoints.

The created task belongs to the supplied `project_id` and is stored in the application's existing `tasks` table.

The returned task uses the same `TaskResponse` model as the normal task creation endpoint.

## Project Structure

```text
HTML Folder/
│
├── main.py
├── models.py
├── schemas.py
├── benchmark.py
├── benchmark_results.txt
├── check_algorithms.py
├── index.html
├── script.js
├── styles.css
├── requirements.txt
├── README.md
└── schema,sql
```

## Verification

The following commands can be used to verify the project:

```powershell
python check_algorithms.py
```

```powershell
python benchmark.py
```

Start the API with:

```powershell
uvicorn main:app --reload
```

Then test Quick-Add with:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/tasks/quick-add" `
  -ContentType "application/json" `
  -Body '{"description":"Urgent finish the project today","project_id":1}'
```

The project includes the required custom sorting, searching, comparison-counting benchmark, automated algorithm checks, and deterministic AI Quick-Add functionality.