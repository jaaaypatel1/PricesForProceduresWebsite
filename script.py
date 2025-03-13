import json
import re

def reformat_hospital_data(input_file, output_file):
    """
    Processes a JSON file containing hospital data.
    Extracts only the 5-digit CPT code if available.
    Groups charges under the correct hospital while ensuring no redundant addresses.
    """
    with open(input_file, 'r') as file:
        data = json.load(file)

    hospitals = {}

    # Ensure the input JSON is a list
    if isinstance(data, list):
        data = data[0] if len(data) == 1 else data  # Handle single-item list case

    hospital_name = data.get("hospital_name", "").strip()
    hospital_addresses = data.get("hospital_address", [])

    # Ensure addresses are in list format
    if not isinstance(hospital_addresses, list):
        hospital_addresses = [hospital_addresses]

    for address in set(hospital_addresses):  # Ensure unique addresses
        hospital_key = f"{hospital_name} - {address}"

        if hospital_key not in hospitals:
            hospitals[hospital_key] = {
                "name": hospital_name,
                "addr": address,
                "charges": []
            }

        # Process charges
        for item in data.get("standard_charge_information", []):
            # Extract the first 5-digit CPT code if available
            cpt_code = None
            for code_entry in item.get("code_information", []):
                if re.fullmatch(r"\d{5}", code_entry["code"]):  # Match exactly 5 digits
                    cpt_code = code_entry["code"]
                    break  # Stop after finding the first 5-digit code

            for charge in item.get("standard_charges", []):
                charge_entry = {
                    "desc": item.get("description", "").strip(),
                    "cpt_code": cpt_code,  # Include only the 5-digit CPT code
                    "cost": charge.get("gross_charge"),
                    "discounted": charge.get("discounted_cash")
                }

                # Remove empty values to keep JSON compact
                charge_entry = {k: v for k, v in charge_entry.items() if v}

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

print(f"Optimized data has been written to {output_file}")
