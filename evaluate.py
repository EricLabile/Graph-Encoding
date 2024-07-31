import os

answers_dir = '/mnt/main/answers/'
outputs_after_dir = '/mnt/main/outputs_after/'

# Function to compare two files line by line and calculate accuracy
def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    if len(lines1) != len(lines2):
        print(f"Files {file1_path} and {file2_path} have different number of lines.")
        return

    total_lines = len(lines1)
    matching_lines = 0

    for line1, line2 in zip(lines1, lines2):
        if line1.strip() == line2.strip():
            matching_lines += 1

    accuracy = (matching_lines / total_lines) * 100
    print(f"Accuracy between {os.path.basename(file1_path)} and {os.path.basename(file2_path)}: {accuracy:.2f}%")

# Compare files in the two directories
answer_files = sorted(os.listdir(answers_dir))
output_files = sorted(os.listdir(outputs_after_dir))

for answer_file, output_file in zip(answer_files, output_files):
    answer_file_path = os.path.join(answers_dir, answer_file)
    output_file_path = os.path.join(outputs_after_dir, output_file)
    if os.path.isfile(answer_file_path) and os.path.isfile(output_file_path):
        compare_files(answer_file_path, output_file_path)