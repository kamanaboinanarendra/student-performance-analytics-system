"""
functions.py - Student Performance Analytics System
==================================================
Reusable data processing, validation, calculation, and analysis functions
built using Python, NumPy, and Pandas.
"""

import os
import numpy as np
import pandas as pd

# Standard constant definitions
REQUIRED_COLUMNS = [
    'Student_ID',
    'Name',
    'Department',
    'Python',
    'Java',
    'DBMS',
    'Networks',
    'Maths',
    'Attendance'
]

SUBJECT_COLUMNS = ['Python', 'Java', 'DBMS', 'Networks', 'Maths']
NUMERIC_COLUMNS = SUBJECT_COLUMNS + ['Attendance']


# =====================================================================
# A. DATASET LOADING AND VALIDATION
# =====================================================================

def validate_dataset_structure_and_data(df):
    """
    Validates a loaded DataFrame against all schema, type, and value rules.
    Collects and returns all discovered errors as a list of descriptive strings.
    Does not modify the DataFrame or the original CSV file.
    """
    errors = []

    # 1. Check for empty DataFrame
    if df is None or df.empty:
        errors.append("Dataset is empty. It contains zero records.")
        return errors

    # 2. Check for required columns and exact column presence
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required column(s): {', '.join(missing_columns)}")
        # If columns are missing, dependent value checks cannot proceed safely
        return errors

    # Check for correct column ordering
    if list(df.columns[:len(REQUIRED_COLUMNS)]) != REQUIRED_COLUMNS:
        errors.append(
            f"Columns do not match expected order. Expected: {REQUIRED_COLUMNS}, "
            f"Found: {list(df.columns)}"
        )

    # 3. Check for missing (null / blank / NaN) values
    null_counts = df[REQUIRED_COLUMNS].isnull().sum()
    columns_with_nulls = null_counts[null_counts > 0]
    if not columns_with_nulls.empty:
        for col, count in columns_with_nulls.items():
            errors.append(f"Column '{col}' has {count} missing (empty/null) value(s).")

    # Check for empty string values in text columns
    for text_col in ['Student_ID', 'Name', 'Department']:
        if text_col in df.columns:
            empty_string_mask = df[text_col].astype(str).str.strip() == ''
            empty_count = empty_string_mask.sum()
            if empty_count > 0:
                errors.append(f"Column '{text_col}' contains {empty_count} blank/whitespace string(s).")

    # 4. Check for duplicate Student IDs
    if 'Student_ID' in df.columns:
        duplicate_ids = df[df['Student_ID'].duplicated(keep=False)]['Student_ID'].unique()
        if len(duplicate_ids) > 0:
            errors.append(f"Duplicate Student_ID values found: {list(duplicate_ids)}")

    # 5. Check numeric columns for non-numeric values and valid ranges [0, 100]
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            # Check if values can be parsed as numbers
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            non_numeric_count = numeric_series.isnull().sum() - df[col].isnull().sum()
            if non_numeric_count > 0:
                errors.append(f"Column '{col}' contains {non_numeric_count} non-numeric value(s).")

            # Check valid ranges for successfully parsed numbers
            valid_numbers = numeric_series.dropna()
            below_zero = valid_numbers[valid_numbers < 0]
            above_hundred = valid_numbers[valid_numbers > 100]

            if len(below_zero) > 0:
                errors.append(f"Column '{col}' contains values below 0: {list(below_zero.unique())}")
            if len(above_hundred) > 0:
                errors.append(f"Column '{col}' contains values above 100: {list(above_hundred.unique())}")

    return errors


def load_dataset(filepath):
    """
    Loads a dataset from the specified CSV filepath and validates it.
    
    Returns:
        tuple: (df, errors)
            df (pd.DataFrame or None): The loaded DataFrame if successful and valid.
            errors (list of str): List of error messages. Empty list if valid.
    """
    errors = []

    # Check file existence
    if not os.path.exists(filepath):
        errors.append(f"File not found: '{filepath}'. Please verify the file path.")
        return None, errors

    # Check if the file is empty (0 bytes)
    try:
        if os.path.getsize(filepath) == 0:
            errors.append(f"File is empty: '{filepath}' has a file size of 0 bytes.")
            return None, errors
    except OSError as e:
        errors.append(f"Could not inspect file '{filepath}': {str(e)}")
        return None, errors

    # Read CSV using Pandas
    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        errors.append(f"File '{filepath}' contains no data or valid headers.")
        return None, errors
    except pd.errors.ParserError as e:
        errors.append(f"Failed to parse CSV file '{filepath}': {str(e)}")
        return None, errors
    except Exception as e:
        errors.append(f"Unexpected error loading file '{filepath}': {str(e)}")
        return None, errors

    # Validate structure and values
    validation_errors = validate_dataset_structure_and_data(df)
    if validation_errors:
        return None, validation_errors

    # Cast numeric columns cleanly
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col])

    return df, []


