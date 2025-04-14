# Veridion Challenge – Entity Resolution

## 📝 Task
Identify unique companies and group duplicate records accordingly.

---

## 🧠 Context
The dataset contains company records imported from multiple systems, which may include **duplicate entries with slight variations**. These variations can appear in fields like company name, country, or website, due to different formats, typos, or missing data.

---

## 📌 Guidelines

- **Understand the problem deeply before writing code.**
  Even the most sophisticated solution is ineffective if it solves the wrong problem.

- **Not all fields are necessary for deduplication.**
  The key challenge is to identify and leverage the **most relevant attributes** to accurately detect and group duplicate records.

- **Research what uniquely defines a company.**
  Consider fields like name, domain/website, country, and others — and determine which ones are essential for grouping.

- **Handle incomplete data.**
  Some fields may be missing or inconsistent. What matters is the reasoning behind your decisions and how clearly you document them.

- **Document your approach.**
  Explain the logic, assumptions, and rules you applied when identifying duplicates.

- **Choose your own tools and language.**
  You can use **any tech stack** you prefer (Veridion prefers Python, Java, Scala).

- **Scalability is a bonus.**
  You don’t need to scale to billions of records, but your solution should be designed thoughtfully and allow future scaling.

---

## ✅ Expected Deliverables

### 1. 📄 Solution Explanation / Presentation
Provide a detailed explanation of:
- Your approach
- Tools and techniques used
- What decisions you made (and why)
- What worked and what didn't

### 2. 📊 Output
Return an **updated dataset** in which:
- Duplicate records are grouped or tagged
- You can clearly see which rows represent the same entity

### 3. 💻 Code and Logic
- Include all code and logic used to achieve your solution
- Ensure it’s clean, commented, and reproducible

---

## 🚀 Submission
When your challenge is complete, submit the **GitHub link to this project** with all the deliverables listed above.

## 🧠 Reasoning and Approach Draft

After reading the task description carefully, I decided to begin by loading the provided dataset using `pandas` and inspecting the structure and content of both rows and columns. My first goal is to analyze how similar the string fields are between entries using `thefuzz`.

### 🔍 Observations & Early Challenges

- One immediate challenge is the presence of missing or null values in certain fields. This makes direct comparison more difficult, especially when trying to rely on fields like address, phone number, or domain.
- A key decision is whether to compare companies **only by name** or to include other attributes such as location, country, phone number, etc. Using only one field may lead to false positives or missed duplicates.

### 🤔 Example Scenarios

- For example, if we encounter both **"Google Inc."** and **"Google Incorporated"**, and determine they are the same entity, we must decide: **which name do we keep** in the final output?
- One approach could be to retain the most complete version or the most frequently occurring variant.

### 💡 Merging Strategy (Data Enrichment)

A feature I’d like to incorporate is **information enrichment**:
If two records are deemed to refer to the same company, I can merge their values:
- If the first record has an empty phone number but the second one has a valid one → copy it.
- If the second record has a city or address not present in the first → merge it.

However, this introduces another challenge:
- **What if both records have values in the same field, but those values are different?**
  For example, two different phone numbers. In that case:
  - I would first check if the numbers are *structurally* similar (e.g., presence/absence of country code).
  - If the values are truly different, I might:
    - Choose one based on quality (e.g., longer, formatted),
    - Or log both versions for manual review,
    - Or even store them as a list if allowed.

### ✅ Next steps

- Define similarity rules for relevant fields (starting with company name).
- Handle missing data cleanly.
- Develop a logic to prioritize or merge values when duplicates are found.
---

## 🔧 Final Approach and Logic

After iterating through multiple ideas, the final implementation relies on the following strategy:

### 🧩 Field Selection Justification

After carefully reviewing all **77 available fields** in the dataset, I selected a subset of the most **relevant and conclusive attributes** for identifying duplicate companies.

The fields used in the comparison logic are:

