# LLM Behavior Lab

A comprehensive testing suite for analyzing and evaluating the behavior of Language Learning Models (LLMs) across various instruction-following tasks and constraints.

## Overview

This project, developed by CloudCode, aims to provide a robust framework for testing the capabilities of LLMs in following complex instructions and adhering to specific linguistic rules. Our suite of tests covers a wide range of scenarios, from simple constraints to intricate language patterns.

## Features

- Diverse test cases covering various linguistic and structural constraints
- Easily extensible framework for adding new tests
- Automated evaluation of LLM responses
- Comprehensive documentation of test cases and their purposes

## Getting Started

### Prerequisites

- Python 3.7+
- LLM Provider and their API keys

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Cloud-Code-AI/llm-behavior-lab.git
   cd llm-behavior-lab
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API key:
   - Create a `.env` file in the root directory
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

Run the main test suite:

```
python main.py
```

To run specific tests:

```
python main.py --test alliteration palindrome
```

## Test Categories

- Basic Constraints (e.g., avoiding specific letters)
- Structural Patterns (e.g., increasing word length, specific line counts)
- Linguistic Creativity (e.g., alliteration, rhyme schemes)
- Complex Rules (e.g., progressive letter exclusion, Fibonacci word lengths)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- OpenAI for their GPT models and API
- All contributors and testers who help improve this suite

## Contact

For any queries, please open an issue or contact us at [support@cloudcode.com].
