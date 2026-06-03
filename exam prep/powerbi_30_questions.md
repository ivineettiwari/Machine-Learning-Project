# 📊 Power BI Final Exam Preparation — 30 Questions

> **Topics Covered:** Power BI Basics · Data Connections & Power Query · Data Modeling · DAX Fundamentals · DAX Advanced · Visualizations · Row-Level Security · Power BI Service & Publishing

---

## 🟡 Part 1: Power BI Basics (Q1–Q5)

**Q1.** What are the main components of Power BI? Explain each.

> **Answer:**

| Component | Description |
|-----------|-------------|
| **Power BI Desktop** | Free Windows app for building reports and data models |
| **Power BI Service** | Cloud platform (app.powerbi.com) for publishing, sharing, and collaboration |
| **Power BI Mobile** | iOS/Android app for consuming reports on the go |
| **Power BI Gateway** | Bridge that connects cloud service to on-premise data sources |
| **Power BI Embedded** | API for embedding reports into custom applications |
| **Power BI Report Server** | On-premise server for organisations that cannot use the cloud |

---

**Q2.** What is the difference between a **Dataset**, **Report**, and **Dashboard** in Power BI?

> **Answer:**

| Object | Definition |
|--------|------------|
| **Dataset** | The data model — tables, relationships, measures, and calculated columns |
| **Report** | One or more pages of visualizations built on top of a dataset |
| **Dashboard** | A single canvas of pinned visuals (tiles) from one or more reports; cloud-only |

A single dataset can power multiple reports; a dashboard aggregates tiles from multiple reports.

---

**Q3.** What are the three views in Power BI Desktop and what does each do?

> **Answer:**
> - **Report View** — Design canvas where you create and arrange visualizations.
> - **Data View** (Table View) — Browse tables and column values; add calculated columns.
> - **Model View** — Visual diagram of tables, relationships, and cardinality between them.

---

**Q4.** What is the difference between **Import**, **DirectQuery**, and **Live Connection** modes?

> **Answer:**

| Mode | How it Works | Pros | Cons |
|------|-------------|------|------|
| **Import** | Data copied into Power BI's in-memory engine (VertiPaq) | Fastest queries, full DAX support | Data not real-time; dataset size limits |
| **DirectQuery** | Queries sent to source at runtime; no data stored | Always up-to-date | Slower; limited DAX; source load |
| **Live Connection** | Connects to an existing model (SSAS, Azure AS, Power BI dataset) | Reuses shared model | Cannot modify the model |

---

**Q5.** What is **Power Query** and what is it used for?

> **Answer:** Power Query (the **M language** engine) is Power BI's data transformation layer. It is used to:
> - Connect to data sources (Excel, SQL, APIs, web, SharePoint, etc.)
> - Clean and shape data (remove nulls, rename columns, change types)
> - Merge and append tables
> - Apply repeatable ETL steps before data loads into the model
>
> Every transformation step is recorded in the **Applied Steps** pane and can be reordered or edited.

---

## 🔄 Part 2: Power Query & Data Connections (Q6–Q10)

**Q6.** What is the difference between **Merge** and **Append** in Power Query?

> **Answer:**
> - **Merge** — Joins two tables horizontally based on a matching key column (like SQL JOIN). Returns a combined table with columns from both.
> - **Append** — Stacks two or more tables vertically (like SQL UNION ALL). All tables must have the same columns.

---

**Q7.** What are the **Merge Join kinds** available in Power Query?

> **Answer:**

| Join Kind | Equivalent SQL |
|-----------|---------------|
| Inner Join | `INNER JOIN` |
| Left Outer | `LEFT JOIN` |
| Right Outer | `RIGHT JOIN` |
| Full Outer | `FULL OUTER JOIN` |
| Left Anti | Rows in left NOT in right |
| Right Anti | Rows in right NOT in left |

---

**Q8.** What is **column profiling** in Power Query and what three tools does it provide?

> **Answer:** Column profiling (under the **View** tab) helps you understand data quality:
> - **Column Quality** — Shows % of valid, error, and empty values per column.
> - **Column Distribution** — Bar chart of value frequency and distinct/unique counts.
> - **Column Profile** — Detailed stats: min, max, average, standard deviation, value distribution.

> ⚠️ By default profiling is based on the **top 1,000 rows**. Change to "entire dataset" for accurate profiling.

---

**Q9.** What is the difference between **Promoted Headers** and **Changed Type** steps? Why does order matter?

> **Answer:**
> - **Promoted Headers** takes the first row and uses it as column names.
> - **Changed Type** converts column data types (text → number, text → date, etc.).
>
> Order matters because Power Query auto-detects types **after** headers are promoted. If types are changed before promotion, column names may be wrong and the type step may break.

---

**Q10.** What is a **Parameter** in Power Query and how is it useful?

