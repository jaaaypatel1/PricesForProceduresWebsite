import json

def reformat_hospital_data(input_file, output_file):
    """
    Processes a JSON file containing hospital data.
    Groups charges under the correct hospital and removes redundancy.
    """
    with open(input_file, 'r') as file:
        data = json.load(file)

    hospitals = {}

    # Ensure the input JSON is a list
    if isinstance(data, list):
        for hospital_data in data:
            hospital_name = hospital_data.get("hospital_name", "").strip()
            hospital_address = hospital_data.get("hospital_address", "").strip()
            hospital_key = f"{hospital_name} - {hospital_address}"

            # Initialize hospital entry if it doesn't exist
            if hospital_key not in hospitals:
                hospitals[hospital_key] = {
                    "name": hospital_name,
                    "addr": hospital_address,
                    "charges": []
                }

            # Extract charge information
            charge_entry = {
                "desc": hospital_data.get("description", "").strip(),
                "cost": hospital_data.get("gross_charge"),
                "discounted": hospital_data.get("discounted_cash")
            }

            # Remove empty values to keep JSON compact
            charge_entry = {k: v for k, v in charge_entry.items() if v is not None}

            # Add charge to the hospital's charge list
            if charge_entry:
                hospitals[hospital_key]["charges"].append(charge_entry)

    # Convert dictionary to a list
    output_data = list(hospitals.values())

    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)


# Main execution
input_file = input("Enter the input file name: ").strip()
output_file = input_file.replace(".json", "_optimized.json")

reformat_hospital_data(input_file, output_file)