# =====================================================================
# B. STUDENT CALCULATIONS (GRADES, PASS/FAIL, TOTAL, AVERAGE)
# =====================================================================

def calculate_grade(average):
    """
    Assigns a letter grade based on unrounded numerical average marks across 5 subjects:
        - Average >= 90: A
        - Average >= 75 and < 90: B
        - Average >= 60 and < 75: C
        - Average >= 35 and < 60: D
        - Average < 35: F
    """
    if average >= 90.0:
        return 'A'
    elif average >= 75.0:
        return 'B'
    elif average >= 60.0:
        return 'C'
    elif average >= 35.0:
        return 'D'
    else:
        return 'F'


def calculate_status(subject_marks):
    """
    Determines Pass/Fail status for a student.
    A student passes ONLY if all five subject marks are at least 35 (>= 35).
    If even one subject mark is below 35, the student fails.
    
    Args:
        subject_marks (iterable): Marks across the 5 subjects.
    Returns:
        str: 'Pass' or 'Fail'
    """
    marks_array = np.array(subject_marks, dtype=float)
    if np.all(marks_array >= 35.0):
        return 'Pass'
    else:
        return 'Fail'


def add_student_results(df):
    """
    Calculates Total, Average, Grade, and Status for each student in the DataFrame.
    Uses NumPy for numerical array operations.
    Returns a NEW DataFrame copy with the calculated columns added.
    The original DataFrame is preserved without modification.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    results_df = df.copy()

    # Extract subject marks matrix using NumPy
    marks_matrix = results_df[SUBJECT_COLUMNS].to_numpy(dtype=float)

    # 1. Total marks calculation using NumPy sum along rows
    totals = np.sum(marks_matrix, axis=1)
    results_df['Total'] = totals

    # 2. Average marks calculation using NumPy mean along rows (unrounded)
    averages = np.mean(marks_matrix, axis=1)
    results_df['Average'] = averages

    # 3. Grade calculation using unrounded averages
    grades = [calculate_grade(avg) for avg in averages]
    results_df['Grade'] = grades

    # 4. Pass/Fail status calculation independently using NumPy condition
    # Student passes only if all 5 subject marks are >= 35
    all_subjects_passed = np.all(marks_matrix >= 35.0, axis=1)
    statuses = np.where(all_subjects_passed, 'Pass', 'Fail')
    results_df['Status'] = statuses

    return results_df


# =====================================================================
# C. OVERALL CLASS STATISTICS
# =====================================================================

def get_class_statistics(df_results):
    """
    Computes overall class summary statistics from a DataFrame containing calculated results.
    
    Returns a dictionary with:
        - total_students (int)
        - passed_students (int)
        - failed_students (int)
        - pass_percentage (float)
        - class_average (float)
        - highest_average (float)
        - lowest_average (float)
        - top_students (list of dicts)
        - grade_counts (dict)
    """
    if df_results is None or df_results.empty:
        return {
            'error': 'Cannot compute statistics: No student records available.',
            'total_students': 0,
            'passed_students': 0,
            'failed_students': 0,
            'pass_percentage': 0.0,
            'class_average': 0.0,
            'highest_average': 0.0,
            'lowest_average': 0.0,
            'top_students': [],
            'grade_counts': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        }

    total_students = len(df_results)
    passed_students = int((df_results['Status'] == 'Pass').sum())
    failed_students = int((df_results['Status'] == 'Fail').sum())

    # Avoid division by zero
    pass_percentage = (passed_students / total_students) * 100.0 if total_students > 0 else 0.0

    # Numerical calculations using NumPy
    averages_array = df_results['Average'].to_numpy(dtype=float)
    class_average = float(np.mean(averages_array))
    highest_average = float(np.max(averages_array))
    lowest_average = float(np.min(averages_array))

    # Identify all top-performing students (handles ties accurately)
    # Using a small tolerance (1e-9) to handle floating-point precision
    top_mask = np.isclose(averages_array, highest_average, atol=1e-9)
    top_df = df_results[top_mask]
    top_students = top_df[['Student_ID', 'Name', 'Department', 'Total', 'Average', 'Grade', 'Status']].to_dict('records')

    # Grade distribution counts for all grades A, B, C, D, F
    raw_grade_counts = df_results['Grade'].value_counts().to_dict()
    grade_counts = {g: int(raw_grade_counts.get(g, 0)) for g in ['A', 'B', 'C', 'D', 'F']}

    return {
        'total_students': total_students,
        'passed_students': passed_students,
        'failed_students': failed_students,
        'pass_percentage': pass_percentage,
        'class_average': class_average,
        'highest_average': highest_average,
        'lowest_average': lowest_average,
        'top_students': top_students,
        'grade_counts': grade_counts
    }


# =====================================================================
# D. SUBJECT-WISE ANALYSIS
# =====================================================================

def get_subject_statistics(df):
    """
    Calculates detailed statistics for each of the five subjects:
        - Average marks
        - Highest mark
        - Lowest mark
        - Number of students scoring at least 35 (pass count)
    
    Identifies best-performing and lowest-performing subject(s),
    handling ties using unrounded numerical comparisons.
    """
    if df is None or df.empty:
        return {
            'error': 'Cannot compute subject statistics: No student records available.',
            'subjects': {},
            'best_subjects': [],
            'lowest_subjects': []
        }

    subjects_stats = {}
    subject_averages = {}

    for subject in SUBJECT_COLUMNS:
        if subject in df.columns:
            marks_array = df[subject].to_numpy(dtype=float)
            avg_mark = float(np.mean(marks_array))
            highest_mark = float(np.max(marks_array))
            lowest_mark = float(np.min(marks_array))
            passing_students = int(np.sum(marks_array >= 35.0))

            subjects_stats[subject] = {
                'average': avg_mark,
                'highest': highest_mark,
                'lowest': lowest_mark,
                'passed_count': passing_students
            }
            subject_averages[subject] = avg_mark

    # Identify best and lowest performing subjects (handles ties using unrounded values)
    max_avg = max(subject_averages.values())
    min_avg = min(subject_averages.values())

    best_subjects = [s for s, avg in subject_averages.items() if np.isclose(avg, max_avg, atol=1e-9)]
    lowest_subjects = [s for s, avg in subject_averages.items() if np.isclose(avg, min_avg, atol=1e-9)]

    return {
        'subjects': subjects_stats,
        'best_subjects': best_subjects,
        'best_average': max_avg,
        'lowest_subjects': lowest_subjects,
        'lowest_average': min_avg
    }


# =====================================================================
# E. STUDENT SEARCH AND FILTERING
# =====================================================================

def search_student_by_id(df_results, student_id):
    """
    Searches for a student by Student_ID (case-insensitive and trimmed).
    Returns a dictionary of student details if found, or None if not found.
    """
    if df_results is None or df_results.empty or not student_id:
        return None

    clean_id = str(student_id).strip().upper()
    match = df_results[df_results['Student_ID'].astype(str).str.strip().str.upper() == clean_id]

    if not match.empty:
        return match.iloc[0].to_dict()
    return None


def filter_passed_students(df_results):
    """
    Returns a DataFrame containing only students who passed (Status == 'Pass').
    """
    if df_results is None or df_results.empty:
        return pd.DataFrame()
    return df_results[df_results['Status'] == 'Pass'].copy()


def filter_failed_students(df_results):
    """
    Returns a DataFrame containing only students who failed (Status == 'Fail').
    """
    if df_results is None or df_results.empty:
        return pd.DataFrame()
    return df_results[df_results['Status'] == 'Fail'].copy()


def get_top_students(df_results):
    """
    Returns a DataFrame containing all students tied for the highest average mark.
    """
    if df_results is None or df_results.empty:
        return pd.DataFrame()
    highest_avg = df_results['Average'].max()
    return df_results[np.isclose(df_results['Average'], highest_avg, atol=1e-9)].copy()


# =====================================================================
# F. FORMATTING AND DISPLAY UTILITIES
# =====================================================================

def format_display_table(df_subset):
    """
    Formats a student results DataFrame into a clean, human-readable table string
    with Average formatted to 2 decimal places for display purposes only.
    """
    if df_subset is None or df_subset.empty:
        return "No records found."

    display_df = df_subset.copy()
    if 'Average' in display_df.columns:
        display_df['Average'] = display_df['Average'].map(lambda x: f"{x:.2f}")

    return display_df.to_string(index=False)
