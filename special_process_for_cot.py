import os
import transformers
from transformers import AutoTokenizer
import torch

# Directory containing the files
input_dir = '/mnt/main/outputs_new'
output_dir = '/mnt/main/cot_after'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


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

# Initialize the summarization pipeline
# summarizer = pipeline()

# Function to process each file
def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split the content into chunks
    chunks = content.split('\n\n')
    
    summarized_answers = []

    task_max_tokens = {
        "edge_existence": 2,
        "edge_count": 2,
        "node_count": 2,
        'node_degree': 2,
        "cycle_check": 7,
        "connected_nodes": 40,
    }
    
    for chunk in chunks:
        # Extract the answer part
        if 'A:' in chunk:
            answer = chunk.split('A:')[1].strip()
            # Add "summarization. The format should be like Kenny, Kyle, Tolkien. or 1, 2, 3." before the answer
            answer = "summarization. The format should be like Kenny, Kyle, Tolkien. or 1, 2, 3. \n" + answer
            # Summarize the answer
            summary = pipeline(answer,
                                 do_sample=True,
            top_k=5,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            truncation=True,
            max_new_tokens=max_new_tokens,
            )
            summarized_answers.append(summary[0]['summary_text'])
    
    # Write the summarized answers to the output file
    with open(output_file, 'w') as f:
        for summary in summarized_answers:
            f.write(summary + '\n')

# Iterate over all files in the directory
for filename in os.listdir(input_dir):
    if 'zero_cot' in filename:
        print("Process file: ", filename)
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename.replace('.txt', '_summary.txt'))
        process_file(input_file, output_file)