- `company_name`, `company_legal_names`, `company_commercial_names`
- `main_country_code` / `main_country`, `main_region`, `main_city`, `main_postcode`, `main_street`
- `product_type`
- `primary_phone`

These fields capture the **core identity** of a company: name, location, contact details, and type of activity. Based on several experiments and visual inspection, these provided the most meaningful signal for entity resolution.

If a row is missing **all** of these key attributes, it's not feasible to confidently group it with any other entry, so such rows remain ungrouped.

### ❌ Why We Didn't Apply Data Enrichment

In the early stages of planning, I considered implementing **data enrichment** — meaning, merging values from multiple records once they were marked as duplicates (e.g. filling missing phone numbers, combining addresses, etc.).

However, after further analysis of the dataset and task objectives, I decided **not to include enrichment** in the final implementation. Here's why:

- The task focuses on **entity resolution**, not data completion.
- Merging data across records could introduce noise or incorrect values, especially if two duplicates have conflicting information.
- The expected output format is simply grouping duplicate records, not generating enriched master records.

That being said, the code is modular and could easily be extended with an enrichment step if required in the future.

### 🧬 1. Flexible Name Matching
The function `compare_names_flexibly()` uses cross-comparisons between:

- `company_name`
- `company_legal_names`
- `company_commercial_names`

Each combination is compared using different fuzzy matching techniques:
- strict (`ratio`)
- loose (`token_set_ratio`)
- strong (`partial_token_sort_ratio`), etc.

This allows detecting matches like:
- "IBM Corporation" ~ "International Business Machines"
- "Google Inc." ~ "Google Incorporated"

### 🌍 2. Contextual Validation
A name match is only accepted as a duplicate **if at least one of the following conditions is also true**:
- Same `main_country_code` or `main_country`
- Same `product_type`
- Same phone number or domain
- Same city, region or address fields

This helps reduce false positives for companies with similar names but different profiles (e.g. franchises or unrelated businesses in other countries).

### 🧩 3. Grouping Strategy
If two records are determined to be duplicates, they are assigned the same `group_id`. Each record also stores its `original_index` for traceability.

The result is saved in a `grouped_results.csv` file with **all original fields preserved** + these two columns:
- `group_id` → numeric ID of the cluster
- `original_index` → original row index in the input dataset

### 🧪 4. Test Scale
Due to runtime and visualization constraints, testing was done on a subset of **500 - 10 000 rows**.
The algorithm is functional on full datasets but not yet optimized for large-scale processing

---

## 🧪 Testing

The correctness of the duplicate detection algorithm was primarily validated through a dedicated test file:
`test/test_compare.py`

This file contains unit tests that cover:
- Positive cases where two or more company entries should be considered duplicates
- Negative cases where companies are clearly different and must not be grouped together
- Edge cases with missing fields or partial information

These tests are crafted using real examples from the dataset and assert the expected output of the comparison logic.

In addition to automated testing, the output CSV file was also manually inspected to validate the correctness of grouping decisions and ensure no obvious mismatches or false positives were present.

## 🧠 Notes and Iterative Thinking

Some parts of the initial planning are left intentionally in this README — even ideas that were discarded or adjusted later — to reflect the full reasoning process.

Veridion emphasizes clear problem thinking, not just final performance.
I aimed to balance flexibility, precision, and explainability in my approach.

---

## 📦 Python Dependencies

The following Python libraries were used in this project:

- **pandas**
  For reading the dataset, manipulating tabular data, and exporting results to CSV. Core to all data processing steps.

- **thefuzz**
  Provides fuzzy string matching (based on Levenshtein distance). Used to compare company names that are slightly different due to typos or formatting.

- **python-Levenshtein**
  Optional dependency that significantly speeds up `thefuzz`. It improves performance when processing larger datasets.

- **pyarrow**
  Required for reading the `.parquet` file format used for the input dataset.


To run this project, make sure you have Python installed (version 3.8 or higher is recommended).

Install all required packages using the command below:

```bash
pip install -r requirements.txt
