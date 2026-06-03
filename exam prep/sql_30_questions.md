# 🗄️ SQL Final Exam Preparation — 30 Questions

> **Topics Covered:** SELECT & Filtering · JOINs · Aggregations & GROUP BY · Subqueries · Window Functions · DDL & DML · Indexes & Constraints · Transactions · Advanced Concepts

---

## 📘 Part 1: SELECT, Filtering & Sorting (Q1–Q6)

**Q1.** What is the output/result of this query? What does `DISTINCT` do?
```sql
SELECT DISTINCT department
FROM employees;
```
> **Answer:** Returns a list of **unique department names** — duplicate department values are eliminated. Without `DISTINCT`, each row's department would appear even if repeated.

---

**Q2.** What is the difference between `WHERE` and `HAVING`?
```sql
-- Query A
SELECT department, COUNT(*) AS total
FROM employees
WHERE salary > 50000
GROUP BY department;

-- Query B
SELECT department, COUNT(*) AS total
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```
> **Answer:**
> - `WHERE` filters **individual rows** *before* grouping.
> - `HAVING` filters **grouped results** *after* `GROUP BY`.
> - You **cannot** use aggregate functions in `WHERE`; use `HAVING` for that.

---

**Q3.** What is the order of SQL clause execution (logical query order)?

> **Answer:**
> ```
> FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
> ```
> This is why you **cannot** use a `SELECT` alias in a `WHERE` clause — `WHERE` runs before `SELECT`.

---

**Q4.** What is the output of this query?
```sql
SELECT name, salary
FROM employees
WHERE salary BETWEEN 40000 AND 60000
ORDER BY salary DESC
LIMIT 3;
```
> **Answer:** Returns the **top 3 highest-paid employees** with salaries between 40,000 and 60,000, sorted highest first. `BETWEEN` is **inclusive** on both ends.

---

**Q5.** What is the difference between `LIKE` and `ILIKE`? What do these patterns match?
```sql
WHERE name LIKE 'A%'       -- (a)
WHERE name LIKE '%son'     -- (b)
WHERE name LIKE '_a%'      -- (c)
WHERE name LIKE '%a_l%'    -- (d)
```
> **Answer:**
> - `LIKE` is **case-sensitive**; `ILIKE` (PostgreSQL) is **case-insensitive**.
> - `%` matches zero or more characters; `_` matches exactly one character.
> - (a) Names starting with `A`
> - (b) Names ending with `son`
> - (c) Names where the second character is `a`
> - (d) Names containing `a` followed by any char then `l`

---

**Q6.** What is the difference between `NULL` comparisons?
```sql
SELECT * FROM employees WHERE manager_id = NULL;    -- (a)
SELECT * FROM employees WHERE manager_id IS NULL;   -- (b)
SELECT * FROM employees WHERE manager_id IS NOT NULL; -- (c)
```
> **Answer:**
> - (a) **Returns no rows** — `NULL = NULL` evaluates to `UNKNOWN`, not `TRUE`. You can never use `=` with NULL.
> - (b) Correctly returns rows where `manager_id` is NULL.
> - (c) Returns rows where `manager_id` has a value.

---

## 🔗 Part 2: JOINs (Q7–Q12)

**Q7.** Explain the difference between `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`.

> **Answer:**

| Join Type | Returns |
|-----------|---------|
| `INNER JOIN` | Only rows with **matching keys** in both tables |
| `LEFT JOIN` | All rows from the **left** table + matched rows from right (NULLs for no match) |
| `RIGHT JOIN` | All rows from the **right** table + matched rows from left (NULLs for no match) |
| `FULL OUTER JOIN` | All rows from **both** tables; NULLs where no match exists |

---

**Q8.** Given these tables, what does the query return?

```
employees:  id | name    | dept_id
            1  | Alice   | 10
            2  | Bob     | 20
            3  | Carol   | NULL

departments: id | dept_name
             10 | HR
             30 | Finance
```
```sql
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```
> **Answer:**
> ```
> Alice  | HR
> Bob    | NULL
> Carol  | NULL
> ```
> Bob's dept_id (20) has no match in departments. Carol's dept_id is NULL. Both get NULL for `dept_name`.

---