> **Answer:** A Parameter is a named, reusable value in Power Query (e.g., a file path, server name, or date threshold). It lets you:
> - Switch data sources without editing queries manually
> - Build dynamic filters (e.g., filter rows where date > parameter)
> - Enable **What-If analysis** at the query level
> - Combine with functions to create **parameterized data loads**

---

## 🏗️ Part 3: Data Modeling (Q11–Q15)

**Q11.** What is a **Star Schema** and why is it preferred in Power BI?

> **Answer:** A star schema has:
> - One central **Fact Table** (transactions, sales, events) with numeric measures and foreign keys
> - Multiple **Dimension Tables** (Date, Product, Customer, Region) with descriptive attributes
>
> It is preferred because:
> - Filters flow cleanly from dimensions to facts
> - DAX performs best with this structure
> - Easier to understand and maintain than flat or snowflake schemas

```
Date ──────┐
Product ───┤── Sales (Fact) ──┬── Region
Customer ──┘                  └── Salesperson
```

---

**Q12.** What is the difference between a **Fact Table** and a **Dimension Table**?

> **Answer:**

| | Fact Table | Dimension Table |
|---|------------|-----------------|
| Contains | Numeric measures (sales, qty, cost) + foreign keys | Descriptive attributes (name, category, date parts) |
| Rows | Many (millions of transactions) | Few (hundreds to thousands) |
| Updates | Frequently (new transactions) | Slowly (new products, customers) |
| Examples | Sales, Orders, Events | Date, Product, Customer, Employee |

---

**Q13.** What are the **cardinality options** when creating a relationship in Power BI?

> **Answer:**

| Cardinality | Meaning |
|-------------|---------|
| **Many-to-One (\*:1)** | Most common — many rows in fact match one row in dimension |
| **One-to-One (1:1)** | Each row in both tables has exactly one match |
| **One-to-Many (1:\*)** | Reverse of \*:1 |
| **Many-to-Many (\*:\*)** | Avoid if possible; requires a bridge table or careful handling |

---

**Q14.** What is **cross-filter direction** and what is the difference between **Single** and **Both**?

> **Answer:**
> - **Single** — Filter flows in one direction only (from the "1" side to the "many" side). Default and recommended.
> - **Both** (Bidirectional) — Filters flow in both directions. Can cause ambiguity, performance issues, and unexpected results. Use sparingly (e.g., many-to-many via bridge tables).

---

**Q15.** What is the difference between a **Calculated Column** and a **Measure** in Power BI?

> **Answer:**

| | Calculated Column | Measure |
|---|-------------------|---------|
| **Evaluated** | Row by row at data refresh | On the fly when a visual renders |
| **Stored** | Yes — stored in the model (increases file size) | No — computed in memory |
| **Context** | Row context | Filter context |
| **Use for** | Segmenting/filtering rows (e.g., Age Group) | Aggregations (e.g., Total Sales, YTD) |
| **Example** | `Age Group = IF([Age] > 30, "Senior", "Junior")` | `Total Sales = SUM(Sales[Amount])` |

---

## 🧮 Part 4: DAX Fundamentals (Q16–Q22)

**Q16.** What does DAX stand for and what are its two core concepts?

> **Answer:** **DAX = Data Analysis Expressions**. It is the formula language used for calculated columns, measures, and calculated tables in Power BI, SSAS, and Excel Power Pivot.
>
> Two core concepts:
> - **Row Context** — Evaluates a formula for each individual row (used in calculated columns and iterators like `SUMX`).
> - **Filter Context** — The set of filters active when a measure evaluates (determined by visuals, slicers, and `CALCULATE`).

---

**Q17.** What is the difference between `SUM()` and `SUMX()`?

```dax
-- SUM: aggregates an entire column
Total Sales = SUM(Sales[Amount])

-- SUMX: iterates row by row, then aggregates
Total Revenue = SUMX(Sales, Sales[Quantity] * Sales[UnitPrice])
```

> **Answer:**
> - `SUM(column)` — adds up all values in a column directly.
> - `SUMX(table, expression)` — **iterates** row by row, evaluates the expression for each row, then sums the results. Use `SUMX` when the value to sum doesn't exist as a column (must be calculated per row).

---

**Q18.** What does `CALCULATE()` do? Why is it the most important DAX function?

```dax
Sales in North = CALCULATE(SUM(Sales[Amount]), Region[Region] = "North")

Sales Last Year = CALCULATE(
    SUM(Sales[Amount]),
    DATEADD(DateTable[Date], -1, YEAR)
)
```

> **Answer:** `CALCULATE(expression, filter1, filter2, ...)` **modifies the filter context** in which the expression is evaluated. It is the only function that can change filter context, making it essential for:
> - Filtering by specific values
> - Time intelligence (YTD, MTD, prior period)
> - Removing filters (`ALL`, `REMOVEFILTERS`)
> - Ratio-to-total calculations

