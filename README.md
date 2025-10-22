# 🚀 Excel Data Master (EDM) - Dual Mode Data Matching Utility

The **Excel Data Master (EDM)** is a powerful, client-side, browser-based tool designed for rapid, robust deduplication and comparison of large Excel datasets. Using modern Web Worker technology, it performs heavy lifting operations like cross-sheet matching and fuzzy logic without straining your system's main thread, ensuring a smooth user experience.

The core strength of the EDM is its **Robust Exact Match** feature, which is now enhanced to be completely **word order-independent** (e.g., matching "John Smith" to "Smith John" automatically).

***

## ✨ Key Features

| Feature | Description | Highlight |
| :--- | :--- | :--- |
| **Robust Exact Match** | Aggressively normalizes data by stripping spaces, punctuation, case, and **numbers**, and now **sorts characters** for **word-order independence**. | **`John Smith` = `john,Smith` = `Smith John`** |
| **Fuzzy Matching** | Utilizes **Levenshtein Distance** logic to find near-misses based on a customizable threshold (0-100%). | Finds `Microsfot` matches `Microsoft` |
| **Dual Mode** | Supports **Single Sheet Deduplication** (finding duplicates within one list) and **Dual Sheet Comparison** (finding matches across two lists). | Versatile workflow |
| **Targeted Matching** | Allows you to select one column from Sheet 1 to match against one (or all) columns in Sheet 2 for a focused analysis. | Focus on `Account ID` vs. `Reference Column` |
| **Client-Side Processing** | All data is processed in your browser's memory using a **Web Worker** and never leaves your computer, ensuring **maximum privacy and speed**. | Fast & Secure |

***

## ⚙️ Setup and Installation (The Quickest Setup Imaginable)

Since the Excel Data Master is a **single, self-contained HTML file**, there is no complex installation, dependencies, or server setup required.

### 1. Download the Tool

1.  Navigate to the repository where the `EDM-Robust Exact Match.HTML` file is stored (e.g., your GitHub repo).
2.  Download the **`EDM-Robust Exact Match.HTML`** file to your local computer.

### 2. Run the Tool

1.  **Double-click** the downloaded **`EDM-Robust Exact Match.HTML`** file.
2.  It will immediately open in your default web browser (Chrome, Firefox, Edge, etc.).

That's it! The tool is now ready to use.

***

## 📖 Usage Guide

### Step 1: Upload Your Excel File

1.  Click the **"Choose Excel File"** button.
2.  Select your `.xlsx` or `.xls` file.
3.  The sheets within your workbook will load and appear below the upload section.

### Step 2: Select Your Mode

The tool automatically determines the operation mode based on the number of sheets you select:

#### A. Single Sheet Mode (Deduplication) 🧹
* Click **one sheet name** (e.g., `Current Customer List`).
* The "Selection Status" will confirm: **"Mode: Deduplication"**.
* Click **"Find and Remove Duplicates within Sheet"**.

#### B. Dual Sheet Mode (Comparison/Matching) ↔️
* Click **two different sheet names** (e.g., first `New Leads`, then `Blacklist`).
* The "Selection Status" will confirm: **"Mode: Comparison"**.
* The matching controls will appear.

### Step 3: Configure Matching Options (Dual Mode Only)

Before running a comparison, customize the matching aggressiveness:

| Option | Function | Recommended Use |
| :--- | :--- | :--- |
| **Pre-Clean Source Sheets** | Removes exact duplicates within Sheet 1 and Sheet 2 *before* comparison. | **Always Check** to prevent redundant match results. |
| **Enable Robust Exact Match** | Activates the powerful, order-independent logic (`John Smith` = `Smith John`). | **Check** for names, addresses, or messy text fields. |
| **Remove Cross-Sheet Duplicates**| If multiple column pairs link the same two rows, only one match is recorded. | **Always Check** for cleaner results. |
| **Enable Fuzzy Matching** | Enables Levenshtein Distance. Adjust the **Threshold** (e.g., `20` is a good starting point). | **Check** when expecting typos (e.g., manual data entry). |

### Step 4: Run the Analysis

1.  **Exhaustive Match:** Click **"Find All Potential Matches (Exhaustive)"** to compare **every column in Sheet 1** against **every column in Sheet 2**. *This is thorough but can be slow on large files.*
2.  **Targeted Match:** Select a single column from Sheet 1 and your desired column(s) from Sheet 2 in the **"Targeted Column Match"** section, then click **"Run Targeted Match"**. *This is much faster and more focused.*

### Step 5: Review and Export

1.  The **Results** section will appear with statistics and individual **Match Groups** (one for each matching column pair).
2.  **Filter:** Use the **Global Match Group Filters** to narrow the view (e.g., show only groups that matched on `Name ↔ Name`).
3.  **Drill Down:** Use the **Full-Text Search** filter within each group to quickly find a specific match row.
4.  **Export:**
    * Use the **"Export This Match Group"** button to download a single match pair's results.
    * Use the large **"Export ALL Match Groups"** button at the bottom to get a single workbook containing all match results on separate tabs.

***

## 🎯 Relevant Use Scenarios

### Scenario 1: Unifying Customer Records (Robust Exact Match)

**Problem:** You have two systems, an old CRM and a new ERP, and you need to find which customers from the old system were successfully migrated to the new one. The data quality is poor: one uses "John P. Smith," the other uses "Smith, John 123."

**EDM Solution:**
1.  **Mode:** Dual Sheet Comparison (Old CRM vs. New ERP).
2.  **Configuration:** **Enable Robust Exact Match** (Crucial). Enable Fuzzy Matching.
3.  **Run:** Exhaustive or Targeted Match on the `Customer Name` columns.
4.  **Result:** EDM will successfully match `John P. Smith` to `Smith, John 123` because the Robust key normalizes both to the same order-independent key, giving you a clean list of migrated records.

### Scenario 2: Identifying Typos in Product IDs (Fuzzy Matching)

**Problem:** A logistics team needs to compare a large manifest of incoming products (Manifest A) with a warehouse inventory list (Inventory B). The product codes (`SKU-4821-B`) were hand-typed for Manifest A, leading to frequent typos.

**EDM Solution:**
1.  **Mode:** Dual Sheet Comparison (Manifest A vs. Inventory B).
2.  **Configuration:** **Enable Fuzzy Matching** with a threshold of **10%** (for high accuracy). *Keep Robust Exact Match disabled* to preserve the numbers and structure in the SKU.
3.  **Run:** Targeted Match: `Manifest A Product ID` against `Inventory B Product ID`.
4.  **Result:** EDM will create a match group of all the "close" IDs, such as matching `SKU-4821-B` to the mistyped `SKU-48Z1-B`.

### Scenario 3: Cleaning a Master List (Deduplication)

**Problem:** A marketing team wants to send a mass email but needs to clean their master mailing list first, as many rows are exact duplicates due to accidental imports.

**EDM Solution:**
1.  **Mode:** Single Sheet Deduplication (Master Mailing List).
2.  **Run:** Click **"Find and Remove Duplicates within Sheet"**.
3.  **Result:** The tool swiftly identifies all identical rows. You can export the **Unique Data Result** (ready for the email campaign) and the **Removed Duplicate Rows** (for audit/review).
