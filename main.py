from groq import Groq
import streamlit as st
import os
import tempfile
import json
import requests
import pandas as pd
import datetime
import time
import logging
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load environment variables from .env file
load_dotenv()

# Initialize session state for storing analysis results
if 'initial_analysis' not in st.session_state:
    st.session_state.initial_analysis = None
if 'critique' not in st.session_state:
    st.session_state.critique = None
if 'optimization' not in st.session_state:
    st.session_state.optimization = None

# Function to validate GROQ API key
def validate_groq_api_key(api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
            stream=False
        )
        logging.info("API key validation successful")
        return True
    except Exception as e:
        logging.error(f"API key validation failed: {str(e)}")
        return False

# Read the README file
def read_readme():
    with open('readme.md', 'r') as file:
        return file.read()

# Function to create JSON from business model canvas data
def create_business_model_json(data_dict):
    return json.dumps(data_dict, indent=2)

# Function to save JSON file
def save_json_file(json_data, folder_path):
    try:
        # Create folder if it doesn't exist
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        datestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"business_plan_{datestamp}.json"
        
        # Combine folder path and filename
        full_path = os.path.join(folder_path, filename)
        
        # Save the file
        with open(full_path, 'w') as f:
            f.write(json_data)
        
        logging.info(f"Saved business model data to {full_path}")
        return full_path
    except Exception as e:
        error_msg = f"Error saving file: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

# Function to save combined output (JSON + Report)
def save_combined_output(json_data, analysis_data, folder_path):
    try:
        # Create folder if it doesn't exist
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        datestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON file
        json_filename = f"business_plan_{datestamp}.json"
        json_path = os.path.join(folder_path, json_filename)
        with open(json_path, 'w') as f:
            f.write(json_data)
        
        # Save combined text file
        txt_filename = f"business_plan_{datestamp}.txt"
        txt_path = os.path.join(folder_path, txt_filename)
        with open(txt_path, 'w') as f:
            f.write("=== BUSINESS MODEL CANVAS JSON ===\n\n")
            f.write(json_data)
            f.write("\n\n=== BUSINESS MODEL CANVAS ANALYSIS ===\n\n")
            f.write(analysis_data)
        
        logging.info(f"Saved JSON to {json_path} and combined output to {txt_path}")
        return json_path, txt_path
    except Exception as e:
        error_msg = f"Error saving files: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

# Function to format GROQ output
def format_output(text):
    # Add proper line breaks and formatting
    formatted_text = text.replace(". ", ".\n")
    formatted_text = formatted_text.replace("• ", "\n• ")
    return formatted_text

# Function to get GROQ completion with proper formatting
def get_groq_completion(prompt, system_prompt="You are an expert at business analysis and creation."):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Create a placeholder for the streaming output
        output_placeholder = st.empty()
        response = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                # Update the placeholder with formatted text
                output_placeholder.markdown(format_output(response))
        
        logging.info("Successfully generated GROQ completion")
        return response
    except Exception as e:
        error_msg = f"Error in GROQ completion: {str(e)}"
        logging.error(error_msg)
        st.error(error_msg)
        return None

# Help text for each component
HELP_TEXT = {
    "value_proposition": """What value do you deliver to the customer? Which customer needs are you satisfying?
• Products and services you offer
• Pain relievers and gain creators
• Unique selling points
• Why customers should choose you over competitors""",
    
    "customer_profile": """Who are your most important customers? For whom are you creating value?
• Target market demographics
• User personas
• Market size and characteristics
• Customer pain points and gains""",
    
    "distribution_channel": """How do you reach your customers? Through which channels do your customer segments want to be reached?
• Sales channels (direct/indirect)
• Marketing channels
• Communication channels
• Physical/digital presence
• Customer touchpoints""",
    
    "customer_relationship": """What type of relationship does each customer segment expect you to establish and maintain?
• Personal assistance
• Self-service
• Automated services
• Communities
• Co-creation
• Customer support strategy""",
    
    "revenue_streams": """For what value are your customers willing to pay? How do they currently pay?
• Pricing models
• Payment methods
• Revenue sources
• Pricing strategy
• Recurring vs one-time revenues""",
    
    "key_resources": """What key resources does your value proposition require?
• Physical assets
• Intellectual property
• Human resources
• Financial resources
• Technology infrastructure
• Brand and reputation""",
    
    "key_activities": """What key activities does your value proposition require?
• Production
• Problem solving
• Platform/Network
• Research & Development
• Marketing & Sales
• Supply chain management""",
    
    "key_partners": """Who are your key partners and suppliers? What key resources are you acquiring from them?
• Strategic alliances
• Supplier relationships
• Joint ventures
• Coopetition
• Key suppliers and their roles""",
    
    "cost_structure": """What are the most important costs inherent in your business model?
• Fixed costs
• Variable costs
• Economies of scale
• Cost-driven vs value-driven
• Major cost centers
• Cost optimization opportunities"""
}

