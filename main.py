
import json
import os
import requests
from flask import Flask, jsonify, request


#from tavily import TavilyClient

from langchain_community.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError




# Environment variables
os.environ["api_key"] = "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"
#os.environ["tavily_base_url"] = "https://api.tavily.com"
os.environ["llm_api_key"] = "lm-studio"
os.environ["llm_base_url"] = "http://127.0.0.1:1234"



# Define a Pydantic class for each level in the mind map schema

class MindMapNode(BaseModel):
    name: str
    children: Optional[List['MindMapNode']] = Field(default_factory=list)

    class Config:
        # Allow forward references for recursive models
        arbitrary_types_allowed = True
        orm_mode = True

MindMapNode.update_forward_refs()  # Necessary to handle the self-referential nature of the children

# Define the root schema which contains the mind map
class MindMap(BaseModel):
    root: MindMapNode











class TavilyClient:
    
    #tavily_base_url="https://api.tavily.com"
    def __init__(self,tavily_base_url="https://api.tavily.com", headers=None, api_key=None, llm_api_key=None, llm_base_url=None):
        self.api_key = api_key
        self.tavily_base_url = tavily_base_url
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.headers = headers or {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

    def search(self, query: str, **kwargs) -> dict:
        api_url = "https://api.tavily.com" + "/search"
        data = {
            "query": query,
            **kwargs
        }
        
        response = requests.post(
            url=api_url,
            json=data,
            headers=TavilyClient().headers,
            timeout=100
        )
        
        return response.json()

    def llm_generation(self, query):
        llm_base_url = "http://127.0.0.1:1234/v1"
        model = "claude2-alpaca-7b.q4_0"
        
        print(f"Searching for: {query}")
        content = self.search(query)
        print(content)
        prompt = [{
            "role": "system",
            "content": 'You are an AI critical thinker research assistant. '
                       'Your sole purpose is to write well-written, critically acclaimed, '
                       'objective, and structured reports on the given text.'
        }, {
            "role": "user",
            "content": f'Information: """{content}"""\n\n'
                       f'Using the above information, provide output for the following tasks below'
                       f'Provide MLA format or markdown syntax for main topic and subtopics.'
                       f'query: "{query}" in the detailed report --'
                       f'contents :{content} Make a retailed report with summary '
                       
        }]
        
        
        lc_messages = convert_openai_messages(prompt)
        report = ChatOpenAI(model=model,base_url=llm_base_url,api_key="lm-studio").invoke(lc_messages).content
        return report


    def generate_report(self, query,**search_params:None):
        
        #Performs the Web search using Tavily
        search_results=self.search(query, **search_params)
        
        #Generating the report using the LLM
        report_content =self.llm_generation(query)
        
        return report_content
    
    def save_report_as_pdf(self, report_content, filename="report.pdf"):
        
        # Create a PDF file with the generated report content
        pdf_canvas = canvas.Canvas(filename, pagesize=letter)
        pdf_canvas.setFont("Helvetica", 12)
    
        # Define starting position
        text = pdf_canvas.beginText(40, 750)  # 40 margin from left, 750 margin from bottom
        
       # Add report content Markdown, handling line breaks and text wrapping
        for line in report_content.splitlines():
            text.textLine(line)
        #
        pdf_canvas.drawText(text)
        pdf_canvas.save()
        print(f"Report saved as {filename}")

class MindMapAI:
    # Class-level constants for LLM configuration
    
    model = "claude2-alpaca-7b.q4_0"

    def __init__(self,llm_base_url, llm_api_key, model):  # Initializes with LLM configuration.
        
        
        self.llm_base_url = "http://127.0.0.1:1234/v1"
        self.model = model or self.model  
        self.llm_api_key = os.getenv("llm_api_key")        
        
    
    
    def clean_json_output(self, markdown_output):
        """
        Cleans the given markdown JSON output by removing markdown code block syntax and escape characters.

        Args:
        - markdown_output (str): The markdown JSON output as a string.

        Returns:
        - dict: The cleaned JSON data.
        """
        try:
            # Remove the markdown code block syntax (e.g., "```json")
            cleaned_output = markdown_output.strip().replace("```json", "").replace("```", "").strip()

            # Parse the cleaned output into a Python dictionary
            cleaned_data = json.loads(cleaned_output)
            
            return cleaned_data
        except Exception as e:
            print(f"Error cleaning the JSON output: {e}")
            return None

    def process_markdown(self, cleaned_data, topic):
        # Extract the markdown output
        markdown_output_json = cleaned_data  # Get the markdown output
        #print("Markdown Output:", markdown_output_json)  # Debug statement

        # Call the clean_json_output method to clean the markdown JSON
        markdown_output_json_cleaned = self.clean_json_output(markdown_output_json)
        return markdown_output_json_cleaned
    
    
    # Example function to validate LLM output
    def validate_mind_map(data: dict):
        try:
            mind_map = MindMap(**data)
            print("Validation successful:", mind_map)
        except ValidationError as e:
            print("Validation error:", e.json())
        
        
    def generate_nodes(self):
        llm_api_key = os.getenv("llm_api_key")
        llm_base_url = os.getenv("llm_base_url")
        model = "claude2-alpaca-7b.q4_0"
        
        mindmap_ai = MindMapAI(llm_api_key,llm_base_url,model)
        # Prompt for user input on the topic
        topic = input("Enter a topic for creating a report and a mind map: ")
        
        # Define the report generation prompt
        report_prompt = [
            {
                "role": "system",
                "content": (
                    'You are an AI critical thinker research assistant. '
                    'Your sole purpose is to write well-written, critically acclaimed, '
                    'objective, and structured reports on the given topic.'
                )
            },
            {
                "role": "user",
                "content": (
                    f'Instructions:\n'
                    f'1. Provide a detailed report on the topic in 200 words: "{topic}".\n'
                    f'2. Include an introduction that outlines the main ideas.\n'
                    f'3. Organize the report into main sections and sub-sections, using markdown syntax for headers.\n'
                    f'4. Summarize key points at the end of the report.\n'
                    f'5. Ensure all claims are backed by credible sources and are well-researched.\n\n'
                    f'Please generate a comprehensive report on the topic of "{topic}".'
                )
            }
        ]

        # Convert the report prompt into the required message format
        lc_messages = convert_openai_messages(report_prompt)
        
        # Call the LLM to generate the report
        report_content = ChatOpenAI(
            model=self.model,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key
        ).invoke(lc_messages).content

        # Define the mind map response schema
        mind_map_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "mind_map",
                "schema": {
                    "type": "object",
                    "properties": {
                        "root": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "children": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "children": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {"type": "string"},
                                                        "children": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "name": {"type": "string"},
                                                                    "children": {"type": "array"}
                                                                },
                                                                "required": ["name"]
                                                            }
                                                        }
                                                    },
                                                    "required": ["name"]
                                                }
                                            }
                                        },
                                        "required": ["name"]
                                    }
                                }
                            },
                            "required": ["name", "children"]
                        }
                    },
                    "required": ["root"]
                }
            }
        }

        # Define the mind map prompt based on the generated report content
        map_prompt = [
    {
        "role": "system",
        "content": (
            "You are an AI specializing in hierarchical knowledge organization. "
            "Your task is to analyze the provided content and structure it as a mind map according to a predefined schema. "
            "This schema represents a hierarchical JSON structure, with specific requirements for each level. "
            "Please ensure that your output strictly adheres to this schema."
        )
    },
    {
        "role": "user",
        "content": (
            f'Content Information: """{report_content}"""\n\n'
            "Instructions:\n"
            "1. Carefully analyze the provided content to determine the main topic.\n"
            "2. Decompose the content into a nested structure, with each level reflecting a logical hierarchy:\n"
            "   - The top level represents the root topic.\n"
            "   - The next levels represent subtopics and finer details, organized under 'children' arrays.\n"
            "   - Each entry must contain a 'name' property, and, if applicable, a 'children' array with further nested topics.\n"
            "3. Ensure each level logically relates to its parent, creating a clear mind map format.\n\n"
            "Output Requirements:\n"
            "- Return the output as a JSON object matching the exact structure of the provided schema.\n"
            "- The JSON must be a nested hierarchy under the 'root' key, with 'name' and 'children' properties at each level.\n"
            "- For each item:\n"
            "   - Include 'name' as a string representing the topic.\n"
            "   - Use 'children' arrays where subtopics exist.\n"
            "   - If a topic has no subtopics, omit the 'children' array for that item.\n\n"
            "Expected JSON Schema:\n"
            f"{mind_map_schema}\n\n"
            
        )
    }
]


        # Convert map prompt into the required message format
        lc_messages = convert_openai_messages(map_prompt)

        # Call the LLM to generate the mind map markdown
        response = ChatOpenAI(
            model=self.model,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key
        ).invoke(lc_messages)
        
        print(response)
       
        # Extract the markdown output
        markdown_output_json = response.content  # Get the markdown output
        print(markdown_output_json)
        markdown_output_json_cleaned= mindmap_ai.process_markdown(markdown_output_json, "mind_map_output")
              
        print("Cleaned Markdown output: ", markdown_output_json_cleaned)
        with open(f"{topic}.txt", "w") as file:
            file.write(json.dumps(markdown_output_json_cleaned))

        return markdown_output_json_cleaned  # Return structured data
    
    

# Flask Application
app = Flask(__name__)

@app.route('/api/generate_mindmap', methods=['GET'])
def generate_mindmap():
    try:
        mind_map_ai = MindMapAI(
            llm_base_url=os.getenv("llm_base_url"),
            llm_api_key=os.getenv("llm_api_key"),
            model="claude2-alpaca-7b.q4_0"
        )
        mindmap_data = mind_map_ai.generate_nodes()
        
        # Save the JSON data to a file
        with open("generated_mindmap.json", "w") as json_file:
            json.dump(mindmap_data, json_file, indent=4)
        
        
        
        return jsonify(mindmap_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    '''
    query =input("Enter your query: ")
    
    tavily_client = TavilyClient()
    report = tavily_client.llm_generation(query)
    report_content=tavily_client.generate_report(f"{query}\n, {report}")
    print("Generated Report: \n", report_content, report)
    

    # Option to save as PDF
    tavily_client.save_report_as_pdf(report_content, f"{query}.pdf")
    '''
    app.run(debug=True)  # Run the Flask app
