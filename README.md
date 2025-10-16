# 🚀 Excel Data Matcher: The Full-Scan Matrix Matcher

Tired of manually checking column-by-column for matches across massive spreadsheets? The **Excel Data Matcher** is a powerful, client-side HTML tool that performs a **full-matrix comparison**, automatically testing **every column** in one sheet against **every column** in another. Find all potential join keys, from exact IDs to slightly misspelled names, in a single click! 🤯

---

## ✨ Features That Supercharge Your Data Analysis

* **⚡ Full Matrix Comparison:** Automatically iterates through *all possible single-column pairs* between your two selected sheets (e.g., `Sheet1.ColA` vs `Sheet2.Col1`, `Sheet1.ColA` vs `Sheet2.Col2`, etc.) to surface every potential link.
* **💻 Client-Side & High Performance:** Runs entirely in your browser using **JavaScript Web Workers** to keep the interface responsive, even while processing tens of thousands of rows in the background. No data is ever uploaded to a server!
* **🧠 Fuzzy Matching (Levenshtein):** Don't miss out on near-matches! Toggle on **Fuzzy Matching** with a configurable threshold (based on Levenshtein distance) to intelligently pair up values with typos or minor variations.
* **🧹 Smart Deduplication:** Automatically **removes duplicate row pairings** by default, ensuring that each unique `(Row A, Row B)` match is only counted once, even if multiple fuzzy or exact matches were found for that row pair during the process.
* **📁 Dual Export Options:**
    * **Export All:** Download a single workbook containing a separate sheet for *every successful column-pair match*.
    * **Per-Group Export:** Download an individual Excel file for a single, specific column-pair match you deem most relevant.

---

## 🔍 Functionality Scenarios: Choosing Your Match Mode

The tool is designed to solve different data linkage problems. Understanding these scenarios allows you to tune the matching process for precision or comprehensive discovery.

### **Scenario 1: The Data Discovery Scan (Full-Matrix Exact Match)**

This is the **default and most comprehensive** mode. It addresses the challenge of having two datasets but not knowing which column to use as the join key.

| Setting | Status |
| :--- | :--- |
| **Fuzzy Match** | ❌ Disabled |
| **Deduplication** | ✅ Enabled (Recommended) |

* **Process:** The tool compares the value in **every column** in `Sheet A` against **every column** in `Sheet B` for an **exact value match**.
* **Use Case:** You receive new customer data and need to merge it with your internal system. The key field is named differently in both. The full scan will reveal an exact match between columns (e.g., finding the match between `CustomerList.ID` and `CRM.Client_Identifier`), showing all potential join keys.

### **Scenario 2: The Dirty Data Cleanup (Fuzzy Matching Mode)**

This scenario is vital when dealing with user-entered, scraped, or legacy data that is prone to slight errors, typos, or formatting inconsistencies.

| Setting | Status |
| :--- | :--- |
| **Fuzzy Match** | ✅ Enabled |
| **Deduplication** | ✅ Enabled (Recommended) |

* **Process:** The system uses the **Levenshtein Distance** algorithm to find pairs where values are similar (within the set **Fuzzy Threshold**), but not identical.
* **Use Case:** Matching names or addresses where typos exist. For example, matching **"Microsoft Corp."** to **"Microsft Corp"**. The tool finds this match because the difference is minimal and falls below the threshold, which an exact match would miss.

### **Scenario 3: The Forensic Analysis (Deduplication Disabled)**

Turning off deduplication allows for detailed examination, showing every instance of a match, even if a single row pair matches multiple ways.

| Setting | Status |
| :--- | :--- |
| **Fuzzy Match** | Optional |
| **Deduplication** | ❌ Disabled |

* **Process:** When a single row pair (`Sheet A, Row 5` and `Sheet B, Row 10`) matches multiple ways (e.g., both exactly and fuzzily), **every single instance is kept** in the results list for that column pair.
* **Use Case:** **Investigating Ambiguity** or analyzing **Many-to-Many** relationships. This helps debug why a record might be unexpectedly linking or appearing multiple times, revealing potential data quality issues that need to be addressed at the source.

---

## 🛠️ Installation and Usage

This tool is a single, self-contained HTML file. No installation, libraries, or server setup is required!

### **Direct Download and Local Use (Recommended)**

This is the fastest and easiest method to use the client-side application and allows you to run it completely **offline** after the first load.

1.  **Download:**
    * Click the green **`< > Code`** button.
    * Select **`Download ZIP`**.
2.  **Extract & Launch:** Unzip the downloaded file. Find the `data-matcher.html` file and **double-click it** to open it in your default web browser.

Once opened, proceed with the following steps:

1.  **Load Data:** Click **"Choose Excel File"** and select your `.xlsx` or `.xls` document.
2.  **Select Sheets:** Click on **exactly two** sheets in the list to define the comparison pair.
3.  **Run Comparison:** Click the **"Find All Potential Matches"** button.
4.  **Analyze Results:** Review the resulting groups. The matching columns are **highlighted** in the results table for easy visual inspection.

---

## ⚙️ Customization

| Option | Default | Description |
| :--- | :--- | :--- |
| **Remove Duplicate Matches** | ✅ Enabled | **Highly recommended.** Ensures a single row from Sheet 1 is only matched once to a single row in Sheet 2 for a given column pair. Disable only for forensic analysis (Scenario 3). |
| **Enable Fuzzy Matching** | ❌ Disabled | Turn this on to find matches where the key values are similar but not identical (e.g., "John Smith" vs "Jon Smith"). |
| **Fuzzy Match Threshold** | `20` | Only available when Fuzzy Matching is enabled. This value determines the leniency (Lower value = stricter/more exact match, Higher value = more lenient/more typos allowed). |
