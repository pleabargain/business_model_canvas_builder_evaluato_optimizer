# Business Model Canvas Builder

## Overview

The Business Model Canvas Builder is a Streamlit application designed to assist users in creating, evaluating, and optimizing a business model canvas. This tool is inspired by Dries Faems and aims to provide a structured approach to developing a coherent and consistent business model.

## Features

- **User Input**: Users can input descriptions for various components of the business model canvas, including value proposition, customer profile, distribution channel, customer relationship, revenue streams, key resources, key activities, key partners, and cost structure.
- **Business Model Evaluation**: The application uses a series of agents to build, critique, and optimize the business model canvas based on user input.
- **Sequential Process**: The application follows a sequential process to ensure that the business model is coherent, consistent, and unique.

## Usage

1. **API Key**: Start by entering your Groq API key. If you do not have one, you can obtain it from [Groq Playground](https://console.groq.com/playground).
2. **Input Details**: Provide detailed descriptions for each component of the business model canvas. You can leave fields empty if specific information is not available.
3. **Start Evaluation**: Click the "Start Business Model Evaluation" button to begin the process.
4. **Results**: The application will display the initial business model, a critical analysis, and an optimized version of the business model canvas.

## Technical Details

- **Streamlit**: The application is built using Streamlit for a user-friendly interface.
- **Groq API**: Utilizes the Groq API for language model processing.
- **CrewAI**: Employs CrewAI to manage agents and tasks for building, critiquing, and optimizing the business model canvas.

## Installation

To run the application, ensure you have the necessary dependencies installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.

## Acknowledgments

Special thanks to Dries Faems for the inspiration behind this application.

## Additional Resources

For more information on the Business Model Canvas, visit [Wikipedia](https://en.wikipedia.org/wiki/Business_Model_Canvas).
