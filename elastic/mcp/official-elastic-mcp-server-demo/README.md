# Amazon Bedrock with Elastic - Agentic workflows with official Elastic MCP Server Demo

## Travel & Tourism Advisory application powered by Amazon Bedrock and Elastic MCP Server

This project implements a travel advisory application that uses MCP (Model Context Protocol) servers to integrate with Elasticsearch and weather services. The application leverages Amazon's Open Source [Strands SDK](https://github.com/strands-agents/sdk-python), to orchestrate an Agentic workflow that leverages tools from MCP servers and custom Strands Agent tools. The application provides information about tourist destinations, attractions, hotels, travel advisories, weather forecasts, and events. It also supports user profiles and hotel reservations.

## Product Demo

https://github.com/user-attachments/assets/d07149b9-5bdf-48e0-97da-b99ec521d3e3

## Overview 

The application provides intelligent analysis and information about tourist destinations, attractions, hotels, etc. and provides advisory to plan a travel, leveraging: 
- Amazon's open source [Strands SDK](https://github.com/strands-agents/sdk-python) based Agentic AI application
- Amazon Bedrock's Claude 3.x Sonnet for natural language understanding and reasoning 
- Elasticsearch's official MCP server for efficient data querying and analytics 
- Custom Weather MCP server for real-time weather data 
- Amazon SES MCP server for sending booking confirmation emails
- Multi-server architecture for scalable and modular functionality 

## Reference Architecture

![Agentic AI Architecture with Elastic](static/agentic-ai-strands-sdk-elastic.png)

### Key Features 
- Natural language queries for complex travel advisory, recommendations and reservations 
- Search for destinations based on various criteria (continent, budget, safety, etc.)
- Find attractions at destinations
- Search for hotels with specific amenities
- Get travel advisories for countries
- Check weather forecasts for destinations
- Find events happening at destinations
- User profiles with preferences and loyalty information
- Hotel reservation management (book, view, update, cancel)
- Room availability checking and booking
- Email confirmations via Amazon SES

### MCP Client Scripts

The project includes two client implementations in the `mcp-clients/` directory:

1. **`multi_server_mcp_client_travel_reservations.py`** — A multi-server MCP client that uses Amazon Bedrock's Converse API directly. This is the primary client with full reservation management (book, view, update, cancel, list).
2. **`agentic_ai_strands_sdk_travel_reservations.py`** — A Strands SDK-based agent client with the same travel advisory and reservation capabilities using the Strands agent framework.

### Elasticsearch Indices

The application uses the following Elasticsearch indices:

1. **destinations** — Information about travel destinations
2. **attractions** — Tourist attractions at destinations
3. **hotels** — Hotel and accommodation information
4. **advisories** — Travel advisories and safety information
5. **weather** — Weather forecasts for destinations
6. **events** — Events happening at destinations
7. **users** — User profiles and preferences
8. **reservations** — Hotel reservation information
9. **room_availability** — Room availability and pricing information

### Real-World Data Integration

The application uses realistic data for destinations and their related entities:

- Real-world destinations with accurate geographic information
- Famous attractions for popular cities
- Well-known hotels with appropriate amenities and star ratings
- Actual events that occur in each destination
- Realistic travel advisories based on current global conditions
- Seasonal weather patterns that match the destination's climate
- Sample user profiles (USER001–USER004) with preferences and loyalty tiers
- Pre-generated reservations for each user

## Setup

### Spin up EC2
You can run this on your local machine, but the instructions here are for an EC2 machine with:
- Amazon Linux 2023 AMI
- 64-bit (x86)
- t2.medium
- 40GB gp3 storage

After you launch the EC2 machine, install git and clone this repo:

```bash
sudo yum install git -y
sudo yum install nodejs -y

git clone https://github.com/aws-samples/aws-generativeai-partner-samples.git
cd aws-generativeai-partner-samples/elastic/mcp/official-elastic-mcp-server-demo
```

### AWS Account Setup
- Active AWS account with access to Amazon Bedrock 
- AWS CLI installed and configured 
- Permissions to use Claude 3 Sonnet model
- Set up AWS credentials for Bedrock access:

```shell
# Set environment variables (temporary)
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_REGION=us-west-2

# Or configure AWS CLI (permanent)
aws configure
```

### Install Dependencies
Validate Python version. If you are not running Python 3.10+, here is how you can upgrade for Amazon Linux as an example:

```bash
sudo dnf upgrade --releasever=2023.7.20250331
# Search for python3.XX versions
sudo yum list available | grep python3

# If Python 3.10 or 3.11 is found, simply install
sudo yum install python3.11 -y
python3.11 --version
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo alternatives --config python3
python3 --version
```

### Elasticsearch Setup

