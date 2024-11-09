from flask import Flask, jsonify, request
import os
import requests
import logging
import json 


from tavily import TavilyClient

app = Flask(__name__)


# Configure logging to a file
logging.basicConfig(
    filename='app.log',  # Name of the log file
    level=logging.INFO,   # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)


# Set your API key and base URL for the local LLM
os.environ["TAVILY_API_KEY"] = "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"
BASE_URL = "http://localhost:1234/v1"  # Local API for LLMStudio
tools = ["search"]


def generate_mindmap_content(prompt, tools):
    try:
        # Format the input string manually
        tool_names = ", ".join([tool.__class__.__name__ for tool in tools])
        agent_scratchpad = ""  # If you have specific context or memory, include it here
        
        # Construct the full prompt for the model
        input_string = f"""
        Use the following tools: {tool_names}.
        {agent_scratchpad}
        Question: {prompt}
        """

        # Send a request to the completions endpoint
        response = requests.post(
            f"{BASE_URL}/completions",
            headers={"Content-Type": "application/json"},
            json={"prompt": input_string}
        )
        app.logger.info(f"Response status: {response.text}")
        # Check if the response was successful
        if response.status_code == 200:
            #mindmap_content = response.json()
            
            # Parse the JSON string
            data = response.json()

            tool_names = ", ".join(tools)
            
            # Extract the "text" field from the "choices" array
            mindmap_content = data['choices'][0]['text']
            
            app.logger.info(f"Response status: {mindmap_content}")

            #Web research using the tavily API
            client = TavilyClient(api_key="tvly-YOUR_API_KEY")
            response = client.search("Who is Leo Messi?")

            # Step 3. That's it! You've done a Tavily Search!
            print(response)
            
            
            # Access the required fields in the dictionary
            if 'choices' in data and len(data['choices']) > 0:
                extracted_text = data['choices'][0]['text']
                return {"mindmap_content": {"llm_response": extracted_text,"tool_names":tool_names}}
            else:
                return {"mindmap_content": {"error": "No choices found in response."}}
        else:
            return {"mindmap_content": {"error": f"Error: {response.status_code} - {response.text}"}}

    except Exception as e:
        return {"mindmap_content": {"error": f"An error occurred: {str(e)}"}}

@app.route('/api/get_mindmap', methods=['GET'])
def get_mindmap():
    # Get the prompt from the query parameters if provided, otherwise use a default topic
    default_content = "explaine AI in healthcare industry in 200 words"
    topic = request.args.get('prompt', default=default_content)
    
    
    # Generate the mind map content
    mindmap_content = generate_mindmap_content(topic, tools)

    
    # Return the result as JSON
    return jsonify({
        "mindmap_content": mindmap_content
    })

@app.route('/')
def home():
    return "Welcome to the Mind Map Generator!"

if __name__ == "__main__":
    app.run(debug=True, port=5002)
    
    #Web research using the tavily API
    client = TavilyClient(api_key="tvly-YOUR_API_KEY")
    response = client.search("Who is Leo Messi?")

    # Step 3. That's it! You've done a Tavily Search!
    print(response)
    
    
    
    
# Placeholder function for parsing mindmap structure
def parse_mindmap_structure(text):
    # Convert the text output from the LLM into a JSON or dict structure suitable for D3.js
    # Placeholder for parsing logic
    pass