**Q9.** What is a `SELF JOIN`? Write an example to find employees and their managers.
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```
> **Answer:** A self join joins a table **to itself**. Useful for hierarchical data (employees/managers, categories/subcategories). `LEFT JOIN` ensures employees with no manager (top-level) still appear with `NULL` as manager.

---

**Q10.** What is a `CROSS JOIN`? When would you use it?
```sql
SELECT a.color, b.size
FROM colors a
CROSS JOIN sizes b;
```
> **Answer:** Returns the **Cartesian product** — every row from the left combined with every row from the right. If `colors` has 3 rows and `sizes` has 4 rows, the result has 12 rows. Used to generate all combinations (e.g., product variants).

---

**Q11.** What is the difference between `JOIN` and a subquery for the same result?
```sql
-- Using JOIN
SELECT e.name FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE d.dept_name = 'HR';

-- Using subquery
SELECT name FROM employees
WHERE dept_id = (SELECT id FROM departments WHERE dept_name = 'HR');
```
> **Answer:** Both return the same result. JOINs are generally **faster and more readable** for simple lookups. Subqueries can be cleaner for complex filtering and are necessary when the subquery returns **multiple rows** (use `IN` instead of `=`).

---

**Q12.** Find employees who share the same department as 'Alice' (without hardcoding the dept).
```sql
SELECT name
FROM employees
WHERE dept_id = (
    SELECT dept_id FROM employees WHERE name = 'Alice'
)
AND name != 'Alice';
```
> **Answer:** The subquery fetches Alice's `dept_id`, then the outer query finds all other employees in that same department. This is a **correlated-style lookup** using a scalar subquery.

---

## 📊 Part 3: Aggregations & GROUP BY (Q13–Q17)

**Q13.** What are SQL's built-in aggregate functions? Give an example of each.

> **Answer:**

| Function | Description | Example |
|----------|-------------|---------|
| `COUNT(*)` | Count all rows | `COUNT(*)` |
| `COUNT(col)` | Count non-NULL values | `COUNT(email)` |
| `SUM(col)` | Total of values | `SUM(salary)` |
| `AVG(col)` | Average (ignores NULLs) | `AVG(score)` |
| `MIN(col)` | Smallest value | `MIN(hire_date)` |
| `MAX(col)` | Largest value | `MAX(salary)` |

---

**Q14.** What is the output of this query?
```sql
SELECT department,
       COUNT(*)          AS headcount,
       AVG(salary)       AS avg_salary,
       MAX(salary)       AS top_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000
ORDER BY avg_salary DESC;
```
> **Answer:** Returns one row per department where the **average salary exceeds 60,000**, sorted by average salary highest first. Each row shows department name, employee count, average, and maximum salary.

---

**Q15.** What is `GROUP BY ROLLUP`?
```sql
SELECT department, job_title, SUM(salary)
FROM employees
GROUP BY ROLLUP(department, job_title);
```
> **Answer:** `ROLLUP` generates **subtotals and a grand total**. It produces groupings for: `(department, job_title)` → `(department)` → `()` (grand total). NULL in the result indicates a subtotal/total row.

---

**Q16.** What is the difference between `COUNT(*)`, `COUNT(col)`, and `COUNT(DISTINCT col)`?
```sql
SELECT
    COUNT(*)                 AS total_rows,
    COUNT(manager_id)        AS has_manager,
    COUNT(DISTINCT dept_id)  AS unique_depts
FROM employees;
```
> **Answer:**
> - `COUNT(*)` — counts **all rows** including NULLs.
> - `COUNT(col)` — counts rows where `col` is **NOT NULL**.
> - `COUNT(DISTINCT col)` — counts **unique non-NULL** values.

---

**Q17.** Write a query to find the department with the highest total salary bill.
```sql
SELECT department, SUM(salary) AS total_salary
FROM employees
GROUP BY department
ORDER BY total_salary DESC
LIMIT 1;
```
> **Answer:** Groups by department, sums salaries, sorts descending, and picks the top row. In standard SQL you could also use a subquery with `MAX`.

---

## 🪟 Part 4: Subqueries & Window Functions (Q18–Q23)

**Q18.** What is a correlated subquery? How does it differ from a regular subquery?
```sql
-- Regular (runs once)
SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Correlated (runs once per row)
SELECT name, salary FROM employees e1
WHERE salary > (
    SELECT AVG(salary) FROM employees e2
    WHERE e2.department = e1.department
);
```
> **Answer:** A **regular subquery** runs once independently. A **correlated subquery** references the outer query and re-executes for **every row** of the outer query — useful for row-by-row comparisons but can be slower.

---

**Q19.** What is a CTE (Common Table Expression)? Rewrite Q18's correlated subquery using one.
```sql
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY department
)
SELECT e.name, e.salary, d.avg_sal
FROM employees e
JOIN dept_avg d ON e.department = d.department
WHERE e.salary > d.avg_sal;
```
> **Answer:** A CTE (introduced with `WITH`) is a **named temporary result set** valid for the duration of the query. It improves readability, replaces complex subqueries, and can be referenced multiple times. Equivalent to a derived table but far cleaner.

---

**Q20.** What is a window function? What makes it different from GROUP BY?
```sql
SELECT name, department, salary,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg,
       RANK()      OVER (PARTITION BY department ORDER BY salary DESC) AS rank