# Default placeholder texts
DEFAULT_TEXTS = {
    "value_proposition": """Example: Our innovative software solution automates business process management, 
reducing operational costs by 40% while improving accuracy and efficiency.""",
    
    "customer_profile": """Example: Mid to large-sized enterprises (100+ employees) in the manufacturing sector, 
specifically operations and process managers looking to optimize their workflow.""",
    
    "distribution_channel": """Example: Direct sales through our website and enterprise sales team, 
plus partnerships with major consulting firms for broader market reach.""",
    
    "customer_relationship": """Example: Dedicated account managers for enterprise clients, 
24/7 technical support, and regular check-ins to ensure customer success.""",
    
    "revenue_streams": """Example: Monthly subscription model ($500-2000/month based on users),
implementation services ($5000-20000), and premium support packages.""",
    
    "key_resources": """Example: Proprietary automation software, cloud infrastructure,
skilled development team, and established client relationships.""",
    
    "key_activities": """Example: Software development and updates, customer support,
sales and marketing, and continuous platform improvement.""",
    
    "key_partners": """Example: Cloud service providers (AWS, Azure),
consulting firms for implementation, and technology vendors for integrations.""",
    
    "cost_structure": """Example: Development team salaries (40%), cloud infrastructure (20%),
sales and marketing (25%), customer support (15%)."""
}

# create title for the streamlit app
st.title('Business Model Canvas Builder')

# API Key Management at the top
st.markdown("### API Key Configuration")
api_key = st.text_input('Enter your GROQ API Key:', type='password', value=os.getenv('GROQ_API_KEY', ''))

col1, col2 = st.columns([1, 2])
with col1:
    if st.button('Validate API Key'):
        if not api_key:
            st.error('Please enter an API key')
            logging.warning("Attempted to validate empty API key")
        elif validate_groq_api_key(api_key):
            st.success('API key is valid!')
            # Save the valid API key to .env file
            with open('.env', 'w') as f:
                f.write(f'GROQ_API_KEY={api_key}')
            logging.info("New API key validated and saved")
        else:
            st.error('Invalid API key. Please get a new key from https://console.groq.com/keys')
with col2:
    st.markdown('Get your API key from [GROQ Console](https://console.groq.com/keys)')

st.divider()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Main", "DATA", "LOGGING", "README"])

with tab1:
    # create a description
    st.write("""This application will help you in creating, evaluating, and optimizing a business model canvas.""")
    st.write("""Inspired by Dries Faems at https://www.linkedin.com/in/dries-faems-0371569/""")

    # create inputs with default placeholder text
    value_proposition = st.text_area('What is the value proposition for your business model?', 
                                   help=HELP_TEXT["value_proposition"],
                                   placeholder=DEFAULT_TEXTS["value_proposition"])
    
    customer_profile = st.text_area('Please provide a description of the customer segment that you are targeting',
                                  help=HELP_TEXT["customer_profile"],
                                  placeholder=DEFAULT_TEXTS["customer_profile"])
    
    distribution_channel = st.text_area('Please provide a description of the distribution channel that you are using',
                                      help=HELP_TEXT["distribution_channel"],
                                      placeholder=DEFAULT_TEXTS["distribution_channel"])
    
    customer_relationship = st.text_area('Please provide a description of the customer relationship that you are building',
                                       help=HELP_TEXT["customer_relationship"],
                                       placeholder=DEFAULT_TEXTS["customer_relationship"])
    
    revenue_streams = st.text_area('Please provide a description of the revenue streams that you are generating',
                                 help=HELP_TEXT["revenue_streams"],
                                 placeholder=DEFAULT_TEXTS["revenue_streams"])
    
    key_resources = st.text_area('Please provide a description of the key resources that you are using',
                               help=HELP_TEXT["key_resources"],
                               placeholder=DEFAULT_TEXTS["key_resources"])
    
    key_activities = st.text_area('Please provide a description of the key activities that you are performing',
                                help=HELP_TEXT["key_activities"],
                                placeholder=DEFAULT_TEXTS["key_activities"])
    
    key_partners = st.text_area('Please provide a description of the key partners that you are working with',
                              help=HELP_TEXT["key_partners"],
                              placeholder=DEFAULT_TEXTS["key_partners"])
    
    cost_structure = st.text_area('Please provide a description of the cost structure that you are facing',
                                help=HELP_TEXT["cost_structure"],
                                placeholder=DEFAULT_TEXTS["cost_structure"])

    # Create business model data dictionary
    business_model_data = {
        "value_proposition": value_proposition,
        "customer_profile": customer_profile,
        "distribution_channel": distribution_channel,
        "customer_relationship": customer_relationship,
        "revenue_streams": revenue_streams,
        "key_resources": key_resources,
        "key_activities": key_activities,
        "key_partners": key_partners,
        "cost_structure": cost_structure
    }

    initial_business_model_canvas = "\n".join([
        f"Value proposition:\n{value_proposition}",
        f"\nCustomer profile:\n{customer_profile}",
        f"\nDistribution channel:\n{distribution_channel}",
        f"\nCustomer relationship:\n{customer_relationship}",
        f"\nRevenue streams:\n{revenue_streams}",
        f"\nKey resources:\n{key_resources}",
        f"\nKey activities:\n{key_activities}",
        f"\nKey partners:\n{key_partners}",
        f"\nCost structure:\n{cost_structure}"
    ])

    # create a button to start the generation of the business model canvas
    if st.button('Start Business Model Evaluation'):
        if not api_key:
            st.error("Please enter and validate your GROQ API key first")
            logging.error("Attempted to start evaluation without valid API key")
            st.stop()
            
        try:
            # Step 1: Create initial business model
            st.markdown("## Business Model Canvas Creation")
            st.markdown("### Step 1: Initial business model created based on user input")
            
            create_prompt = f"""Create a business model canvas based on the following information. The business model canvas should be coherent and consistent. Pay special attention to the uniqueness of the business model canvas.

Input from user:
{initial_business_model_canvas}

Provide a detailed analysis and suggestions for each component."""

            st.session_state.initial_analysis = get_groq_completion(create_prompt)

            # Step 2: Critique the business model
            st.markdown("### Step 2: Critical analysis of the initial business model")
            
            critique_prompt = f"""Critique the following business model canvas to identify areas for improvement and optimization. Pay special attention to inconsistencies between different parts of the business model. Identify room for improvement in terms of uniqueness.

Business Model Canvas:
{st.session_state.initial_analysis}

Provide a detailed critical analysis highlighting issues and inconsistencies."""

            st.session_state.critique = get_groq_completion(critique_prompt)

            # Step 3: Optimize the business model
            st.markdown("### Step 3: Optimized business model canvas")
            
            optimize_prompt = f"""Create an optimized version of the business model canvas by addressing the following critical issues:

Original Business Model:
{st.session_state.initial_analysis}

Critical Analysis:
{st.session_state.critique}

Provide a detailed optimized business model canvas addressing all identified issues."""

            st.session_state.optimization = get_groq_completion(optimize_prompt)
            
            logging.info("Successfully completed business model evaluation")
            
        except Exception as e:
            error_msg = f"Error during business model evaluation: {str(e)}"
            logging.error(error_msg)
            st.error(error_msg)

    else:
        st.write('Please click the button to start the evaluation')

