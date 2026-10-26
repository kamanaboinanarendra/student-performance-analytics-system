"""
main.py - Student Performance Analytics System
=============================================
Command-line interface and menu execution for student performance analysis.
Built with Python, NumPy, and Pandas.
"""

import os
import sys
import functions


def get_dataset_path():
    """
    Locates the students.csv file in the current working directory
    or in the directory where this script is located.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(script_dir, 'students.csv')
    cwd_path = os.path.join(os.getcwd(), 'students.csv')

    if os.path.exists(cwd_path):
        return cwd_path
    elif os.path.exists(local_path):
        return local_path
    else:
        return 'students.csv'


def print_header(title):
    """Prints a styled header for readability."""
    width = 75
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def display_table(df_subset, title=None):
    """Displays a DataFrame in a clean, tabular format with formatted averages."""
    if title:
        print(f"\n--- {title} ---")
    if df_subset is None or df_subset.empty:
        print("No records found matching this criterion.")
        return

    table_str = functions.format_display_table(df_subset)
    print(table_str)
    print(f"Total records displayed: {len(df_subset)}")


def handle_search(results_df):
    """Handles searching for a student by ID."""
    print("\n--- Search Student by ID ---")
    student_id = input("Enter Student ID to search (e.g., STD101): ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    record = functions.search_student_by_id(results_df, student_id)
    if record is None:
        print(f"No student record found with Student ID '{student_id}'.")
        return

    print("\nStudent Record Found:")
    print("-" * 45)
    print(f"  Student ID    : {record['Student_ID']}")
    print(f"  Name          : {record['Name']}")
    print(f"  Department    : {record['Department']}")
    print(f"  Attendance    : {record['Attendance']}%")
    print("-" * 45)
    print("  Subject Marks :")
    for subj in functions.SUBJECT_COLUMNS:
        status_flag = "Pass" if record[subj] >= 35 else "Fail"
        print(f"    - {subj:<12}: {record[subj]:>5.1f}  [{status_flag}]")
    print("-" * 45)
    print(f"  Total Marks   : {record['Total']:.1f} / 500.0")
    print(f"  Average Marks : {record['Average']:.2f}")
    print(f"  Grade         : {record['Grade']}")
    print(f"  Overall Status: {record['Status']}")
    print("-" * 45)


def handle_subject_statistics(results_df):
    """Displays subject-wise analysis and highlights best/lowest subjects."""
    stats = functions.get_subject_statistics(results_df)
    if 'error' in stats:
        print(stats['error'])
        return

    print("\n--- Subject-Wise Performance Statistics ---")
    header = f"{'Subject':<14}{'Average':>10}{'Highest':>10}{'Lowest':>10}{'Passed Count':>15}"
    print(header)
    print("-" * len(header))

    for subj, data in stats['subjects'].items():
        print(
            f"{subj:<14}"
            f"{data['average']:>10.2f}"
            f"{data['highest']:>10.1f}"
            f"{data['lowest']:>10.1f}"
            f"{data['passed_count']:>15}"
        )

    print("-" * len(header))
    best_list = ", ".join(stats['best_subjects'])
    lowest_list = ", ".join(stats['lowest_subjects'])
    print(f"Best-Performing Subject(s)  : {best_list} (Average: {stats['best_average']:.2f})")
    print(f"Lowest-Performing Subject(s): {lowest_list} (Average: {stats['lowest_average']:.2f})")


def handle_class_statistics(results_df):
    """Displays comprehensive class statistics and distributions."""
    stats = functions.get_class_statistics(results_df)
    if 'error' in stats:
        print(stats['error'])
        return

    print("\n--- Overall Class Performance Statistics ---")
    print(f"  Total Students Enrolled : {stats['total_students']}")
    print(f"  Passed Students         : {stats['passed_students']}")
    print(f"  Failed Students         : {stats['failed_students']}")
    print(f"  Overall Pass Percentage : {stats['pass_percentage']:.2f}%")
    print(f"  Class Average Marks     : {stats['class_average']:.2f}")
    print(f"  Highest Student Average : {stats['highest_average']:.2f}")
    print(f"  Lowest Student Average  : {stats['lowest_average']:.2f}")

    print("\n  Top-Performing Student(s):")
    for s in stats['top_students']:
        print(f"    * {s['Student_ID']} - {s['Name']} ({s['Department']}): "
              f"Avg = {s['Average']:.2f}, Total = {s['Total']:.1f}, Grade = {s['Grade']}")

    print("\n  Grade Distribution:")
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = stats['grade_counts'].get(grade, 0)
        percentage = (count / stats['total_students']) * 100.0 if stats['total_students'] > 0 else 0.0
        bar = "#" * count
        print(f"    Grade {grade}: {count:>2} student(s) ({percentage:>5.1f}%)  {bar}")


def main():
    """Main program entry point."""
    print_header("STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("Initializing application and loading dataset...\n")

    csv_path = get_dataset_path()
    raw_df, errors = functions.load_dataset(csv_path)

    if errors:
        print("ERROR: Failed to validate dataset. Cannot start application.")
        print("-" * 60)
        for err in errors:
            print(f"  [X] {err}")
        print("-" * 60)
        print("Please resolve the dataset issues before running the program.")
        sys.exit(1)

    # Dataset loaded and validated successfully
    rows, cols = raw_df.shape
    print(f"[OK] Dataset successfully loaded from: {csv_path}")
    print(f"[OK] Dataset dimensions: {rows} student records, {cols} columns.")

    print("\nInitial Baseline Dataset Preview:")
    print(raw_df.head(5).to_string(index=False))
    if rows > 5:
        print(f"... and {rows - 5} more records.")

    # Calculate student results (Total, Average, Grade, Status)
    # The original CSV and raw_df remain completely unmodified.
    results_df = functions.add_student_results(raw_df)
    print("\n[OK] Performance metrics calculated successfully.")

    # Interactive Menu Loop
    while True:
        print_header("MAIN MENU")
        print("1. Display all student records")
        print("2. Search for a student by ID")
        print("3. Display passed students")
        print("4. Display failed students")
        print("5. Display top-performing students")
        print("6. Display subject-wise statistics")
        print("7. Display overall class statistics")
        print("8. Exit the program")
        print("=" * 75)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            display_table(results_df, "All Student Performance Records")

        elif choice == '2':
            handle_search(results_df)

        elif choice == '3':
            passed_df = functions.filter_passed_students(results_df)
            display_table(passed_df, "Passed Students (All Subjects >= 35)")

        elif choice == '4':
            failed_df = functions.filter_failed_students(results_df)
            display_table(failed_df, "Failed Students (One or More Subjects < 35)")

        elif choice == '5':
            top_df = functions.get_top_students(results_df)
            display_table(top_df, "Top-Performing Student(s) (Highest Average Marks)")

        elif choice == '6':
            handle_subject_statistics(results_df)

        elif choice == '7':
            handle_class_statistics(results_df)

        elif choice == '8':
            print("\nThank you for using Student Performance Analytics System. Goodbye!")
            break

        else:
            print("\n[!] Invalid selection. Please enter a valid number between 1 and 8.")


if __name__ == '__main__':
    main()
