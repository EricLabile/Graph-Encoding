import os
import transformers
import torch
from transformers import AutoTokenizer
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'


# Directories
questions_dir = '/mnt/main/questions_new'
outputs_dir = '/mnt/main/outputs_new'

# Ensure the output directory exists
os.makedirs(outputs_dir, exist_ok=True)

# LLaMA model setup
access_token = "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"
model = "Meta-Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float32,
    device_map="auto",
)

device = pipeline.device
print(f"Model loaded on {device}")

# Get a list of all question files in the directory
question_files = sorted([os.path.join(questions_dir, f) for f in os.listdir(questions_dir) if f.endswith('.txt')])

count = 0
# Iterate over all question files
for question_file in question_files:
    if count < 11:
        count += 1
        print("Skipping file: ", question_file)
        continue

    count += 1
    print(f"Processing file: {question_file}")
    
    # Read questions from the file
    with open(question_file, 'r') as q_file:
        questions = q_file.read().strip().split('\n\n')
    
    answers = []
    cnt = 1

    # The max_new_tokens parameter controls the maximum number of tokens that can be generated, and it varies based on the task. for edge existence, the max_new_tokens is 5. For node count, the max_new_tokens is 3. For shortest path, the max_new_tokens is 10. For connected nodes, the max_new_tokens is 5. the name of the task can be found in the file name. generate codes to read the file name and set the max_new_tokens accordingly.
    task_name_parts = os.path.basename(question_file).split('_')[:2]
    task_name = '_'.join(task_name_parts)

    # print(f"Task: {task_name}")

    # Define a mapping from task names to max_new_tokens values
    task_max_tokens = {
        "edge_existence": 2,
        "edge_count": 2,
        "node_count": 2,
        'node_degree': 2,
        "cycle_check": 7,
        "connected_nodes": 40,
    }


    max_new_tokens = task_max_tokens.get(task_name, 5)  # Default to 5 if task name is not found

    if 'zero_cot' in os.path.basename(question_file):
        max_new_tokens= 60

    print(f"Task: {task_name}, Max New Tokens: {max_new_tokens}")


    # Perform inference for each question
    for question in questions:
        print(f"Answering question: No. {cnt}")
        cnt += 1
        sequences = pipeline(
            question,
            do_sample=True,
            top_k=5,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            truncation=True,
            max_new_tokens=max_new_tokens,
        )
        
        for seq in sequences:
            answers.append(seq['generated_text'])

        for seq in sequences:
            print(f"Result: {seq['generated_text']}")

        # Clear CUDA cache
        torch.cuda.empty_cache()
    
    # Save answers to the output directory
    output_file = os.path.join(outputs_dir, os.path.basename(question_file))
    with open(output_file, 'w') as a_file:
        for answer in answers:
            a_file.write(answer + '\n\')  # Add an extra newline character after each answer
    
    print(f"Answers saved to file: {output_file}")
    torch.cuda.empty_cache()