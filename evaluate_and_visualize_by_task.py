import os
import matplotlib.pyplot as plt
import seaborn as sns


answers_dir = '/mnt/main/answers_new/'
outputs_after_dir = '/mnt/main/outputs_after_new/'

# Function to compare two files line by line and calculate accuracy
def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    if len(lines1) != len(lines2):
        print(f"Files {file1_path} and {file2_path} have different number of lines. We truncate the longer file.")
        min_len = min(len(lines1), len(lines2))
        lines1 = lines1[:min_len]
        lines2 = lines2[:min_len]

    total_lines = len(lines1)
    matching_lines = 0

    for line1, line2 in zip(lines1, lines2):
        if line1.strip() == line2.strip():
            matching_lines += 1

    accuracy = (matching_lines / total_lines) * 100
    print(f"Accuracy between {os.path.basename(file1_path)} and {os.path.basename(file2_path)}: {accuracy:.2f}%")
    return accuracy

# Compare files in the two directories
answer_files = sorted(os.listdir(answers_dir))
output_files = sorted(os.listdir(outputs_after_dir))

accuracies = []

for answer_file, output_file in zip(answer_files, output_files):
    answer_file_path = os.path.join(answers_dir, answer_file)
    output_file_path = os.path.join(outputs_after_dir, output_file)
    if os.path.isfile(answer_file_path) and os.path.isfile(output_file_path):
        accuracy = compare_files(answer_file_path, output_file_path)
        accuracies.append(accuracy)

# Calculate average accuracy every 5 files
# average_accuracies = []
# for i in range(0, len(accuracies), 5):
#     avg_accuracy = sum(accuracies[i:i+5]) / 5
#     average_accuracies.append(avg_accuracy)

# Skip zero_cot files
average_accuracies = []
for i in range(0, len(accuracies), 5):
    # Exclude the 4th file (index 3) in each group of 5
    group = accuracies[i:i+5]
    if len(group) == 5:
        group.pop(3)
    avg_accuracy = sum(group) / len(group)
    average_accuracies.append(avg_accuracy)

# There are altogether 30 files, so the average accuracies list should have 6 elements, whose names are as follows: connected_nodes, cycle_check, edge_count, edge_existence, node_count, node_degree. visualize the average accuracies using a bar plot.

# Plot the results
tasks = ['connected_nodes', 'cycle_check', 'edge_count', 'edge_existence', 'node_count', 'node_degree']
averages = average_accuracies
# Set the style and color palette
sns.set(style="whitegrid")
palette = sns.color_palette("viridis", len(tasks))

plt.figure(figsize=(12, 8))
bars = plt.bar(tasks, averages, color=palette)

# Add labels on top of the bars
for bar, average in zip(bars, averages):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, round(average, 2), ha='center', va='bottom')
yval = bar.get_height()
plt.text(bar.get_x() + bar.get_width()/2, yval + 1, round(average, 2), ha='center', va='bottom')

# Customize the plot
plt.xlabel('Tasks', fontsize=16, labelpad=20)  # Increase labelpad to make the xlabel higher
plt.ylabel('Average Accuracy (%)', fontsize=14)
plt.title('Llama3.1-8B Instruct\'s Reasoning Ability on Graphs', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0, max(averages) + 10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Increase figure size to make 'tasks' labels taller
plt.gcf().set_size_inches(14, 10)

# Add footnote
plt.figtext(0.5, 0.01, 'Note: The graphs are generated using the ER algorithm on a relatively small scale.', 
            wrap=True, horizontalalignment='center', fontsize=10)

# Remove top and right spines
# Remove top and right spines
sns.despine()

# Adjust layout to make the xlabel "Tasks" higher
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure
plt.savefig('average_accuracies.png')