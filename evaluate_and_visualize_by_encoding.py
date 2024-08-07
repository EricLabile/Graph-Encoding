import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

answers_dir = '/mnt/main/answers_new/'
outputs_after_dir = '/mnt/main/outputs_after_new/'

text_encoders = [
    'adjacency',
    'incident',
    'coauthorship',
    'friendship',
    'south_park',
    'got',
    'social_network',
    'politician',
    'expert',
]

# Function to compare chunks of lines and calculate accuracy
def compare_chunks(answer_lines, output_lines):
    correct = sum(1 for a, b in zip(answer_lines, output_lines) if a.strip() == b.strip())
    total = len(answer_lines)
    return correct

# Initialize accuracy counts for each encoding method
accuracy_counts = [0] * len(text_encoders)

for answer_file in os.listdir(answers_dir):
    # print(answer_file)
    # the file name is in the format edge_count_zero_cot_test_answers.txt
    # if the file name contains zero_cot, skip it

    # if 'zero_cot' in answer_file:
    #     continue
    task_name_match = re.match(r'(\w+)_test_answers.txt', answer_file)
    if task_name_match:
        task_name = task_name_match.group(1)
        output_file = answer_file.replace('answers', 'questions_extracted')
        answer_file_path = os.path.join(answers_dir, answer_file)
        output_file_path = os.path.join(outputs_after_dir, output_file)
        if os.path.isfile(answer_file_path) and os.path.isfile(output_file_path):
            with open(answer_file_path, 'r') as f1, open(output_file_path, 'r') as f2:
                answer_lines = f1.readlines()
                output_lines = f2.readlines()
                for i in range(0, len(answer_lines), 10):
                    chunk_correct = compare_chunks(answer_lines[i:i+10], output_lines[i:i+10])
                    encoder_index = i // 10
                    accuracy_counts[encoder_index] += chunk_correct

# Calculate average accuracies
average_accuracies = [(count / 300) * 100 for count in accuracy_counts]

# Plot the results
tasks = text_encoders
averages = average_accuracies

# Set the style and color palette
sns.set(style="whitegrid")
palette = sns.color_palette("viridis", len(tasks))

plt.figure(figsize=(14, 10))
bars = plt.bar(tasks, averages, color=palette)

# Add labels on top of the bars
for bar, average in zip(bars, averages):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, round(average, 2), ha='center', va='bottom')

# Customize the plot
plt.xlabel('Encoding Methods', fontsize=16, labelpad=20)  # Increase labelpad to make the xlabel higher
plt.ylabel('Average Accuracy (%)', fontsize=14)
plt.title('Llama3.1-8B Instruct\'s Reasoning Ability on Graphs', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0, max(averages) + 10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add footnote
plt.figtext(0.5, 0.01, 'Note: The graphs are generated using the ER algorithm on a relatively small scale.', 
            wrap=True, horizontalalignment='center', fontsize=10)

# Remove top and right spines
sns.despine()

plt.tight_layout()
plt.savefig('average_accuracies_by_encoding_method.png')
plt.show()