FROM employees;
```
> **Answer:** Window functions compute values **across a set of rows related to the current row** without collapsing them. Unlike `GROUP BY`, the original rows are **preserved**. `PARTITION BY` defines the window (like a GROUP BY within the window); `ORDER BY` defines the order within each partition.

---

**Q21.** What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`?

Given salaries: `100, 90, 90, 80`

> **Answer:**

| Function | Result | Behavior |
|----------|--------|----------|
| `ROW_NUMBER()` | 1, 2, 3, 4 | Always unique, no gaps, no ties |
| `RANK()` | 1, 2, 2, 4 | Ties get same rank; **gaps** after ties |
| `DENSE_RANK()` | 1, 2, 2, 3 | Ties get same rank; **no gaps** |

---

**Q22.** Write a query to get the **top 1 earner per department** using a window function.
```sql
WITH ranked AS (
    SELECT name, department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rn = 1;
```
> **Answer:** `ROW_NUMBER()` assigns rank within each department. Filtering `rn = 1` gives exactly one top earner per department (no ties). Use `RANK() = 1` if you want all top earners when there's a tie.

---

**Q23.** What do `LAG()` and `LEAD()` do?
```sql
SELECT month, revenue,
       LAG(revenue, 1)  OVER (ORDER BY month) AS prev_month,
       LEAD(revenue, 1) OVER (ORDER BY month) AS next_month,
       revenue - LAG(revenue, 1) OVER (ORDER BY month) AS mom_change
FROM monthly_sales;
```
> **Answer:**
> - `LAG(col, n)` — returns the value from **n rows before** the current row.
> - `LEAD(col, n)` — returns the value from **n rows after** the current row.
> Both return `NULL` when the offset goes out of range. Extremely useful for month-over-month or period comparisons.

---

## 🏗️ Part 5: DDL, DML, Constraints & Indexes (Q24–Q27)

**Q24.** What is the difference between DDL and DML? Give examples of each.

> **Answer:**

| Category | Stands For | Commands | Effect |
|----------|-----------|----------|--------|
| **DDL** | Data Definition Language | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | Changes **structure** |
| **DML** | Data Manipulation Language | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | Changes **data** |
| **DCL** | Data Control Language | `GRANT`, `REVOKE` | Controls **access** |
| **TCL** | Transaction Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Controls **transactions** |

---

**Q25.** What are SQL constraints? List and explain each.
```sql
CREATE TABLE orders (
    order_id    INT           PRIMARY KEY,
    customer_id INT           NOT NULL,
    amount      DECIMAL(10,2) CHECK (amount > 0),
    status      VARCHAR(20)   DEFAULT 'pending',
    email       VARCHAR(100)  UNIQUE,
    product_id  INT           REFERENCES products(id) ON DELETE CASCADE
);
```
> **Answer:**
> - `PRIMARY KEY` — uniquely identifies each row; implies `NOT NULL + UNIQUE`.
> - `NOT NULL` — column cannot contain NULL.
> - `UNIQUE` — all values in the column must be distinct.
> - `CHECK` — enforces a boolean condition on column values.
> - `DEFAULT` — provides a fallback value when none is supplied.
> - `FOREIGN KEY` / `REFERENCES` — enforces referential integrity between tables.
> - `ON DELETE CASCADE` — automatically deletes child rows when the parent is deleted.

---

**Q26.** What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?

> **Answer:**

| Command | Removes | Rollback? | Resets Identity? | Removes Structure? |
|---------|---------|-----------|------------------|--------------------|
| `DELETE` | Specific rows (with `WHERE`) or all rows | ✅ Yes | ❌ No | ❌ No |
| `TRUNCATE` | All rows instantly | ❌ No (usually) | ✅ Yes | ❌ No |
| `DROP` | Entire table/object | ❌ No | N/A | ✅ Yes |

---

