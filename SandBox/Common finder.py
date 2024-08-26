
import openpyxl
from collections import defaultdict
import csv

def load_sheet_to_dict(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    sheet = workbook[sheet_name]
    data = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming first row is header
        image, label = row
        data[image] = label
    return data

def compare_labels(dict1, dict2):
    total_count = len(dict1)
    match_count = 0
    label_counts = defaultdict(lambda: {"match": 0, "total": 0})

    for image, label1 in dict1.items():
        label_counts[label1]["total"] += 1
        if image in dict2:
            label2 = dict2[image]
            if label1 == label2:
                match_count += 1
                label_counts[label1]["match"] += 1

    return match_count, total_count, label_counts

def save_to_csv(label_counts, total_accuracy, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Label', 'Matched Count', 'Total Count', 'Accuracy'])  # Header
        for label, counts in label_counts.items():
            accuracy = counts["match"] / counts["total"] if counts["total"] > 0 else 0
            writer.writerow([
                label,
                counts["match"],
                counts["total"],
                f"{accuracy:.2%}"
            ])
        writer.writerow(['Total', '', '', f"{total_accuracy:.2%}"])

def calculate_total_accuracy(label_counts):
    total_match = sum(counts["match"] for counts in label_counts.values())
    total_images = sum(counts["total"] for counts in label_counts.values())
    return total_match / total_images if total_images > 0 else 0


def main():
    file_path = 'D:\\Clean Data evaluation\\CleanLab\\KYEC Test\\Labels compare.xlsx'  # Replace with your file path
    sheet1_name = 'Operator labels'  # Replace with your first sheet name
    sheet2_name = 'Org labels'  # Replace with your second sheet name
    output_csv = 'D:\\Clean Data evaluation\\CleanLab\\KYEC Test\\analysis.csv'  # Name of the output CSV file

    dict1 = load_sheet_to_dict(file_path, sheet1_name)
    dict2 = load_sheet_to_dict(file_path, sheet2_name)

    match_count, total_count, label_counts = compare_labels(dict1, dict2)
    total_accuracy = calculate_total_accuracy(label_counts)

    print(f"Total images in {sheet1_name}: {total_count}")
    print(f"Images with matching labels in both sheets: {match_count}")
    print(f"Total accuracy: {total_accuracy:.2%}")

    print(f"\nAccuracy by label:")
    for label, counts in label_counts.items():
        accuracy = counts["match"] / counts["total"] if counts["total"] > 0 else 0
        print(f"  {label}: {accuracy:.2%} ({counts['match']}/{counts['total']})")

    # Save results to CSV
    save_to_csv(label_counts, total_accuracy, output_csv)
    print(f"\nResults have been saved to {output_csv}")

if __name__ == "__main__":
    main()