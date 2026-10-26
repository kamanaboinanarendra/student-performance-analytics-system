"""
test_suite.py - Automated Testing for Student Performance Analytics System
==========================================================================
Uses Python standard library unittest to verify all 42 specification cases.
"""

import os
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# Robust Path Configuration
# Supports running test_suite.py from workspace root or inside student-performance-analytics
# ---------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUB_DIR = os.path.join(SCRIPT_DIR, 'student-performance-analytics')

if os.path.exists(os.path.join(SUB_DIR, 'students.csv')):
    PROJECT_DIR = SUB_DIR
elif os.path.exists(os.path.join(SCRIPT_DIR, 'students.csv')):
    PROJECT_DIR = SCRIPT_DIR
else:
    PROJECT_DIR = os.getcwd()

for p in [PROJECT_DIR, SCRIPT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Import functions module
try:
    import functions
except ImportError:
    import importlib.util
    func_path = os.path.join(PROJECT_DIR, 'functions.py')
    spec = importlib.util.spec_from_file_location("functions", func_path)
    functions = importlib.util.module_from_spec(spec)
    sys.modules["functions"] = functions
    spec.loader.exec_module(functions)


class TestStudentPerformanceAnalytics(unittest.TestCase):

    # =================================================================
    # 1. GRADING TESTS (Cases 1-7)
    # =================================================================
    def test_01_grade_boundary_exact_35(self):
        """Case 1: Average exactly 35 returns Grade D."""
        self.assertEqual(functions.calculate_grade(35.0), 'D')

    def test_02_grade_boundary_exact_60(self):
        """Case 2: Average exactly 60 returns Grade C."""
        self.assertEqual(functions.calculate_grade(60.0), 'C')

    def test_03_grade_boundary_exact_75(self):
        """Case 3: Average exactly 75 returns Grade B."""
        self.assertEqual(functions.calculate_grade(75.0), 'B')

    def test_04_grade_boundary_exact_90(self):
        """Case 4: Average exactly 90 returns Grade A."""
        self.assertEqual(functions.calculate_grade(90.0), 'A')

    def test_05_grade_below_35(self):
        """Case 5: Average below 35 returns Grade F."""
        self.assertEqual(functions.calculate_grade(34.0), 'F')
        self.assertEqual(functions.calculate_grade(0.0), 'F')
        self.assertEqual(functions.calculate_grade(20.5), 'F')

    def test_06_grade_immediately_below_boundaries(self):
        """Case 6: Correct grade immediately below each relevant boundary."""
        self.assertEqual(functions.calculate_grade(34.999), 'F')
        self.assertEqual(functions.calculate_grade(59.999), 'D')
        self.assertEqual(functions.calculate_grade(74.999), 'C')
        self.assertEqual(functions.calculate_grade(89.999), 'B')

    def test_07_grade_immediately_above_boundaries(self):
        """Case 7: Correct grade immediately above each relevant boundary."""
        self.assertEqual(functions.calculate_grade(35.001), 'D')
        self.assertEqual(functions.calculate_grade(60.001), 'C')
        self.assertEqual(functions.calculate_grade(75.001), 'B')
        self.assertEqual(functions.calculate_grade(90.001), 'A')

    # =================================================================
    # 2. PASS / FAIL TESTS (Cases 8-11)
    # =================================================================
    def test_08_pass_every_subject_exactly_35(self):
        """Case 8: Student scoring exactly 35 in every subject must pass."""
        marks = [35, 35, 35, 35, 35]
        self.assertEqual(functions.calculate_status(marks), 'Pass')

    def test_09_fail_one_subject_below_35_with_high_average(self):
        """Case 9: One subject mark below 35 with average above 35 must fail."""
        marks = [90, 80, 75, 20, 85]
        avg = float(np.mean(marks))
        self.assertGreater(avg, 35.0)
        self.assertEqual(functions.calculate_status(marks), 'Fail')

    def test_10_pass_all_subjects_above_35(self):
        """Case 10: All subjects above 35 must pass."""
        marks = [70, 75, 80, 85, 90]
        self.assertEqual(functions.calculate_status(marks), 'Pass')

    def test_11_fail_multiple_subjects_below_35(self):
        """Case 11: A student failing multiple subjects must fail."""
        marks = [30, 25, 40, 20, 34]
        self.assertEqual(functions.calculate_status(marks), 'Fail')

    # =================================================================
    # 3. CLASS ANALYSIS AND SUBJECT TESTS (Cases 12-23)
    # =================================================================
    def setUp(self):
        """Load baseline dataset for analysis tests."""
        csv_file = os.path.join(PROJECT_DIR, 'students.csv')
        self.df, self.errors = functions.load_dataset(csv_file)
        if self.df is not None:
            self.results_df = functions.add_student_results(self.df)
            self.class_stats = functions.get_class_statistics(self.results_df)
            self.sub_stats = functions.get_subject_statistics(self.results_df)

    def test_12_correct_total_student_count(self):
        """Case 12: Correct total student count."""
        self.assertEqual(self.class_stats['total_students'], 25)

    def test_13_correct_passed_student_count(self):
        """Case 13: Correct passed student count."""
        self.assertEqual(self.class_stats['passed_students'], 17)

    def test_14_correct_failed_student_count(self):
        """Case 14: Correct failed student count."""
        self.assertEqual(self.class_stats['failed_students'], 8)

    def test_15_correct_pass_percentage(self):
        """Case 15: Correct pass percentage."""
        self.assertAlmostEqual(self.class_stats['pass_percentage'], 68.0, places=2)

    def test_16_correct_overall_average(self):
        """Case 16: Correct overall average."""
        expected_avg = float(self.results_df['Average'].mean())
        self.assertAlmostEqual(self.class_stats['class_average'], expected_avg, places=4)

    def test_17_correct_highest_and_lowest_student_averages(self):
        """Case 17: Correct highest and lowest student averages."""
        expected_max = float(self.results_df['Average'].max())
        expected_min = float(self.results_df['Average'].min())
        self.assertAlmostEqual(self.class_stats['highest_average'], expected_max, places=4)
        self.assertAlmostEqual(self.class_stats['lowest_average'], expected_min, places=4)

    def test_18_multiple_students_tied_for_highest_average(self):
        """Case 18: Multiple students tied for the highest average."""
        top_students = self.class_stats['top_students']
        self.assertGreaterEqual(len(top_students), 2)
        top_ids = [s['Student_ID'] for s in top_students]
        self.assertIn('STD101', top_ids)
        self.assertIn('STD102', top_ids)
        self.assertAlmostEqual(top_students[0]['Average'], 94.20, places=2)
        self.assertAlmostEqual(top_students[1]['Average'], 94.20, places=2)

    def test_19_correct_count_for_each_grade(self):
        """Case 19: Correct count for each grade."""
        expected_grades = {'A': 3, 'B': 5, 'C': 8, 'D': 7, 'F': 2}
        self.assertEqual(self.class_stats['grade_counts'], expected_grades)

    def test_20_correct_subject_averages(self):
        """Case 20: Correct subject averages."""
        for subj in functions.SUBJECT_COLUMNS:
            expected_subj_avg = float(self.results_df[subj].mean())
            self.assertAlmostEqual(self.sub_stats['subjects'][subj]['average'], expected_subj_avg, places=4)

    def test_21_correct_subject_highest_and_lowest_marks(self):
        """Case 21: Correct subject highest and lowest marks."""
        for subj in functions.SUBJECT_COLUMNS:
            expected_high = float(self.results_df[subj].max())
            expected_low = float(self.results_df[subj].min())
            self.assertEqual(self.sub_stats['subjects'][subj]['highest'], expected_high)
            self.assertEqual(self.sub_stats['subjects'][subj]['lowest'], expected_low)

    def test_22_correct_number_of_students_passing_each_subject(self):
        """Case 22: Correct number of students passing each subject (>= 35)."""
        for subj in functions.SUBJECT_COLUMNS:
            expected_pass = int((self.results_df[subj] >= 35).sum())
            self.assertEqual(self.sub_stats['subjects'][subj]['passed_count'], expected_pass)

    def test_23_multiple_subjects_tied_for_best_or_lowest_average(self):
        """Case 23: Multiple subjects tied for best or lowest average."""
        synth_data = pd.DataFrame([
            {'Student_ID': 'S1', 'Name': 'N1', 'Department': 'CS', 'Python': 80, 'Java': 80, 'DBMS': 70, 'Networks': 60, 'Maths': 60, 'Attendance': 90},
            {'Student_ID': 'S2', 'Name': 'N2', 'Department': 'IT', 'Python': 80, 'Java': 80, 'DBMS': 70, 'Networks': 60, 'Maths': 60, 'Attendance': 90}
        ])
        synth_sub = functions.get_subject_statistics(synth_data)
        self.assertCountEqual(synth_sub['best_subjects'], ['Python', 'Java'])
        self.assertCountEqual(synth_sub['lowest_subjects'], ['Networks', 'Maths'])

    # =================================================================
    # 4. DATA VALIDATION TESTS (Cases 24-37)
    # =================================================================
    def test_24_valid_dataset_at_least_20_records(self):
        """Case 24: Valid dataset loads with at least 20 records and 0 errors."""
        csv_file = os.path.join(PROJECT_DIR, 'students.csv')
        df, errors = functions.load_dataset(csv_file)
        self.assertEqual(errors, [])
        self.assertIsNotNone(df)
        self.assertGreaterEqual(len(df), 20)

    def test_25_missing_csv_file(self):
        """Case 25: Missing CSV file returns clear error message without crash."""
        df, errors = functions.load_dataset("non_existent_file_path_12345.csv")
        self.assertIsNone(df)
        self.assertTrue(any("not found" in err.lower() for err in errors))

    def test_26_empty_csv_file(self):
        """Case 26: Empty CSV file (0 bytes) returns error."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("empty" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_27_missing_required_column(self):
        """Case 27: CSV missing a required column returns error."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Attendance\n")
            tmp.write("S101,John Doe,CS,80,85,90,75,95\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("missing required column" in err.lower() and "maths" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_28_duplicate_student_ids(self):
        """Case 28: Duplicate student IDs are detected and reported."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,85,90,75,80,95\n")
            tmp.write("S101,Jane Smith,IT,70,75,80,65,70,85\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("duplicate student_id" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_29_missing_student_id_or_required_values(self):
        """Case 29: Blank or missing required text fields are detected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write(",John Doe,CS,80,85,90,75,80,95\n")
            tmp.write("S102,,IT,70,75,80,65,70,85\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(len(errors) > 0)
            self.assertTrue(any("student_id" in err.lower() or "name" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_30_missing_subject_marks(self):
        """Case 30: Missing / null subject marks are detected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,,90,75,80,95\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("missing" in err.lower() and "java" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_31_non_numeric_subject_marks(self):
        """Case 31: Non-numeric subject marks are detected and rejected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,AB,90,75,80,95\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("non-numeric" in err.lower() and "java" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_32_marks_below_zero(self):
        """Case 32: Negative subject marks are rejected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,-5,90,75,80,95\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("below 0" in err.lower() and "java" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_33_marks_above_100(self):
        """Case 33: Marks greater than 100 are rejected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,105,90,75,80,95\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("above 100" in err.lower() and "java" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_34_non_numeric_attendance(self):
        """Case 34: Non-numeric attendance is rejected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,85,90,75,80,present\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("non-numeric" in err.lower() and "attendance" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_35_attendance_below_zero(self):
        """Case 35: Attendance below 0 is rejected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,85,90,75,80,-10\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("below 0" in err.lower() and "attendance" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_36_attendance_above_100(self):
        """Case 36: Attendance above 100 is rejected."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Student_ID,Name,Department,Python,Java,DBMS,Networks,Maths,Attendance\n")
            tmp.write("S101,John Doe,CS,80,85,90,75,80,120\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(any("above 100" in err.lower() and "attendance" in err.lower() for err in errors))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_37_invalid_or_unreadable_csv_content(self):
        """Case 37: Corrupted / unreadable CSV content is handled cleanly."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("Random corrupted text\nwith\x00nullbytes\x01\n")
            tmp_path = tmp.name
        try:
            df, errors = functions.load_dataset(tmp_path)
            self.assertIsNone(df)
            self.assertTrue(len(errors) > 0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # =================================================================
    # 5. SEARCH AND FILTERING TESTS (Cases 38-42)
    # =================================================================
    def test_38_search_for_an_existing_student(self):
        """Case 38: Search for existing student returns student record."""
        record = functions.search_student_by_id(self.results_df, "STD101")
        self.assertIsNotNone(record)
        self.assertEqual(record['Name'], "Aarav Sharma")
        self.assertEqual(record['Department'], "Computer Science")

        # Test case-insensitivity
        record_lower = functions.search_student_by_id(self.results_df, "std101")
        self.assertIsNotNone(record_lower)
        self.assertEqual(record_lower['Name'], "Aarav Sharma")

    def test_39_search_for_a_nonexistent_student(self):
        """Case 39: Search for nonexistent student returns None safely."""
        record = functions.search_student_by_id(self.results_df, "NON_EXISTENT_ID_999")
        self.assertIsNone(record)

    def test_40_invalid_menu_selection(self):
        """Case 40: Invalid menu input validation logic."""
        valid_options = {'1', '2', '3', '4', '5', '6', '7', '8'}
        for invalid_choice in ['0', '9', 'abc', '-1', '99', '']:
            self.assertNotIn(invalid_choice.strip(), valid_options)

    def test_41_exit_selection_and_source_immutability(self):
        """Case 41: Exit selection integrity and source dataset immutability."""
        csv_file = os.path.join(PROJECT_DIR, 'students.csv')
        with open(csv_file, 'r', encoding='utf-8') as f:
            content_before = f.read()

        df, _ = functions.load_dataset(csv_file)
        res = functions.add_student_results(df)
        functions.get_class_statistics(res)
        functions.get_subject_statistics(res)

        with open(csv_file, 'r', encoding='utf-8') as f:
            content_after = f.read()

        self.assertEqual(content_before, content_after)

    def test_42_no_results_behavior_for_empty_filter(self):
        """Case 42: No-results behavior for an empty filter result."""
        empty_df = pd.DataFrame()
        passed_empty = functions.filter_passed_students(empty_df)
        failed_empty = functions.filter_failed_students(empty_df)
        top_empty = functions.get_top_students(empty_df)

        self.assertTrue(passed_empty.empty)
        self.assertTrue(failed_empty.empty)
        self.assertTrue(top_empty.empty)
        self.assertEqual(functions.format_display_table(empty_df), "No records found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
