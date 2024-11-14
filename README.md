# MindMap AI Application

This project is a Python-based web application for generating hierarchical mind maps and reports. It uses local LLMs via LM Studio and integrates search capabilities through the Tavily API. Generated data can be saved as PDFs, allowing users to structure complex topics into mind maps with nested topics.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Code Structure](#code-structure)
- [Contributing](#contributing)

## Features

- Mind map generation with hierarchical structures.
- LLM-based content generation using local LM Studio.
- PDF report generation.
- Flask API for accessing and managing mind maps.
- Tavily API integration for web search functionality.
- Cross-Origin Resource Sharing (CORS) enabled.

## Dependencies

The following libraries are required to run this application:

- `Flask`
- `flask-cors`
- `requests`
- `reportlab`
- `pydantic`
- `logging`
- `openai`
- `langchain_community`
- `langchain_openai`

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/mindmap-ai.git
   cd mindmap-ai

2.**Install Dependencies:**

  '''bash
  pip install -r requirements.txt
  
3.**Set Up Environment Variables:** Update your .env file with the necessary keys as described in the Configuration section.

## Configuration

Set the following environment variables for the Tavily and LM Studio configurations:

 '''bash
 api_key=<Your Tavily API Key>
 llm_api_key=<Your LM Studio API Key>
 llm_base_url=<Your LM Studio Base URL>

You can configure these environment variables in the code by updating the os.environ settings.

## Usage

1. **  Run the Flask Server.
   '''bash
   python main.py



