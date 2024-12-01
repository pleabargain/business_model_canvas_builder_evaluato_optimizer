from groq import Groq
import streamlit as st
import os
import tempfile
from crewai import Crew, Agent, Task, Process
import json
import os
import requests
from crewai_tools import tool
from crewai import Crew, Process
import tomllib
from langchain_groq import ChatGroq
import pandas as pd
import datetime
import time


# create title for the streamlit app

st.title('Business Model Canvas Builder')

# create a description

st.write(f"""This application will help you in creating, evaluating, and optimizing a business model canvas. For more information, contact Dries Faems at https://www.linkedin.com/in/dries-faems-0371569/. For additional generative AI tools to accelerate venture building, check out www.youtube.com/@GenAI_Nerd_Channel""")

groq_api_key = st.text_input('Please provide your Groq API key. If you do not have a Groq API key, please go to https://console.groq.com/playground', type='password')

# create a text input for the user to input the name of the customer

st.write('Please provide a description of the different components of the business model canvas. If you do not yet have specfic information for a component, you can leave it empty.')

value_proposition = st.text_area('What is the value proposition for your business model')
customer_pofile = st.text_area('Please provide a description of the customer segment that you are targeting')
distribution_channel = st.text_area('Please provide a description of the distribution channel that you are using')
customer_relationship = st.text_area('Please provide a description of the customer relationship that you are building')
revenue_streams = st.text_area('Please provide a description of the revenue streams that you are generating')
key_resources = st.text_area('Please provide a description of the key resources that you are using')
key_activities = st.text_area('Please provide a description of the key activities that you are performing')
key_partners = st.text_area('Please provide a description of the key partners that you are working with')
cost_structure = st.text_area('Please provide a description of the cost structure that you are facing')

initial_business_model_canvas = "Value proposition: " + value_proposition + "\n" + "Customer profile: " + customer_pofile + "\n" + "Distribution channel: " + distribution_channel + "\n" + "Customer relationship: " + customer_relationship + "\n" + "Revenue streams: " + revenue_streams + "\n" + "Key resources: " + key_resources + "\n" + "Key activities: " + key_activities + "\n" + "Key partners: " + key_partners + "\n" + "Cost structure: " + cost_structure

# create a button to start the generation of the business model canvas

if st.button('Start Business Model Evaluation'):
    os.environ["GROQ_API_KEY"] = groq_api_key
    client = Groq()
    GROQ_LLM = ChatGroq(
            # api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant"
        )


    #create crew to optimize the business model canvas

    business_model_canvas_builder = Agent(
        role='Building the business model canvas',
        goal=f"""Build a business model canvas based on the information provided by the user. The business model canvas should be coherent and consistent. Pay special attention to the uniqueness of the business model canvas.""",
        backstory = """You have more than 20 years of experience in building business models. You are great in creating coherent and consistent business models. You are able to identify the uniqueness of the business model canvas.""",
        verbose = True,
        llm = GROQ_LLM,
        allow_delegation = False,
        max_iter=5,
        memory=True,
    )

    business_model_canvas_criticizer = Agent(
        role='Critiquing the business model canvas',
        goal=f"""Critique the business model canvas to identify areas for improvement and optimization. Pay special attention to inconsistencies between different parts of the business model. Try to identify room for improvement in terms of the uniqueness of the business model canvas""",
        backstory = """You have more than 20 years of experience in evaluating business models. You are great in spotting inconsistencies in business models and identifying the weaknesses in particular components of the business model canvas.""",
        verbose = True,
        llm = GROQ_LLM,
        allow_delegation = False,
        max_iter=5,
        memory=True,
    )

    business_model_canvas_optimizer = Agent(
        role='Optimize the business model canvas',
        goal=f"""Creating an optimized the business model canvas by addressing the critical comments of the business_model_canvas_criticizer.""",
        backstory="""You are an expert in optimizing the business model canvas. You find creative ideas to address the issues raised by the business_model_canvas_criticizer.
        Your main function is to improve the business model canvas.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )
    

    # Create tasks for the agents
    create_business_model_canvas = Task(
        description=f"""Create a business model canvas based on the information provided by the user. The business model canvas should be coherent and consistent. Pay special attention to the uniqueness of the business model canvas. Here is the input from the user: {initial_business_model_canvas}""",
        expected_output='As output, provide a business model canvas that is coherent and consistent. The business model canvas should be unique and should be a good starting point for building an unfair advantage.',
        agent=business_model_canvas_builder
    )
    
    critique_business_model_canvas = Task(
        description=f"""Critique the business model canvas that has been created by the business_model_canvas_builder to identify areas for improvement and optimization. You can make critical comments regarding inidividual components. In addition, critically evaluate the overall coherence and consistency of the business model canvas. Ask yourself how the components of the business model canvas could be more unique and could be used as a stepstone for building an unfair advantage.""",
        expected_output='As output, provide a critical analysis of the initial business model canvas, highlighting the main issues and inconsistencies.',
        agent=business_model_canvas_criticizer
    )

    optimize_business_model_canvas = Task(
        description=f"""Refine and optimize the business model canvas components, which have been created by the business_model_canvas_builder, by adressing the critical issues raised by the business_model_canvas_criticizer.""",
        expected_output='As output, provide an optimized business model canvas description. Clearly describe each component of the business model canvas.',
        agent=business_model_canvas_optimizer
    )

    # Instantiate the second crew with a sequential process

    first_crew = Crew(
        agents=[business_model_canvas_builder, business_model_canvas_criticizer, business_model_canvas_optimizer],
        tasks=[create_business_model_canvas, critique_business_model_canvas, optimize_business_model_canvas],
        process=Process.sequential,
        full_output=True,
        share_crew=False,
    )

    # Kick off the crew's work
    first_results = first_crew.kickoff()

    st.markdown("**Business Model Canvas Creation**")
    st.markdown("** Step 1: Initial business model created based on user input:**")
    st.write(f"""{create_business_model_canvas.output.raw_output}""")
    st.markdown("** Step 2: Critial analysis of the initial business model:**")
    st.write(f"""{critique_business_model_canvas.output.raw_output}""")
    st.markdown("** Step 3: Optimized business model canvas:**")
    st.write(f"""{optimize_business_model_canvas.output.raw_output}""")
else:
    st.write('Please click the button to start the interview')
