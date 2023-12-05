
# MVP Features: 

1. Generate a BI app - Creates a BI Dashboard that answers business questions about solar data and predicts future failures based on python language and microservice architecture:

- Capture the requirements (business questions asked for a given data set)
- Load data from the desktop (example data is solar sensor data).
- Based on the data and requirements, create a datamart automatically with metrics and features
- Based on the data and requirements, create a predictive model to identify components to fail
- Based on the data and requirements, create a dashboard answer the business questiones asked.

2. Generate documentation - Business Requirements and Solution Design

3. Generate accurate code that runs locally under workspace folder.



# Functional Requirements

1. Develop "App AI Assistant" that helps non-technical people (Business User / Boss) to create complete enterprise grade apps. Currenlty BI Apps are supported.

2. Based on the app type, "App AI Assistant" pulls the right team / roles together to managed the app lifecycle (based on organization requirements)

3. The organization has a template to customize for each role, so that the final app can be generated accordingly.

4. All the team to communicate to each other to colloborativetly build the entire app based on configurable organization standards.

5. Implement each role as an agent. Each agent gets the requirement/message from previous role, thinks about it and decides to take an action (alse called stages). 

6. The team communicates with the Business User / Boss (Human in the loop) to capture missing details that are missing.

7. Store the communication and decisons in cache (context) so that a knowledge base can be built over time across the organization to fulfill similar requests with curated requirements. For e.g. For BI Apps, remember data sources, data curation rules, etl architectures, metrics used for BI Apps across the organization, so the next time once the same data source, metrics being asked by some other user, the "App AI Assistant" would readily use (after confirming) this avaialble knowledge to generate the app.

8. Eventually, the AI Assitant creates requirements, design, working code, related documentation in a local folder. And it automatically runs the generated app.

9. AI Assitant asks for feedback if the outcome is satisfactory. Once the app is approved by the business user, technical staff (senior developer/architect), it can be used as a solution starter to further extend the app. --> In the future, deployment to platforms will be supported.



# Non-Functional Requirements

1. The solution will be secure. Initially deployed on Azure Open AI with GPT4-Turbo LLM. 

2. Cost Control is required and approximate cost of generating an app to be calculated. Cost optimization measures needs to be implemented.

3. [FUTURE: As LLM depends on public repos, the private repos based will need to be trained to generate specific code (for e.g. ETL, etc.)]

4. [FUTURE: The quality of the generated app will be rated. The AI Assitants will need to learn, improve itself to be better.]

5. [FUTURE: Build Governance tools]


#  Roadmap

1. Create new App types (Data Products, microservices with APIs, decision/smart apps for decision making, Automations apps - as autonomous agents) and dynamically map to an app type once a request is provided from the chat window. Currently, it is hard coded to create BI apps only.

2. Implement security controls (users need to login first and can only access the data available to them, etc)

3. Build own model to reduce cost, increase quality (train on private repos, specific technologies, open source projects), performance, and flexibility for customizations.

4. Self-Learning: Learn from failures and build models based on the feedback. How to measure the hallucination automatically and if the generated code is not OK, what to do?

5. Enhanced Context: Manage the large contexes shared across projects (so that many clarifications can be assumed from the context to minimize the feedback required)

6. Governance: Build enterprise governance tools for regulations, policies, compliance, logging, monitoring.


#  Evaluate

1. Integration with Promt Engineering IDE to optimize the prompts https://x.ai/prompt-ide/ 
2. https://huggingface.co/blog/starcoder as LLM