**Q27.** What is an index? When should you add one, and when should you avoid it?
```sql
CREATE INDEX idx_employees_dept ON employees(department);
CREATE UNIQUE INDEX idx_email ON users(email);
```
> **Answer:** An index is a **data structure** (usually B-Tree) that speeds up lookups on a column. Add indexes on:
> - Columns used frequently in `WHERE`, `JOIN`, `ORDER BY`
> - Foreign key columns
> - Columns with high cardinality (many unique values)
>
> Avoid indexes on:
> - Small tables (full scan is faster)
> - Columns with very low cardinality (e.g., boolean flags)
> - Tables with very frequent `INSERT`/`UPDATE`/`DELETE` (indexes slow writes)

---

## 🔄 Part 6: Transactions & Advanced (Q28–Q30)

**Q28.** What are ACID properties in a database transaction?

> **Answer:**

| Property | Meaning |
|----------|---------|
| **Atomicity** | All operations in a transaction succeed or all are rolled back — no partial commits. |
| **Consistency** | A transaction brings the database from one valid state to another, respecting all constraints. |
| **Isolation** | Concurrent transactions do not interfere with each other. |
| **Durability** | Once committed, changes persist even after a system crash. |

```sql
BEGIN;
    UPDATE accounts SET balance = balance - 500 WHERE id = 1;
    UPDATE accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;
-- If either UPDATE fails, ROLLBACK undoes both
```

---

**Q29.** What is the difference between `UNION` and `UNION ALL`?
```sql
-- Returns unique rows (removes duplicates)
SELECT city FROM customers
UNION
SELECT city FROM suppliers;

-- Returns ALL rows including duplicates (faster)
SELECT city FROM customers
UNION ALL
SELECT city FROM suppliers;
```
> **Answer:**
> - `UNION` removes duplicate rows (like `DISTINCT`) — extra sort/hash step, **slower**.
> - `UNION ALL` keeps all rows including duplicates — **faster**, preferred when duplicates are acceptable or impossible.
> - Both require the **same number of columns** with **compatible data types**.

---

**Q30.** What is the difference between a `VIEW` and a materialized view? Write an example.
```sql
-- Regular VIEW (virtual, always up-to-date)
CREATE VIEW high_earners AS
SELECT name, department, salary
FROM employees
WHERE salary > 80000;

-- Query it like a table
SELECT * FROM high_earners WHERE department = 'Engineering';

-- MATERIALIZED VIEW (PostgreSQL — stored physically, refreshed manually)
CREATE MATERIALIZED VIEW dept_summary AS
SELECT department, COUNT(*), AVG(salary)
FROM employees
GROUP BY department;

REFRESH MATERIALIZED VIEW dept_summary;
```
> **Answer:**
> - A **VIEW** is a saved query — it runs the underlying SQL every time you query it. Always fresh, no storage overhead.
> - A **MATERIALIZED VIEW** stores the result physically like a table. Much faster to query but requires manual `REFRESH` to stay current. Best for expensive aggregations queried frequently.

---

## 📊 Quick Reference Summary

| Part | Questions | Key Concepts |
|------|-----------|--------------|
| SELECT & Filtering | Q1–Q6 | DISTINCT, WHERE vs HAVING, execution order, BETWEEN, LIKE, NULL handling |
| JOINs | Q7–Q12 | INNER/LEFT/RIGHT/FULL, SELF JOIN, CROSS JOIN, subquery vs JOIN |
| Aggregations | Q13–Q17 | COUNT/SUM/AVG/MIN/MAX, GROUP BY, ROLLUP, HAVING |
| Subqueries & Windows | Q18–Q23 | CTE, correlated subquery, RANK/DENSE_RANK/ROW_NUMBER, LAG/LEAD |
| DDL, DML & Indexes | Q24–Q27 | DDL vs DML, constraints, DELETE vs TRUNCATE vs DROP, indexes |
| Transactions & Advanced | Q28–Q30 | ACID, UNION vs UNION ALL, VIEW vs materialized view |

---

> 💡 **Exam Tips:**
> - Always remember `NULL` comparisons require `IS NULL` / `IS NOT NULL`.
> - `WHERE` runs before `GROUP BY`; `HAVING` runs after — never mix them up.
> - Window functions keep all rows; `GROUP BY` collapses them.
> - `RANK()` leaves gaps; `DENSE_RANK()` does not.
> - `UNION` deduplicates (slow); `UNION ALL` does not (fast).
> - `TRUNCATE` is faster than `DELETE` for clearing all rows but is usually not rollbackable.

---

*Good luck on your SQL exam! 🎓*
