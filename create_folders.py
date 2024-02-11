import openpyxl
import os
import octk

# Path to the Excel file
input_excel_file_path = 'bot_data.xlsx'

# Output directory
# output_dir = octk.uniquify('test/outputs/output')
output_dir = r'C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj-FCT'

# Load the workbook
workbook = openpyxl.load_workbook(input_excel_file_path)

# Select the active sheet
sheet = workbook.active


# Iterate over each row in the sheet
for row in sheet.iter_rows(min_row=2, values_only=True):
    bot_id, bot_name = row[0], row[3]
    folder_name = f'{bot_id}-{bot_name.replace(" ", "_")}'

    # Create the folder
    os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)
