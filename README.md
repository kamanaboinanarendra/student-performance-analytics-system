# Student Performance Analytics System

A complete, beginner-friendly Python data analysis mini-project developed for academic internship evaluation. The system analyzes student academic performance, determines individual subject and overall results, generates class-level summaries, and performs subject-wise diagnostic evaluations using Python, NumPy, Pandas, and CSV storage.

---

## 1. Project Title

**Student Performance Analytics System**  
*Academic Internship Mini-Project — Python Data Analytics*

---

## 2. Project Overview

The **Student Performance Analytics System** is a modular, command-line data processing application designed to evaluate and summarize student academic records. Built strictly with standard Python, NumPy, and Pandas, it loads tabular records from a CSV file, performs comprehensive schema and value integrity checks, computes totals, unrounded averages, independent grades, and strict pass/fail statuses, and provides an interactive terminal menu for querying, filtering, and reporting performance metrics.

---

## 3. Objective

The primary objectives of this system are:
1. **Automated Data Validation**: Guarantee data integrity by verifying schema structure, detecting duplicate identifiers, catching missing values, and validating numeric score boundaries.
2. **Accurate Academic Assessment**: Implement independent grading and pass/fail evaluations adhering strictly to academic policies (where individual subject mastery is mandatory for passing).
3. **Class & Subject Intelligence**: Provide aggregate statistical summaries including pass percentages, class averages, grade distributions, top performer identification (with tie handling), and subject-level difficulty assessments.
4. **Clean Code & Architecture**: Demonstrate clean modular design separating data logic (`functions.py`) from user interaction (`main.py`) using only authorized core libraries.

---

## 4. Technologies Used

* **Language**: Python 3.10+ (tested on Python 3.14)
* **Numerical Processing**: NumPy (vectorized sums, means, min/max, array comparisons)
* **Tabular Data Processing**: Pandas (CSV parsing, DataFrame filtering, aggregations, formatting)
* **Storage**: CSV (Comma-Separated Values)
* **Testing**: Python Standard Library `unittest`
* **Documentation**: Markdown

> **Technology Restrictions Compliance**: This project introduces zero unauthorized third-party libraries. It strictly excludes GUI frameworks (Tkinter), web frameworks (Flask/Django/Streamlit), visualization libraries (Matplotlib/Seaborn), machine learning libraries (Scikit-learn), databases, or Jupyter-specific dependencies.

---

## 5. Project Structure

The project strictly adheres to the following required structure:

```text
student-performance-analytics/
│
├── main.py                    # Application entry point and interactive CLI menu loop
├── functions.py               # Reusable validation, computation, and analysis functions
├── students.csv               # Baseline student dataset (25 fictional records)
├── README.md                  # Comprehensive project manual and execution guide
├── Project_Documentation.md   # Formal academic internship project report
└── requirements.txt           # Minimal external dependencies specification
```

---

## 6. Dataset Description

The baseline dataset is stored in `students.csv` and contains 25 realistic fictional student records across diverse engineering departments.

### Schema Specification

| Column # | Column Name   | Data Type | Description                                        | Permitted Range |
| -------- | ------------- | --------- | -------------------------------------------------- | --------------- |
| 1        | `Student_ID`  | String    | Unique student identification code (e.g., STD101)  | Unique, Non-empty |
| 2        | `Name`        | String    | Full name of the student                           | Non-empty       |
| 3        | `Department`  | String    | Academic department                                | Non-empty       |
| 4        | `Python`      | Numeric   | Marks obtained in Python Programming               | 0 to 100        |
| 5        | `Java`        | Numeric   | Marks obtained in Java Programming                 | 0 to 100        |
| 6        | `DBMS`        | Numeric   | Marks obtained in Database Management Systems      | 0 to 100        |
| 7        | `Networks`    | Numeric   | Marks obtained in Computer Networks                | 0 to 100        |
| 8        | `Maths`       | Numeric   | Marks obtained in Engineering Mathematics          | 0 to 100        |
| 9        | `Attendance`  | Numeric   | Semester class attendance percentage               | 0 to 100        |

