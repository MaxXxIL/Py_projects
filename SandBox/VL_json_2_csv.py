import json
import csv
import sys


def extract_object_label_metadata(media_item, object_label):
    result = {
        "file_name": media_item['file_name'],
        "media_id": media_item['media_id'],
        "category_name": "",
        "bbox": "",
        "object_url": "",
        "issue": "",
        "confidence": "",
        "description": ""
    }

    props = object_label.get('properties', {})
    result['category_name'] = props.get('category_name', '')
    result['bbox'] = json.dumps(props.get('bbox', []))
    result['object_url'] = props.get('url', '')

    # Process nested metadata items (issues)
    issues = []
    confidences = []
    descriptions = []
    for issue in props.get('metadata_items', []):
        if issue.get('type') == 'issue':
            issue_props = issue.get('properties', {})
            issue_type = issue_props.get('issue_type', '')
            issues.append(issue_type)
            confidences.append(str(issue_props.get('confidence', '')))
            descriptions.append(issue_props.get('issues_description', ''))

    result['issue'] = ';'.join(issues)
    result['confidence'] = ';'.join(confidences)
    result['description'] = ';'.join(descriptions)

    return result


def json_to_csv(json_file, csv_file):
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Prepare the CSV data
    csv_data = []
    for media_item in data['media_items']:
        for metadata_item in media_item['metadata_items']:
            if metadata_item.get('type') == 'object_label':
                row = extract_object_label_metadata(media_item, metadata_item)
                csv_data.append(row)

    # Define the fieldnames in the desired order
    fieldnames = [
        "file_name", "media_id", "category_name", "bbox", "object_url",
        "issue", "confidence", "description"
    ]

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in csv_data:
            writer.writerow(item)

if __name__ == "__main__":


    json_file = "D:\\Clean Data evaluation\\Visual Layer\\Stat Report\\new\\metadata.json"
    csv_file = "D:\\Clean Data evaluation\\Visual Layer\\Stat Report\\new\\metadata.csv"

    json_to_csv(json_file, csv_file)
    print(f"Conversion complete. CSV file saved as {csv_file}")