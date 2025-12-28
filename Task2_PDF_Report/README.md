

# Task-2: Automated PDF Report Generation

This task demonstrates how to use **Python** to read data from a file, analyze it, and generate a **formatted PDF report** using the **ReportLab** library.


## Objective

To:

* Read data from a CSV file
* Analyze numerical values
* Generate a formatted PDF report
* Automate the reporting process


## Technologies Used

* Python
* Pandas
* ReportLab


## Files in This Folder

| File                                | Description                                     |
| ----------------------------------- | ----------------------------------------------- |
| `report_script.py`                  | Python script that reads data and generates PDF |
| `data.csv`                          | Input data file containing student marks        |
| `output_samples/Student_Report.pdf` | Sample generated PDF report                     |
| `README.md`                         | Documentation                                   |


## How to Run

1. Install required libraries:

```bash
pip install pandas reportlab
```

2. Run the script:

```bash
python report_script.py
```

3. A PDF file named **`Student_Report.pdf`** will be generated.


## What the Script Does

The script performs the following steps:

* Loads student marks from `data.csv`
* Calculates:

  * Average marks
  * Highest marks
  * Lowest marks
* Writes these results into a formatted PDF file


## Sample Output

A sample generated report is available here:

```
output_samples/Student_Report.pdf
```

---

## Internship Requirement Mapping

| CODTECH Requirement   | Status |
| --------------------- | ------ |
| Read data from file   | ✔      |
| Analyze data          | ✔      |
| Generate PDF report   | ✔      |
| Provide script        | ✔      |
| Provide sample output | ✔      |

