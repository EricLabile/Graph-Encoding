import os

input_dir = '/mnt/main/outputs/'
output_dir = '/mnt/main/outputs_after/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to process a single file
def process_file(input_file_path, output_dir):
    with open(input_file_path, 'r') as file:
        content = file.read()

    # Split content into chunks separated by double newlines
    chunks = content.split('\n\n')

    # Process each chunk to extract the message after the last "A:"
    extracted_messages = []
    for chunk in chunks:
        lines = chunk.split('\n')
        last_message = None
        for line in lines:
            if line.strip().startswith("A:"):
                last_message = line.strip().split("A:")[-1].strip()
        if last_message:
            extracted_messages.append(last_message)

    # Write the extracted messages to a single output file
    base_filename = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_dir, f"{base_filename}_extracted.txt")
    with open(output_file_path, 'w') as output_file:
        for message in extracted_messages:
            output_file.write(message + '\n')

# Function to read lines from a file and remove text after the first period
def remove_text_after_period(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if '.' in line:
            modified_line = line.split('.')[0] + '.'
        else:
            modified_line = line
        modified_lines.append(modified_line)

    with open(file_path, 'w') as file:
        for line in modified_lines:
            file.write(line + '\n')

# Function to remove all blank lines from a file
def remove_blank_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    non_blank_lines = [line for line in lines if line.strip()]

    with open(file_path, 'w') as file:
        for line in non_blank_lines:
            file.write(line + '')

# Process each file in the input directory
for filename in os.listdir(input_dir):
    print(f"Processing file: {filename}")
    input_file_path = os.path.join(input_dir, filename)
    if os.path.isfile(input_file_path):
        process_file(input_file_path, output_dir)
        output_file_path = os.path.join(output_dir, f"{filename}_extracted.txt")
        remove_text_after_period(output_file_path)
        remove_blank_lines(output_file_path)