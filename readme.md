# Business Model Canvas Builder

This application helps you create, evaluate, and optimize a business model canvas.

After entering your business model canvas data, click "Start Business Model Evaluation" to generate analysis. Then, if you like it, copy the text directly from the web page.


This application is built with Streamlit and uses Groq. 

It runs on a local machine and on streamlit community cloud.

In the data tab, you can save your business model canvas data as a JSON file and as a text file. Keep in mind saving the text file will on streamlit.io is NOT working at this time.


## Business Model Canvas Components

### Value Proposition
What value do you deliver to the customer? Which customer needs are you satisfying?
- Products and services you offer
- Pain relievers and gain creators
- Unique selling points
- Why customers should choose you over competitors

### Customer Segments
Who are your most important customers? For whom are you creating value?
- Target market demographics
- User personas
- Market size and characteristics
- Customer pain points and gains

### Distribution Channels
How do you reach your customers? Through which channels do your customer segments want to be reached?
- Sales channels (direct/indirect)
- Marketing channels
- Communication channels
- Physical/digital presence
- Customer touchpoints

### Customer Relationships
What type of relationship does each customer segment expect you to establish and maintain?
- Personal assistance
- Self-service
- Automated services
- Communities
- Co-creation
- Customer support strategy

### Revenue Streams
For what value are your customers willing to pay? How do they currently pay?
- Pricing models
- Payment methods
- Revenue sources
- Pricing strategy
- Recurring vs one-time revenues

### Key Resources
What key resources does your value proposition require?
- Physical assets
- Intellectual property
- Human resources
- Financial resources
- Technology infrastructure
- Brand and reputation

### Key Activities
What key activities does your value proposition require?
- Production
- Problem solving
- Platform/Network
- Research & Development
- Marketing & Sales
- Supply chain management

### Key Partners
Who are your key partners and suppliers? What key resources are you acquiring from them?
- Strategic alliances
- Supplier relationships
- Joint ventures
- Coopetition
- Key suppliers and their roles

### Cost Structure
What are the most important costs inherent in your business model?
- Fixed costs
- Variable costs
- Economies of scale
- Cost-driven vs value-driven
- Major cost centers
- Cost optimization opportunities

## Using the Application

Locally you can use .env and pass your Groq API key as an environment variable. like this:

```
GROQ_API_KEY="your_groq_api_key"
```

1. Fill in the details for each component of the business model canvas
2. Use the help tooltips (?) for guidance on each component
3. Click "Start Business Model Evaluation" to generate analysis
4. View and manage your data in the DATA tab:
   - View and edit your data in JSON format
   - Choose where to save your files
   - Save as JSON only or combined output (JSON + Analysis)
   - Files are automatically timestamped
5. Monitor application activity in the LOGGING tab

## Save Options

The DATA tab provides flexible options for saving your work:
- **JSON Only**: Saves your business model data in JSON format
- **Combined Output**: Saves both your business model data and the AI analysis in a single file
- Choose any folder on your system to save the files
- Files are automatically named with timestamps for easy tracking

## Tips for Success

- Be as specific as possible in your descriptions
- Consider the relationships between different components
- Think about your competitive advantages
- Focus on creating unique value for your customers
- Regular updates and revisions can help refine your business model
- Save your work regularly using the options in the DATA tab