---

## 7. Major Features

1. **Robust Startup Validation**: Comprehensive pre-flight checks validating file existence, non-emptiness, column naming and order, duplicate IDs, missing values, non-numeric inputs, and score bounds [0, 100]. Multiple errors are aggregated and reported together.
2. **Independent Grade & Pass/Fail Calculations**: Accurately handles the critical distinction between overall average grade and individual subject clearance.
3. **Multi-Performer Tie Handling**: Identifies all students sharing the highest average score rather than truncating to an arbitrary single winner.
4. **Subject Difficulty Analysis**: Computes mean, maximum, minimum, and subject-specific pass counts across all 5 subjects, programmatically identifying the best- and lowest-performing subjects.
5. **Interactive CLI Menu**: An 8-option terminal menu allowing display of all records, individual search by ID, filtering passed/failed cohorts, top students, subject metrics, class statistics, and safe termination.
6. **Data Immutability Guarantee**: The original `students.csv` baseline dataset is never modified, overwritten, or corrupted by runtime calculations.

---

## 8. Grading Policy

Grades are assigned based on the student's unrounded arithmetic mean across the five subjects:

| Average Marks Range    | Letter Grade | Performance Level |
| ---------------------- | :----------: | ----------------- |
| $\text{Average} \ge 90.0$ | **A**        | Outstanding       |
| $75.0 \le \text{Average} < 90.0$ | **B**        | Very Good         |
| $60.0 \le \text{Average} < 75.0$ | **C**        | Good              |
| $35.0 \le \text{Average} < 60.0$ | **D**        | Satisfactory      |
| $\text{Average} < 35.0$ | **F**        | Unsatisfactory    |

*Note: Boundary conditions (35.0, 60.0, 75.0, 90.0) are calculated using unrounded floating-point values. Rounded display values (to 2 decimal places) are used exclusively for presentation.*

---

## 9. Pass/Fail Policy

Academic regulations require mastery across all subjects:
* **Pass Criterion**: A student passes **if and only if** the marks obtained in **every single subject** (`Python`, `Java`, `DBMS`, `Networks`, `Maths`) are **at least 35** ($\ge 35$).
* **Fail Criterion**: If even one subject score is strictly below 35 ($< 35$), the student is marked **Fail**.
* **Independence Rule**: Grade and Pass/Fail status are determined independently. For instance, a student scoring 90, 80, 75, 20, 85 has an average of 70.00 (Grade C) but receives Status **Fail** because Networks is below 35. A student scoring exactly 35 in all five subjects achieves an average of 35.00, receives Grade D, and **passes**.

---

## 10. Installation Prerequisites

* Operating System: Windows 10/11, macOS, or Linux
* Python 3.10 or higher installed and added to the system `PATH`
* `pip` package manager installed

---

## 11. Installation Commands

Clone the repository and install the minimal required packages:

```powershell
# 1. Clone the repository
git clone https://github.com/[YOUR_USERNAME]/student-performance-analytics.git

# 2. Navigate to project root
cd student-performance-analytics

# 3. Install required dependencies
pip install -r requirements.txt
```

---

## 12. How to Run the Project

Execute `main.py` directly using Python:

```powershell
python main.py
```

---

## 13. Menu Options

Upon successful dataset loading, the program presents an interactive 8-option menu:

```text
===========================================================================
                                 MAIN MENU                                 
===========================================================================
1. Display all student records
2. Search for a student by ID
3. Display passed students
4. Display failed students
5. Display top-performing students
6. Display subject-wise statistics
7. Display overall class statistics
8. Exit the program
===========================================================================
```

---

## 14. Representative Sample Output

Below is actual output captured from program execution:

### Overall Class Performance Statistics (Option 7)

