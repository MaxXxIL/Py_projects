import json

# Read the single-line JSON file
with open("D:\\Clean Data evaluation\\Visual Layer\\Stat Report\\new\\metadata.json", 'r') as file:
    data = json.load(file)

# Write the formatted JSON to a new file
with open("D:\\Clean Data evaluation\\Visual Layer\\Stat Report\\new\\metadata_fix.json", 'w') as file:
    json.dump(data, file, indent=4)