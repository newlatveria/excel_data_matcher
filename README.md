# 🚀 EDM: Excel Data Utility (Dual Mode) - The Ultimate Data Cleaner & Matcher!

---

## 🔥 Unleash the Power of Robust Data Comparison!

Tired of clunky, slow, and rigid Excel tools? Meet **EDM**, a lightning-fast, browser-based Excel utility powered by **Web Workers** for high-performance data matching and deduplication. EDM goes beyond simple exact matches, introducing the revolutionary **Robust Exact Match** to find hidden relationships even when your data is messy!

Whether you need to clean a massive list or reconcile two complex datasets, EDM is your one-stop solution.

---

## ✨ Cutting-Edge Features You'll Love

| Feature | Description | Mode |
| :--- | :--- | :--- |
| **💪 Robust Exact Match** | Aggressively strips spaces, punctuation, and numbers for key comparison. **`John Smith` = `johnsmith` = `Smith2John`**. Finds matches traditional tools miss. | Comparison |
| **✨ Fuzzy Matching** | Leverages **Levenshtein Distance** to identify near-matches based on a user-defined threshold (default 20%). | Comparison |
| **🧹 Dual Modes** | Seamlessly switch between **Single-Sheet Deduplication** and **Two-Sheet Comparison**. | Both |
| **🎯 Targeted Match** | Compare a **single key column** (Sheet 1) against a specific column or **ALL** columns (Sheet 2) for maximum efficiency. | Comparison |
| **🔍 Exhaustive Match** | Run a matrix comparison of **all columns in Sheet 1 against all columns in Sheet 2** to discover every potential link. | Comparison |
| **🧼 Pre-Clean Source Data** | Option to remove internal duplicate rows from Sheet 1 and Sheet 2 *before* running the cross-sheet comparison. | Comparison |
| **🗑️ Cross-Match Deduplication** | Automatically removes redundant match pairs (e.g., if Name and ID both match the same two rows, only one result is kept). | Comparison |
| **📊 Advanced Filtering** | Filter results by **Match Count (Min/Max)**, **Fuzzy Only** groups, **Matched Column Pair**, and perform a **Full-Text Search** within any result group. | Comparison |
| **💾 Full Data Export** | All matches/unique rows are included in the exported file, even if the UI display is limited to the first 1,000 results. | Both |
| **🔢 Original Row Trace** | Exported data includes the **Original Row Number** from the source sheet, even after pre-cleaning, for easy tracing back to the source file. | Comparison |

---

## 💡 Use Case Scenarios

### Deduplication Mode (Single Sheet)
* **CRM Clean-Up:** You have a master list of customer accounts. Use EDM to quickly identify and extract all **perfectly duplicate rows** (every column is identical) to ensure data integrity.
* **Inventory Management:** You need a list of **truly unique SKUs** based on the full row details, including quantity, color, and price.

### Comparison Mode (Two Sheets)
* **Invoice Reconciliation:** Match vendor names and amounts from an **Invoices Received** sheet against a **Payments Sent** sheet, using the Robust Exact Match to handle messy data like `Acme Inc.` vs. `ACME, Inc.`.
* **Data Migration Validation:** Compare old system data (Sheet 1) with new system data (Sheet 2) using **Exhaustive Match** to ensure no data points were lost during the migration process.
* **Lead Generation:** Use **Targeted Match** to take a list of potential customer names (Sheet 1, Column A) and search for them across every column (Name, Email, Address, Notes) in your existing **Customer Database** (Sheet 2).

---

## 🛠️ Getting Started from GitHub (Run Instantly!)

Since EDM is built purely on **HTML and JavaScript**, running it is incredibly simple and requires **no installation**!

1.  **Clone or Download:** Clone this repository or download the `EDM-Robust Exact Match.HTML` file to your local machine.
2.  **Open in Browser:** **Double-click** the `EDM-Robust Exact Match.HTML` file. It will automatically open in your default web browser (Chrome, Firefox, Edge, etc.).
3.  **Start Working:** You are now ready to upload your Excel files and begin processing data!

