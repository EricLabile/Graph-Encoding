# Llama3.1-Instruct's Reasoning Ability on Graphs

This is a research about LLM reasoning ability on graphs. In this research we follows https://github.com/google-research/talk-like-a-graph from Google and leverage Llama3.1-8B-Instruct to conduct the research.

## ⏰TODOs

- [ ] Accelerate the inference of Llama3.1 by using pipeline API from Huggingface🤗.
- [ ]
- [ ]
- [ ]

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

For the graph generation and task generation, please refer to [this](https://github.com/google-research/talk-like-a-graph) from Google.

For the deployment of Llama3.1-Instruct, please refer to Meta's official website [this](https://llama.meta.com) for the local deployment.

## Usage




pre_process.py is used to convert the outputs from talk-like-a-graph to lain txt format, which extract the questions and answers only.

inference_script.py is used to leverage the Llama to do the inference. The outputs are stored.

post_process.py is used to process the generated texts, removing useless parts.

evaluate_and_visualize.py is used to calculated the accuracy, which shows the reasonong ability of Llama on graph tasks, and visualize them according to different variables.