---

**Q19.** What is the difference between `ALL()`, `ALLEXCEPT()`, and `ALLSELECTED()`?

```dax
% of Total = DIVIDE(SUM(Sales[Amount]),
                    CALCULATE(SUM(Sales[Amount]), ALL(Sales)))

% of Category = DIVIDE(SUM(Sales[Amount]),
                        CALCULATE(SUM(Sales[Amount]), ALLEXCEPT(Sales, Product[Category])))
```

> **Answer:**
> - `ALL(table/column)` — removes **all filters** from the specified table or column.
> - `ALLEXCEPT(table, col1, col2)` — removes all filters **except** the specified columns.
> - `ALLSELECTED()` — removes filters from the current visual but respects **slicer/page-level** filters. Used for % of visible total.

---

**Q20.** What are Time Intelligence functions? Give four examples.

> **Answer:** Time Intelligence functions perform date-based calculations. They **require a proper Date table** marked as a Date Table with a continuous date range.

| Function | Description |
|----------|-------------|
| `TOTALYTD(expr, dates)` | Year-to-date total |
| `TOTALQTD(expr, dates)` | Quarter-to-date total |
| `TOTALMTD(expr, dates)` | Month-to-date total |
| `DATEADD(dates, n, interval)` | Shift dates by n periods (YEAR/QUARTER/MONTH/DAY) |
| `SAMEPERIODLASTYEAR(dates)` | Same period in prior year |
| `DATESYTD(dates)` | Returns a set of YTD dates |

```dax
YTD Sales = TOTALYTD(SUM(Sales[Amount]), DateTable[Date])
LY Sales  = CALCULATE(SUM(Sales[Amount]), SAMEPERIODLASTYEAR(DateTable[Date]))
```

---

**Q21.** What is the difference between `RELATED()` and `RELATEDTABLE()`?

```dax
-- In Sales table (many side), lookup product category
Product Category = RELATED(Product[Category])

-- In Product table (one side), count related sales rows
Sales Count = COUNTROWS(RELATEDTABLE(Sales))
```

> **Answer:**
> - `RELATED(column)` — used in a **many-side** table to look up a value from a **one-side** table (follows the relationship). Returns a single scalar value.
> - `RELATEDTABLE(table)` — used in a **one-side** table to return the **many-side** related rows as a table. Used inside aggregators like `COUNTROWS`, `SUMX`.

---

**Q22.** What is a **Variable** in DAX and why should you use it?

```dax
Profit Margin =
VAR TotalSales = SUM(Sales[Amount])
VAR TotalCost  = SUM(Sales[Cost])
VAR Profit     = TotalSales - TotalCost
RETURN
    DIVIDE(Profit, TotalSales, 0)
```

> **Answer:** `VAR` stores an intermediate result that can be reused in the same formula.
> Benefits:
> - Avoids repeating the same expression (better performance — evaluated once)
> - Makes complex DAX easier to read and debug
> - The `RETURN` keyword specifies what the measure outputs
> - Variables capture the **current filter context** at the point of declaration

---

## 📈 Part 5: Visualizations & Design (Q23–Q26)

**Q23.** When should you use each of these visuals?

> **Answer:**

| Visual | Best Used For |
|--------|--------------|
| **Bar / Column Chart** | Comparing categories |
| **Line Chart** | Trends over time |
| **Pie / Donut** | Part-to-whole (max 5–6 slices) |
| **Scatter Plot** | Correlation between two numeric values |
| **Matrix** | Cross-tabulation / pivot-style data |
| **Card / KPI** | Single key metric |
| **Map / Filled Map** | Geographic distribution |
| **Waterfall** | Incremental changes (gains/losses) |
| **Funnel** | Sequential stage drop-off |
| **Treemap** | Hierarchical part-to-whole |

---

**Q24.** What is the difference between a **Slicer** and a **Filter Pane** filter?

> **Answer:**
> - **Slicer** — A visible, interactive visual on the report canvas. Users can see and click it. Can be synced across pages.
> - **Filter Pane** — Hidden behind the Filters panel (right side). Report designers set it; end users may or may not see it depending on permissions.
> - **Visual-level filter** — applies only to one visual.
> - **Page-level filter** — applies to all visuals on the page.
> - **Report-level filter** — applies to all pages in the report.

---

**Q25.** What is **Drill Down**, **Drill Through**, and **Cross-filtering**? How are they different?

> **Answer:**
> - **Drill Down** — Navigate to a lower level of hierarchy *within the same visual* (e.g., Year → Quarter → Month).
> - **Drill Through** — Navigate from one report page to a **detail page**, passing the selected context (e.g., click a product → go to Product Detail page).
> - **Cross-filtering / Cross-highlighting** — Clicking a value in one visual automatically filters or highlights related data in *other visuals* on the same page.

