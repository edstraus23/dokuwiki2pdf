import os, subprocess, sys, shutil, glob, re

# Define your input and output files
#input_file = "html/data/pages/drupal/drupal_dita_pdf.txt"
#output_file = "drupal_dita_pdf.md"

# Path to ditamap in dokuwiki
ditamap = sys.argv[1]
# Path to output the ditamap file with the <code></code> tags stripped out
ditamap_out = sys.argv[2]

# Open the source file for reading and the destination file for writing
with open(ditamap, 'r', encoding='utf-8') as infile, \
     open(ditamap_out, 'w', encoding='utf-8') as outfile:
    
    # Loop through the source file line by line
    for line in infile:
        if "code>" not in line:
            # Write the line directly to the destination file
            outfile.write(line)

with open(ditamap, "r") as file:
    for line in file:
        # Copy the images files to a common location
        if "IMG:" in line and "!--" in line:
            item = line.split(":")
            source_dir = item[2]
            destination_dir = item[3]

            # Ensure the destination folder exists before copying
            os.makedirs(destination_dir, exist_ok=True)

            # Find all files with an extension inside the source directory (*.*)
            # Change to "/**/*.*" and add recursive=True if you want to search subfolders too
            files_to_copy = glob.glob(os.path.join(source_dir, "*.*"))

            for file_path in files_to_copy:
                if os.path.isfile(file_path):  # Double-check it's a file, not a folder
                    shutil.copy(file_path, destination_dir)

            print(f"Copied {len(files_to_copy)} files to {destination_dir}")
        # Convert the dokuwiki files to markdown files
        if "DW:" in line and "!--" in line:
            #print(line.strip())
            item = line.split(":")
            #print(f"{item[1]}  {item[2]} {item[3]}")
            input_file=item[2] + "/" + item[3] + ".txt"
            output_file="topics/" + item[3] + ".md"

            print(f"Input file: {input_file}")
            print(f"Output file: {output_file}")

            
            # Construct the Docker command
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{subprocess.list2cmdline([subprocess.os.getcwd()])}:/data",
                "pandoc/core",
                "-f", "dokuwiki",
                "-t", "markdown",
                input_file,
                "-o", output_file
            ]
           
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("Conversion successful!")
            else:
                print("Error:", result.stderr)
        if "DV:" in line and "!--" in line:
            item = line.split(":")
            #print(f"JJJ0 {item[1]}  {item[2]} {item[3]}")
            input_file=item[2] + "/" + item[3] + ".txt"
            output_file="topics/" + item[3] + ".ditaval"

            with open(input_file, 'r', encoding='utf-8') as infile, \
                open(output_file, 'w', encoding='utf-8') as outfile:
                
                # Loop through the source file line by line
                for line in infile:
                    if "code>" not in line:
                        # Write the line directly to the destination file
                        outfile.write(line)
        if "THM:" in line and "!--" in line:
            item = line.split(":")
            #print(f"JJJ0 {item[1]}  {item[2]} {item[3]}")
            input_file=item[2] + "/" + item[3] + ".txt"
            output_file="topics/" + item[3] + ".yml"

            with open(input_file, 'r', encoding='utf-8') as infile, \
                open(output_file, 'w', encoding='utf-8') as outfile:
                
                # Loop through the source file line by line
                for line in infile:
                    if "code>" not in line:
                        # Write the line directly to the destination file
                        outfile.write(line)
        if "DT:" in line and "!--" in line:
            item = line.split(":")
            input_file=item[2] + "/" + item[3] + ".txt"
            output_file="topics/" + item[3] + ".dita"

            with open(input_file, 'r', encoding='utf-8') as infile, \
                open(output_file, 'w', encoding='utf-8') as outfile:
                
                # Loop through the source file line by line
                for line in infile:
                    if "code>" not in line:
                        # Write the line directly to the destination file
                        outfile.write(line)

directory_path = "topics"

#Perform cleanup

# Matches only text files in the target directory
search_pattern = os.path.join(directory_path, "*.md")

for file_path in glob.glob(search_pattern):
    print(f"Processing text file: {file_path}")

    # Step 1: Read the file contents
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Step 2: Overwrite the file with modified content
    with open(file_path, "w") as file:
        for line in lines:
            # Example: Replace the word 'old' with 'new'
            #print(line)
            
            # remove leading /
            updated_line = line.replace("png](/", "png](")
            updated_line = updated_line.replace("jpg](/", "jpg](")
            updated_line = updated_line.replace("jpeg](/", "jpeg](")
            # remove top-level directory (flat file structure for md topics). Update as needed.
            if "](" in updated_line and "png" not in updated_line and "jpg" not in updated_line and "jpeg" not in updated_line:
                updated_line = updated_line.replace("](/drupal/", "](")
                updated_line = updated_line.replace("](/docker/", "](")
                updated_line = updated_line.replace("](/ubuntu/", "](")
                updated_line = updated_line.replace(")", ".md)")
            
            file.write(updated_line)
            
        

