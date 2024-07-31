# Llama3.1-Instruct's Reasoning Ability on Graphs

This is a research about LLM reasoning ability on graphs. In this research we follows https://github.com/google-research/talk-like-a-graph from Google and leverage Llama3.1-8B-Instruct to conduct the research.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Instructions on how to install and set up the project.

## Usage

pre_process.py is used to convert the outputs from talk-like-a-graph to lain txt format, which extract the questions and answers only.

inference_script.py is used to leverage the Llama to do the inference. The outputs are stored.

post_process.py is used to process the generated texts, removing useless parts.

evaluate.py is used to calculated the accuracy, which shows the reasonong ability of Llama on graph tasks.

## Contributing

Guidelines on how to contribute to the project.

## License

Information about the project's license.