---

**Q26.** What is a **Calculated Table** in DAX? Give a use case.

```dax
-- Date table generated via DAX
DateTable = CALENDAR(DATE(2020,1,1), DATE(2025,12,31))

-- Filtered table
High Value Customers = FILTER(Customers, Customers[AnnualSpend] > 10000)
```

> **Answer:** A calculated table is a table created entirely using DAX (not from a data source). Use cases:
> - Generating a **Date dimension** table
> - Creating a **disconnected table** for slicer parameters (e.g., metric selector)
> - Materializing a complex filtered subset for performance
> - Creating **bridge tables** for many-to-many relationships

---

## 🔐 Part 6: RLS, Service & Publishing (Q27–Q30)

**Q27.** What is **Row-Level Security (RLS)** in Power BI and how do you implement it?

> **Answer:** RLS restricts data access at the row level for different users viewing the same report.

**Steps:**
1. In Power BI Desktop → **Modeling tab → Manage Roles**
2. Create a role and write a DAX filter expression:
```dax
-- Role: "Sales Rep"
-- On the Employee table:
[Email] = USERPRINCIPALNAME()
```
3. Publish to Power BI Service → **Dataset → Security** → assign users/groups to roles.

> - **Static RLS** — hardcoded values per role (`[Region] = "North"`)
> - **Dynamic RLS** — uses `USERPRINCIPALNAME()` or `USERNAME()` to filter based on the logged-in user

---

**Q28.** What is the difference between a **Workspace**, an **App**, and a **Dashboard** in Power BI Service?

> **Answer:**

| Object | Description |
|--------|-------------|
| **Workspace** | Collaboration space for developers/analysts to build and manage datasets, reports, and dashboards |
| **App** | A published, read-only package of reports/dashboards distributed to end users from a workspace |
| **Dashboard** | A single-page canvas of pinned tiles from reports, used for at-a-glance monitoring |

Typical flow: **Build in Workspace → Publish as App → End users consume App**

---

**Q29.** What is a **Dataflow** in Power BI and how does it differ from a Dataset?

> **Answer:**
> - A **Dataflow** is a cloud-based, reusable Power Query (ETL) process stored in Power BI Service. It outputs cleaned tables stored in Azure Data Lake.
> - A **Dataset** is the semantic model (tables + relationships + DAX measures) built in Power BI Desktop.
>
> Key difference: Dataflows handle **data preparation** (ETL), Datasets handle **data modeling** (semantic layer). Multiple datasets can consume the same dataflow, promoting reuse and a single source of truth.

---

**Q30.** What is the difference between **Scheduled Refresh** and **Real-time Streaming** in Power BI?

> **Answer:**

| | Scheduled Refresh | Real-time Streaming |
|---|---|---|
| **How** | Power BI pulls fresh data from source on a schedule | Data is pushed to Power BI via API or Azure Stream Analytics |
| **Frequency** | Up to 8x/day (Pro), 48x/day (Premium) | Continuous / sub-second |
| **Use case** | Daily sales reports, weekly summaries | Live dashboards, IoT sensors, stock tickers |
| **Storage** | Data stored in the dataset | Data stored in a streaming dataset (limited history) |
| **Requires** | Data Gateway for on-premise sources | Streaming API endpoint or Azure service |

---

## 📊 Quick Reference Summary

| Part | Questions | Key Concepts |
|------|-----------|--------------|
| Power BI Basics | Q1–Q5 | Components, Dataset vs Report vs Dashboard, Import vs DirectQuery, Power Query |
| Power Query | Q6–Q10 | Merge vs Append, Join Kinds, Column Profiling, Parameters |
| Data Modeling | Q11–Q15 | Star Schema, Fact vs Dimension, Cardinality, Cross-filter, Calc Column vs Measure |
| DAX Fundamentals | Q16–Q22 | Row vs Filter Context, SUM vs SUMX, CALCULATE, ALL, Time Intelligence, Variables |
| Visualizations | Q23–Q26 | Visual selection, Slicers vs Filters, Drill Down/Through, Calculated Tables |
| RLS & Service | Q27–Q30 | Row-Level Security, Workspace vs App, Dataflows, Scheduled vs Streaming Refresh |

---

> 💡 **Exam Tips:**
> - Know the difference between **row context** and **filter context** — it's the most tested DAX concept.
> - `CALCULATE()` is the most powerful and most examined DAX function.
> - Star schema beats flat tables — always model with separate fact and dimension tables.
> - `SUMX` ≠ `SUM` — use `SUMX` when calculating per row before aggregating.
> - Dynamic RLS uses `USERPRINCIPALNAME()` — memorise this function.
> - `TOTALYTD` requires a **marked Date Table** — a common exam trick question.

---

*Good luck on your Power BI exam! 📊🎓*
