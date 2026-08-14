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

---

# Algorithm Complexity and Benchmark Analysis

## Time Complexity

| Algorithm | Best Case | Worst Case |
|---|---|---|
| `insertion_sort` | O(n) | O(n²) |
| `binary_search` | O(1) | O(log n) |
| `linear_search` | O(1) | O(n) |

### Insertion Sort

The `insertion_sort` implementation uses insertion sort. In the best case, the records are already sorted, so each element requires only a small number of comparisons and the running time is O(n). In the worst case, records are in reverse order, causing many shifts and comparisons, giving O(n²) time complexity.

### Binary Search

The `binary_search` implementation operates on a sorted list. Its best case is O(1), when the target is found at the first midpoint checked. Its worst case is O(log n) because each comparison approximately halves the remaining search range.

### Linear Search

The `linear_search` implementation checks records sequentially from the beginning. Its best case is O(1), when the first record matches. Its worst case is O(n), when the target is at the end or is absent.

## Benchmark Evidence

The comparison-counting benchmark uses task-shaped records containing the same fields used by the application:

```text
title
priority
due_date
```

Raw counted results:

| Number of Tasks | Insertion Sort Comparisons | Binary Search Comparisons | Linear Search Comparisons |
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

```text
insertion_sort_count(records, key)
binary_search_count(sorted_records, target_value, key)
linear_search_count(records, target_value, key)
```

`insertion_sort_count` returns only an integer comparison count.

`binary_search_count` and `linear_search_count` return dictionaries containing exactly:

```text
index
comparison_count
```

---

# Automated Algorithm Checks

Run the automated checks with:

```powershell
python check_algorithms.py
```

The script uses plain `if`/`else` conditional statements and prints a `PASS` or `FAIL` line for every required case.

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

The checks complete normally and produce PASS lines for all required cases.

---

# AI Quick-Add

TaskFlow provides a Quick-Add endpoint that accepts a free-text task description and creates a real task in the same `tasks` database table used by the rest of the application.

## Endpoint

```text
POST /tasks/quick-add
```

## Request Body

```json
{
  "description": "Urgent finish the project today",
  "project_id": 1
}
```

## Example Response

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

The created row belongs to the supplied `project_id` and is stored in the same `tasks` table used by the normal CRUD endpoints.

---

## Quick-Add Parser

The Quick-Add feature uses a deterministic, rule-based, keyless mock parser.

It makes:

- Zero network calls
- Zero external API calls
- No API key requirements

The parser uses a standard role-based message structure:

- A `system` role describing the expected parsing behavior
- A `user` role containing the original free-text description

The deterministic mock parser is used by default.

---

## Priority Rules

Priority is determined in this exact order:

1. If the description contains `urgent` or `asap` → `high`
2. Otherwise, if it contains `whenever` or `low priority` → `low`
3. Otherwise → `medium`

If both priority groups occur, the high-priority group wins.

Priority is always one of:

```text
low
medium
high
```

### Example

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

Although both `ASAP` and `whenever` are present, the first priority group wins, so the priority is `high`.

---

## Due-Date Rules

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

The first matching phrase is selected.

For `next <weekday>`, the complete two-word phrase is consumed as one match. This prevents `next` from being left behind in the title.

If no date phrase matches:

```text
due_date_hint = null
```

The matched phrase is stored in lower-case in the task's text `due_date` field.

---

## Title Rules

The title is derived from the original-cased description.

For priority stripping, every occurrence of all of these keywords is removed:

```text
urgent
asap
whenever
low priority
```

The matched due-date phrase is also removed from the title.

The remaining text is trimmed using:

```python
.strip()
```

If the result is empty or whitespace-only, the title becomes:

```text
Untitled task
```

The title is therefore never an empty string.

---

# Worked Parser Examples

The following examples illustrate the deterministic parser rules precisely.

| # | Input `description` | Expected parsed fields |
|---|---|---|
| 1 | `"This is urgent, mark it ASAP please"` | `title: "This is , mark it please"`, `priority: "high"`, `due_date_hint: null` — both `"urgent"` and `"ASAP"` occurrences are removed. |
| 2 | `" "` | `title: "Untitled task"`, `priority: "medium"`, `due_date_hint: null` — no keywords match and the remaining title is whitespace-only. |
| 3 | `"Finish the report next Friday, it's urgent"` | `title: "Finish the report , it's"`, `priority: "high"`, `due_date_hint: "next friday"` — `"next Friday"` is matched as one two-word phrase and `"urgent"` is also removed. |
| 4 | `"tomorrow review tomorrow"` | `title: "review"`, `priority: "medium"`, `due_date_hint: "tomorrow"` — every occurrence of `"tomorrow"` is removed. |

---

# Task 6 — Additional Parser Examples

The following five additional examples test different combinations of priority keywords, date hints, and title stripping.

| # | Input `description` | Expected `title` | Expected `priority` | Expected `due_date_hint` |
|---|---|---|---|---|
| 1 | `"Call the client asap tomorrow"` | `"Call the client"` | `"high"` | `"tomorrow"` |
| 2 | `"Prepare presentation whenever next week"` | `"Prepare presentation"` | `"low"` | `"next week"` |
| 3 | `"Submit assignment on Friday"` | `"Submit assignment on"` | `"medium"` | `"friday"` |
| 4 | `"urgent urgent fix the bug today"` | `"fix the bug"` | `"high"` | `"today"` |
| 5 | `"Plan meeting next Tuesday with team"` | `"Plan meeting with team"` | `"medium"` | `"next tuesday"` |

These examples verify:

- Priority keyword detection
- Multiple priority keyword occurrences
- Default medium priority
- Date phrase detection
- `next <weekday>` handling
- Multiple date occurrences
- Title stripping
- Case preservation in the remaining title

---

# Quick-Add Test Examples

The following requests were tested against the running FastAPI application.

### Test 1 — High Priority

Request:

```json
{
  "description": "Urgent finish the project today",
  "project_id": 1
}
```

Result:

```text
title: finish the project
priority: high
due_date: today
```

### Test 2 — Low Priority

Request:

```json
{
  "description": "Buy groceries whenever tomorrow",
  "project_id": 1
}
```

Result:

```text
title: Buy groceries
priority: low
due_date: tomorrow
```

### Test 3 — High Priority Wins

Request:

```json
{
  "description": "ASAP submit report whenever next monday",
  "project_id": 1
}
```

Result:

```text
title: submit report
priority: high
due_date: next monday
```

These tests confirm that the endpoint creates real database records and that the required deterministic parsing rules are being applied.

---

# Database Integration

Quick-Add uses the same SQLAlchemy database session dependency as the existing task CRUD endpoints.

The endpoint:

1. Receives the free-text description and project ID.
2. Validates that the project exists.
3. Builds the role-based system/user message structure.
4. Runs the deterministic mock parser.
5. Creates a real `Task` object.
6. Saves the task to the existing `tasks` table.
7. Returns the created task using the same `TaskResponse` model as the normal task creation endpoint.

---

# Project Structure

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

---

# Verification Commands

Run the automated algorithm checks:

```powershell
python check_algorithms.py
```

Run the comparison benchmark:

```powershell
python benchmark.py
```

Start the API:

```powershell
uvicorn main:app --reload
```

Test Quick-Add:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/tasks/quick-add" `
  -ContentType "application/json" `
  -Body '{"description":"Urgent finish the project today","project_id":1}'
```

Expected result:

```text
title      : finish the project
priority   : high
due_date   : today
```

The project includes the required custom sorting, searching, comparison-counting benchmark, automated algorithm checks, deterministic Quick-Add parser, and real database integration.