```text
--- Overall Class Performance Statistics ---
  Total Students Enrolled : 25
  Passed Students         : 17
  Failed Students         : 8
  Overall Pass Percentage : 68.00%
  Class Average Marks     : 62.98
  Highest Student Average : 94.20
  Lowest Student Average  : 21.80

  Top-Performing Student(s):
    * STD101 - Aarav Sharma (Computer Science): Avg = 94.20, Total = 471.0, Grade = A
    * STD102 - Diya Patel (Artificial Intelligence): Avg = 94.20, Total = 471.0, Grade = A

  Grade Distribution:
    Grade A:  3 student(s) ( 12.0%)  ###
    Grade B:  5 student(s) ( 20.0%)  #####
    Grade C:  8 student(s) ( 32.0%)  ########
    Grade D:  7 student(s) ( 28.0%)  #######
    Grade F:  2 student(s) (  8.0%)  ##
```

### Subject-Wise Performance Statistics (Option 6)

```text
--- Subject-Wise Performance Statistics ---
Subject          Average   Highest    Lowest   Passed Count
-----------------------------------------------------------
Python             64.24      96.0      20.0             22
Java               61.28      94.0      22.0             20
DBMS               62.88      94.0      25.0             22
Networks           60.88      96.0      18.0             21
Maths              65.60      95.0      24.0             23
-----------------------------------------------------------
Best-Performing Subject(s)  : Maths (Average: 65.60)
Lowest-Performing Subject(s): Networks (Average: 60.88)
```

### Student Search by ID (Option 2)

```text
Enter Student ID to search (e.g., STD101): STD101

Student Record Found:
---------------------------------------------
  Student ID    : STD101
  Name          : Aarav Sharma
  Department    : Computer Science
  Attendance    : 95%
---------------------------------------------
  Subject Marks :
    - Python      :  95.0  [Pass]
    - Java        :  92.0  [Pass]
    - DBMS        :  94.0  [Pass]
    - Networks    :  96.0  [Pass]
    - Maths       :  94.0  [Pass]
---------------------------------------------
  Total Marks   : 471.0 / 500.0
  Average Marks : 94.20
  Grade         : A
  Overall Status: Pass
---------------------------------------------
```

---

## 15. Testing Information

The system includes automated test coverage implemented via Python's standard library `unittest` module covering all 42 required specification scenarios across:
1. **Grading Boundary Tests**: Exact boundary checks (35, 60, 75, 90), below 35, and $\pm 0.001$ boundary transitions.
2. **Pass/Fail Tests**: Exact 35 in all subjects, single subject failure with high overall average, multi-subject failures.
3. **Class & Subject Analysis Tests**: Counts, pass percentages, class averages, tie handling for top students and subject averages.
4. **Data Validation Tests**: File existence, empty files, missing columns, duplicate IDs, missing values, non-numeric values, negative marks, marks > 100, invalid attendance.
5. **Search & Filter Tests**: Existing ID, nonexistent ID, case-insensitivity, empty filter responses.

To run the automated test suite:

```powershell
python test_suite.py
```

*Execution Result*: 42 distinct unit test methods executed, verifying all 42 specification cases in 0.423 seconds with 0 failures and 0 errors.

---

## 16. Known Limitations

* **Single Dataset Scope**: The current version operates on a single active CSV dataset at a time.
* **Console Display Width**: Displaying all 13 columns simultaneously requires a standard terminal window width of at least 110 columns for optimal table alignment.

---

## 17. Future Improvements

Future iterations maintaining the strict technology restrictions (Python, NumPy, Pandas, CSV) can incorporate:
1. Multi-semester CSV comparison and student progress tracking over time.
2. Exporting calculated class analytics and summary reports directly to new CSV output files.
3. Department-wise performance grouping and cross-departmental comparative metrics.
4. Attendance-to-performance correlation calculations using NumPy covariance and correlation coefficients.

---

## 18. GitHub Repository

* **Repository Name**: `student-performance-analytics`
* **Repository URL**: `https://github.com/[YOUR_USERNAME]/student-performance-analytics` *(Update with your actual GitHub username)*
