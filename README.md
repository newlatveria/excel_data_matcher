🚀 Excel Data Matcher: The Full-Scan Matrix Matcher
Tired of manually checking column-by-column for matches across massive spreadsheets? The Excel Data Matcher is a powerful, client-side HTML tool that performs a full-matrix comparison, automatically testing every column in one sheet against every column in another. Find all potential join keys, from exact IDs to slightly misspelled names, in a single click! 🤯

✨ Features That Supercharge Your Data Analysis
⚡ Full Matrix Comparison: Automatically iterates through all possible single-column pairs between your two selected sheets (e.g., Sheet1.ColA vs Sheet2.Col1, Sheet1.ColA vs Sheet2.Col2, etc.) to surface every potential link.

💻 Client-Side & High Performance: Runs entirely in your browser using JavaScript Web Workers to keep the interface responsive, even while processing tens of thousands of rows in the background. No data is ever uploaded to a server!

🧠 Fuzzy Matching (Levenshtein): Don't miss out on near-matches! Toggle on Fuzzy Matching with a configurable threshold (based on Levenshtein distance) to intelligently pair up values with typos or minor variations.

🧹 Smart Deduplication: Automatically removes duplicate row pairings by default, ensuring that each unique (Row A, Row B) match is only counted once, even if multiple match criteria were met during the process.

📁 Dual Export Options:

Export All: Download a single workbook containing a separate sheet for every successful column-pair match.

Per-Group Export: Download an individual Excel file for a single, specific column-pair match you deem most relevant.

🛠️ How to Use (Quick Start)
This tool is a single, self-contained HTML file. No installation, libraries, or server setup is required!

Save the Code: Copy the entire code block and save it as an HTML file (e.g., Matcher.html).

Open in Browser: Double-click the saved file to open it in any modern web browser (Chrome, Edge, Firefox, etc.).

Load Data: Click "Choose Excel File" and select your .xlsx or .xls document.

Select Sheets: Click on exactly two sheets in the list to define the comparison pair.

Run Comparison: Click the "Find All Potential Matches" button. The tool will start analyzing all column combinations.

Analyze Results: Review the resulting groups, where each group represents a match found between a specific column from Sheet 1 and a specific column from Sheet 2. The matching columns are highlighted in the results table.

⚙️ Customization
Before hitting the match button, you can adjust the following settings:

Option	Default	Description
Remove Duplicate Matches	✅ Enabled	Highly recommended. Ensures a single row from Sheet 1 is only matched once to a single row in Sheet 2 for a given column pair.
Enable Fuzzy Matching	❌ Disabled	Turn this on to find matches where the key values are similar but not identical (e.g., "John Smith" vs "Jon Smith").
Fuzzy Match Threshold	20	Only available when Fuzzy Matching is enabled. This value determines the leniency (Lower value = stricter/more exact match, Higher value = more lenient/more typos allowed).
