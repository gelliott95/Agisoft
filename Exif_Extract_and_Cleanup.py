# This was generated to extract exif data from Autel Evo II Pro images to a file (out.csv)
# The elevation on the Autel images is in Elipsoid meters
# Geoid height can be subtracted from the Elipsoid to get Orthometric
# Geoid offset can be found for project area here:
# https://www.unavco.org/software/geodetic-utilities/geoid-height-calculator/geoid-height-calculator.html
# Enter geoid offset as is (can be negative) and the script will convert GPSAltitude from elpisoid to orthometric height 
# Assumes project folder contains a ref folder (out.csv destination) and *FTASK folder containing images
# Example C:\Agisoft_Data\Autel Test\Flight 2\ref and C:\Agisoft_Data\Autel Test\Flight 2\109FTASK
# Both /ref and /109FTASK are existing folders before running script

#Wish List: different geoid offsets for different flights

import os
import subprocess
import csv
import shutil

base_dir = r'C:/Example/Directory' # Parent directory of the project for all flights of interest
geoid_offset_value = -00.00 # Enter the geoid offset for the area of flight in meters (can be negative)

for root, dirs, files in os.walk(base_dir):
    for dir in dirs:
        if "FTASK" in dir:
            folder_path = os.path.join(root, dir)
            flight_folder = os.path.join(root, 'ref')
            output_csv = os.path.join(flight_folder, 'out.csv')

            exiftool_command = [
                'exiftool', '-csv', '-r', '-n', '-a', '-u', '-s',
                '-GPSLongitude', '-GPSLatitude', '-GPSAltitude', '-T', '-ext', 'jpg',
                folder_path
            ]

            print(f"Processing: {folder_path}")

            if not os.path.exists(flight_folder):
                os.makedirs(flight_folder, exist_ok=True)

            with open(output_csv, 'w') as output_file:
                subprocess.run(exiftool_command, stdout=output_file, text=True)
                print(f"Processed: {folder_path}")

            # CSV processing (second script) applied to the created out.csv
            input_csv = output_csv
            if os.path.exists(input_csv) and os.path.getsize(input_csv) > 0:
                temp_csv = r"temp_input.csv"

                with open(input_csv, 'r') as input_file, open(temp_csv, 'w', newline='') as temp_file:
                    csv_reader = csv.reader(input_file)
                    csv_writer = csv.writer(temp_file)

                    header = next(csv_reader)
                    csv_writer.writerow(header)

                    # Determine the index of the 'GPSAltitude' column
                    altitude_index = header.index('GPSAltitude')

                    for row in csv_reader:
                        try:
                            row[header.index('SourceFile')] = "MAX" + row[header.index('SourceFile')].split("MAX", 1)[1]
                            gps_altitude = float(row[altitude_index])
                            row[altitude_index] = str(gps_altitude - geoid_offset_value)  # Subtract the value from GPSAltitude
                            csv_writer.writerow(row)
                        except ValueError:
                            # Handle cases where the value cannot be converted to a float
                            csv_writer.writerow(row)  # Write the row as is

                shutil.move(temp_csv, input_csv)
                print("CSV processing completed")
            else:
                print("Input CSV file does not exist or is empty.")

print("Processing completed.")