with tab2:
    st.markdown("## Business Model Canvas Data")
    
    # Convert business model data to JSON
    json_data = create_business_model_json(business_model_data)
    
    # Allow editing of JSON
    edited_json = st.text_area("Edit Business Model Canvas JSON", json_data, height=400)
    
    # Folder selection
    st.markdown("### Save Options")
    default_folder = os.getcwd()
    save_folder = st.text_input("Save folder path:", value=default_folder,
                               help="Enter the folder path where you want to save the files")
    
    # Create columns for save options
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Save JSON button
        if st.button("Save JSON Only"):
            try:
                # Validate JSON before saving
                json.loads(edited_json)
                # Validate folder path
                if not os.path.exists(save_folder):
                    try:
                        os.makedirs(save_folder)
                    except Exception as e:
                        st.error(f"Could not create folder: {str(e)}")
                        st.stop()
                
                saved_path = save_json_file(edited_json, save_folder)
                st.success(f"Successfully saved JSON to: {saved_path}")
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON format: {str(e)}"
                logging.error(error_msg)
                st.error(error_msg)
            except Exception as e:
                st.error(f"Error saving file: {str(e)}")
    
    with col2:
        # Save combined output button
        if st.button("Save Combined Output"):
            try:
                # Validate JSON before saving
                json.loads(edited_json)
                # Validate folder path
                if not os.path.exists(save_folder):
                    try:
                        os.makedirs(save_folder)
                    except Exception as e:
                        st.error(f"Could not create folder: {str(e)}")
                        st.stop()
                
                # Prepare analysis data
                analysis_data = f"""Initial Analysis:
{st.session_state.initial_analysis if st.session_state.initial_analysis else 'No analysis generated yet'}

Critical Analysis:
{st.session_state.critique if st.session_state.critique else 'No critique generated yet'}

Optimized Business Model:
{st.session_state.optimization if st.session_state.optimization else 'No optimization generated yet'}
"""
                
                json_path, txt_path = save_combined_output(edited_json, analysis_data, save_folder)
                st.success(f"""Successfully saved files to:
- JSON: {json_path}
- Combined Report: {txt_path}""")
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON format: {str(e)}"
                logging.error(error_msg)
                st.error(error_msg)
            except Exception as e:
                st.error(f"Error saving files: {str(e)}")
    
    with col3:
        st.markdown("""
        **Save Options:** 
        - **JSON Only**: Saves just the business model data as JSON
        - **Combined Output**: Saves both JSON and analysis report
        
        **Note:** 
        - You can specify any folder path on your system
        - The folder will be created if it doesn't exist
        - Files are saved with timestamp in the name
        - Combined output includes JSON and full analysis
        """)

with tab3:
    st.markdown("## Logging")
    try:
        with open('log.txt', 'r') as log_file:
            log_content = log_file.read()
            st.text_area("Application Logs", log_content, height=400)
    except Exception as e:
        st.error(f"Error reading log file: {str(e)}")

with tab4:
    st.markdown("## README")
    st.markdown(read_readme())