Sign up for Elastic Cloud (Serverless offering) on AWS using the free trial [here](https://cloud.elastic.co/registration?fromURI=%2Fhome). 
Please note, if you want to use Elastic Cloud deployment, you can choose to set up Elastic Cloud deployment as the deployment type. The screenshots below cover serverless deployment only.

After signing up with your email, select Elasticsearch as the use case:

![After signup](static/Elastic-signup1.png)
 
Select Elastic Cloud Serverless as the deployment type:

![Step2](static/Elastic-signup2.png)

Select AWS for cloud and us-west-2 for region:

![Step3](static/Elastic-signup3.png)

Select General purpose as the configuration:

![Step4](static/Elastic-signup4.png)

Wait for the project to be created. Skip creating an index:

![Step5](static/Elastic-signup5.png)

Note the following details to connect to Elastic Cloud from your application:
- Elasticsearch endpoint URL
- Elasticsearch API key

You will use these credentials in the `.env` file in the next step:
```    
ES_URL=your-elasticsearch-url 
ES_API_KEY=your-api-key
```

### Set Up Python Environment & Install Python Dependencies

```bash
# Ensure you are in the /official-elastic-mcp-server-demo directory
cd aws-generativeai-partner-samples/elastic/mcp/official-elastic-mcp-server-demo

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new environment
uv venv elastic-mcp-official-env

# Activate the environment
source elastic-mcp-official-env/bin/activate  # On Unix/Mac
# or
.\elastic-mcp-official-env\Scripts\activate   # On Windows

# Install required packages
uv pip install -r requirements.txt
```

### Setup MCP Servers
There are 3 MCP servers needed for this app:

1. **Official Elastic MCP Server** — The official MCP server implementation that connects AI agents to Elasticsearch clusters. It provides standardized methods for search operations, index management, and data retrieval. No additional setup is needed — during runtime, the MCP server is automatically downloaded and run.

2. **Weather MCP Server** — A custom MCP server that integrates with Weather.gov APIs to provide weather data and forecasting capabilities. This service currently works only for US locations. No additional setup is needed — it's pre-packaged in the `mcp-servers/weather/` folder. When setting up environment variables (next step), provide the absolute path to `mcp-servers/weather/weather.py`.

3. **Amazon SES MCP Server** — Provides email functionality that enables the agent to send booking confirmations and travel information to users. Setup:

```bash
cd mcp-servers/aws-ses-mcp/
npm install
npm run build
cd ../..
```

### Set Up Environment Variables

Run the `environment_variables_setup.sh` script to create the `.env` file with the required credentials:

```bash
# Ensure you are in the official-elastic-mcp-server-demo directory
chmod +x environment_variables_setup.sh
./environment_variables_setup.sh
```

The script will prompt you for:
- AWS credentials (Access Key ID, Secret Access Key, Region)
- AWS SES email configuration (sender email, reply-to email)
- Absolute paths to the SES MCP server (`mcp-servers/aws-ses-mcp/build/index.js`) and Weather MCP server (`mcp-servers/weather/weather.py`)
- Elasticsearch URL and API key

> **Note:** If running on your local machine instead of EC2, double-check the MCP server absolute paths — the default paths are configured for EC2.

Alternatively, you can copy `.env.example` and fill in the values manually:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Data Loading

Navigate to the `data/` directory to generate and load data:

```bash
cd data/
```

1. Generate destination and travel data (saves JSON files locally):
   ```bash
   python generate_data.py --save-json
   ```

2. Generate user profiles and reservations:
   ```bash
   python generate_user_data.py --save-json
   ```

3. Load all data into Elasticsearch:
   ```bash
   python generate_data.py --load-es
   python generate_user_data.py --load-es
   ```

```bash
cd ..
```

## Running the Application

Navigate to the `mcp-clients/` directory and run the client. The weather MCP server path is passed as an argument — the Elasticsearch MCP server is started automatically at runtime.

### Option 1: Multi-Server MCP Client (Bedrock Converse API)
```bash
cd mcp-clients/
python multi_server_mcp_client_travel_reservations.py ../mcp-servers/weather/weather.py
```

### Option 2: Strands SDK Agent Client
```bash
cd mcp-clients/
python agentic_ai_strands_sdk_travel_reservations.py ../mcp-servers/weather/weather.py
```

### Sample Queries

- I am planning a trip to New York in 2 weeks. What's the weather like and are there any travel advisories?
- Which destinations in France can I consider visiting?
- Are there any upcoming events in France that are interesting to consider for my travel?
- Any interesting events in Paris around next year?
- Can you give precise details of when Paris Fashion Week is happening?
- Find me some hotels in Paris that offer free breakfast
- When are the rooms available for the Hôtel de Crillon (Rosewood) in Paris?
- Book a hotel at Hôtel de Crillon (Rosewood) for 2 adults during the Paris Fashion Show week. I prefer a Deluxe room and a special request of 2 additional water bottles every day.
- View all of my reservations
- Update reservation <reservation_id> with new dates
- Cancel reservation <reservation_id>
- Send me a confirmation email with my reservation details

## Cleanup and Data Management

### Cleaning Up User-Related Indices

Navigate to the `data/` directory. To delete user-related indices and reload:
```bash
python generate_user_data.py --cleanup --load-es
```

To only delete user-related indices without loading new data:
```bash
python generate_user_data.py --delete-indices
```

> **Note:** Do not delete non-user-related data before deleting user-related data, as there are data dependencies.

### Cleaning Up All Indices

To delete all indices and reload:
```bash
python generate_data.py --cleanup --load-es
```

To only delete all indices without loading new data:
```bash
python generate_data.py --delete-indices
```

## Conclusion

This project demonstrates how to create MCP-compliant servers for data retrieval and integrate them with foundation models to provide seamless responses to complex queries that span multiple domains of information.

### Amazon Bedrock
- Powerful natural language understanding with FMs from Anthropic via Amazon Bedrock
- No ML infrastructure management required
- Pay-per-use pricing model
- Enhanced reasoning capabilities for complex queries

### Elastic MCP Server
- Official integration with Elasticsearch
- Optimized query performance
- Real-time data analytics
- Secure data access
- Advanced semantic and hybrid search capabilities
