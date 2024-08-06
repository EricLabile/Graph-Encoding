import tensorflow as tf
import os

# Directory containing the TFRecord files
tfrecord_dir = '/mnt/main/talk-like-a-graph/tasks_new_new'
questions_dir = '/mnt/main/questions_new'
answers_dir = '/mnt/main/answers_new'

# Ensure the directories exist
os.makedirs(questions_dir, exist_ok=True)
os.makedirs(answers_dir, exist_ok=True)

# Get a list of all TFRecord files in the directory
tfrecord_files = [os.path.join(tfrecord_dir, f) for f in os.listdir(tfrecord_dir) if f.endswith('.tfrecords')]

def _parse_function(proto):
    # Define your features
    keys_to_features = {
        'question': tf.io.FixedLenFeature([], tf.string),
        'answer': tf.io.FixedLenFeature([], tf.string)
    }

    # Load one example
    parsed_features = tf.io.parse_single_example(proto, keys_to_features)
    
    return parsed_features['question'], parsed_features['answer']

print("Number of TFRecord files: ", len(tfrecord_files))

# Iterate over all TFRecord files
for tfrecord_file in tfrecord_files:
    print("processing file: ", tfrecord_file)
    # Create a TFRecordDataset
    raw_dataset = tf.data.TFRecordDataset(tfrecord_file)
    
    # Parse the dataset
    parsed_dataset = raw_dataset.map(_parse_function)
    
    questions = []
    answers = []
    cnt = 0
    for question, answer in parsed_dataset:
        questions.append(question.numpy().decode('utf-8'))
        answers.append(answer.numpy().decode('utf-8'))
        cnt += 1
    # break

    # Save questions and answers to respective directories
    output_file = tfrecord_file.split('/')[-1].split('.')[0]
    questions_file_path = os.path.join(questions_dir, output_file + '_questions.txt')
    answers_file_path = os.path.join(answers_dir, output_file + '_answers.txt')

    with open(questions_file_path, 'w') as q_file, open(answers_file_path, 'w') as a_file:
        for question, answer in zip(questions, answers):
            q_file.write(question + '\n\n')  # Add an extra newline character after each question
            a_file.write(answer + '\n')

    print("Data saved to files: ", questions_file_path, answers_file_path)

    # Clear the lists after processing each file
    questions.clear()
    answers.clear()
