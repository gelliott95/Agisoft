#Grant Elliott-6/17/24
#Combines all nav (.24l, .24n, .24e and .24g) files into one .nav file
#Change file extension to .pyw and run with python to run with double click

import os
import tkinter as tk
from tkinter import filedialog, messagebox

def combine_files_to_nav(directory):
    # Find all unique base filenames (excluding extensions)
    base_filenames = set(
        os.path.splitext(filename)[0] for filename in os.listdir(directory)
        if filename.endswith(('.24n', '.24l', '.24g', '.24e'))
    )

    for base_name in base_filenames:
        extensions = ['.24n', '.24l', '.24g', '.24e']
        combined_filename = os.path.join(directory, base_name + '.nav')

        header_lines = ['', '', '', '', '', '', '', '']
        time_system_corr_lines = []

        try:
            # Process the .24n file to get header lines 1, 2, 4, and 5, and its time system correction line
            with open(os.path.join(directory, base_name + '.24n'), 'r') as file_24n:
                lines = file_24n.readlines()
                header_lines[0] = lines[0]  # Line ending with RINEX VERSION / TYPE
                header_lines[1] = lines[1]  # Line ending with PGM / RUN BY / DATE
                time_system_corr_lines.append(lines[2])  # Line ending with TIME SYSTEM CORR
                header_lines[6] = lines[3]  # Line ending with LEAP SECONDS
                header_lines[7] = lines[4]  # Line denoted by END OF HEADER

            # Process the other files to get their time system correction lines
            for ext in extensions[1:]:
                file_path = os.path.join(directory, base_name + ext)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        time_system_corr_lines.append(lines[2])  # Line ending with TIME SYSTEM CORR
                else:
                    print(f"Warning: {file_path} does not exist and will be skipped.")

            # Insert the time system correction lines into the header
            for i, line in enumerate(time_system_corr_lines):
                header_lines[2 + i] = line

            # Write the combined .nav file with the new header
            with open(combined_filename, 'w') as combined_file:
                combined_file.writelines(header_lines)

                # Append the rest of the content from each file
                for ext in extensions:
                    file_path = os.path.join(directory, base_name + ext)
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as input_file:
                            content_lines = input_file.readlines()[5:]  # Skip the first 5 header lines
                            combined_file.writelines(content_lines)

            print(f"Combined file created: {combined_filename}")
        except Exception as e:
            print(f"An error occurred for {base_name}: {e}")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        combine_files_to_nav(directory)
        messagebox.showinfo("Success", "Files combined successfully.")

# GUI Setup
root = tk.Tk()
root.title("Combine RINEX Files")

canvas = tk.Canvas(root, height=200, width=400)
canvas.pack()

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.5, anchor='center')

button = tk.Button(frame, text="Select Directory and Combine Files", command=select_directory)
button.pack()

root.mainloop()