> **Pro Tip:** For optimal performance, especially with large files, ensure you are using a modern browser and open your browser's **Developer Console (F12)** to view detailed file-loading logs and track progress.

---

## 📝 Step-by-Step Usage Instructions

### I. File Upload & Sheet Selection

1.  Click the **"Choose Excel File"** button and select your `.xlsx` or `.xls` file.
2.  The utility will load all sheets and display them as interactive buttons below.
3.  **Select Your Mode:**
    * **Deduplication:** Click **one** sheet button.
    * **Comparison:** Click **two** different sheet buttons.

### II. Single-Sheet Deduplication Mode

1.  After selecting **one sheet**, the status will update to **"Mode: Deduplication"**.
2.  Click the **"🧹 Find and Remove Duplicates within Sheet"** button.
3.  The utility will process the sheet, identifying and separating unique and duplicate rows based on an exact match across all cell values.
4.  **View Results:**
    * **Unique Data Result:** Contains all cleaned, unique rows. Click **"Download Unique Data"** to export.
    * **Removed Duplicate Rows:** Contains all rows that were removed. Click **"Download Duplicated Rows"** to export.

### III. Two-Sheet Comparison Mode

1.  After selecting **two sheets**, the status will update to **"Mode: Comparison"**.
2.  **Configure Options:**
    * **Dedupe Source Sheets:** Check this to remove internal duplicates *before* cross-sheet comparison. Recommended!
    * **Robust Exact Match:** **CHECK THIS** to utilize the aggressive cleaning logic (`john.smith` = `johnsmith`).
    * **Fuzzy Matching:** Check this and set your **Fuzzy Match Threshold** (e.g., 20 is a good starting point) to find near-matches.
3.  **Choose Your Comparison:**
    * **A. Exhaustive Match:** Click **"Find All Potential Matches (Exhaustive)"** to compare every column against every other column. Best for initial discovery.
    * **B. Targeted Column Match:** Select a single column from **Sheet 1** and a target (either a specific column or **"ALL"** columns) from **Sheet 2**, then click **"🎯 Run Targeted Match"**. Best for focused analysis.
4.  **View & Filter Results:**
    * Results are grouped by the matched column pair (e.g., `Sheet1: Email` ↔️ `Sheet2: Email`).
    * Use the **Global Match Group Filters** at the top to quickly filter results (e.g., show only groups with Fuzzy Matches, or only matches found via the `Name` ↔️ `Customer` pair).
    * Use the **Individual Group Filters** (Text Search, Row # Filters) to zero in on specific results within a large match group.
5.  **Export:**
    * Click the green **"Export This Match Group"** button to download the results for a single column pair.
    * Click the red **"Export ALL Match Groups to a Single Workbook"** button to download all match groups into separate tabs in one file.

---

## ❓ FAQ (Frequently Asked Questions)

| Question | Answer |
| :--- | :--- |
| **Why is it browser-based?** | It uses your browser's **JavaScript engine** and **Web Workers** for concurrent, high-speed, client-side processing, meaning your data **never leaves your computer** and is not sent to a server. |
| **How fast is it?** | Due to Web Workers, it's very fast. File parsing is synchronous, but the complex **comparison logic runs in a separate thread**, preventing the browser from freezing and delivering a smooth experience even with hundreds of thousands of rows. |
| **What's the difference between Robust and Fuzzy Match?** | **Robust Exact Match** is still an *exact match* after aggressively cleaning the data (removing all non-alphanumeric characters). **Fuzzy Match** is a *near match* that allows for slight differences (e.g., one letter typo) based on the Levenshtein distance calculation. |
| **Why are only 1,000 matches showing?** | The UI limits displayed rows to 1,000 for performance and responsiveness. **All matches** are included in the exported Excel file. |
| **What does 'Original Row #' mean in the export?** | This is the row number of the matched data point **in the source file**, allowing you to easily track the result back to the original spreadsheet, especially if you used the "Pre-Clean Source Sheets" option. |
