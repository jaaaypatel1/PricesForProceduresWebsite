import json

def reformat_hospital_data(input_file, output_file):
    """
    Processes a JSON file containing hospital data. Handles cases where the input is a list.
    Reformats data to include hospital name and address as a single string for each item.
    """
    # Read the input JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Ensure the input JSON is a dictionary or handle the first element if it's a list
    if isinstance(data, list):
        data = data[0]  # Assume hospital data is in the first element of the list
    
    # Extract hospital information
    hospital_name = data.get("hospital_name", "")
    hospital_address_list = list(set(data.get("hospital_address", [])))  # Deduplicate addresses
    hospital_address = "; ".join(hospital_address_list)  # Combine into a single string
    
    # Process the items
    items = []
    for item in data.get("standard_charge_information", []):
        for charge in item.get("standard_charges", []):
            items.append({
                "hospital_name": hospital_name,
                "hospital_address": hospital_address,
                "description": item.get("description", ""),
                "gross_charge": charge.get("gross_charge", None),
                "discounted_cash": charge.get("discounted_cash", None),
                "billing_class": charge.get("billing_class", ""),
                "notes": charge.get("additional_generic_notes", ""),
                "gross_charge_types": charge.get("setting", "")
            })
    
    # Write the formatted data to the output JSON file
    with open(output_file, 'w') as file:
        json.dump(items, file, indent=4)

# Main execution
input_file = input("Enter the input file name: ").strip()
# Remove the .json extension so it can be used later
new_file_name = input_file.replace(".json", "")
output_file = new_file_name + "_formatted.json"

# Run the function
reformat_hospital_data(input_file, output_file)

print(f"Formatted data has been written to {output_file}")
