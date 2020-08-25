import os
import shutil
import zipfile
# Open a file
zip_location = "C:\\Box\\Temp\\Market Data\\"

with os.scandir(zip_location) as dirs:
    for entry in dirs:
        file_name = entry.name
        full_file_name = os.path.join(zip_location, file_name)
        if os.path.isfile(full_file_name):
            # unzip file & rename csv to concur_output.csv
            with zipfile.ZipFile("./concur_zip.zip", 'r') as zip_ref:
                zip_ref.extractall(location)

            for file_name in os.listdir(location):
                if file_name.endswith('.csv'):
                    os.rename(location + file_name, location + "concur_report.csv")
                else:
                    os.remove(location + file_name)

            shutil.copy(full_file_name, zip_location + file_name)