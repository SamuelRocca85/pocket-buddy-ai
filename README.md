# Gemini AI Agent
This is a AI agent following the guided project at [Boot.dev](https://www.boot.dev/courses/build-ai-agent-python) using Google's Gemini API and python to create and agent that can read files and directories and write to files.

## Example

![Example](example/example.gif)

## Usage

### Install rquirements with pip

```bash
pip install google-genai python-dotenv
```

### Setup ENV var

Create a `.env` file on the root of the project and create a variable `GEMINI_API_KEY`

```bash
# Example
GEMINI_API_KEY=your_api_key
```

### Run project

```bash
python3 main.py [prompt]
```

## Agent functions

- get_files_info: List all directories on a specified directory
- get_file_content: Print out the contents of a file 
- write_file: Write content to a file

> [!NOTE]  
> Agent can run this functions on the working directory
