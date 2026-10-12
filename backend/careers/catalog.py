"""Role catalogue (about 105 roles). Edit freely; re-run `python manage.py seed` (safe to repeat).
Line format: category | title | E=emerging/new, - = established | description | skill:weight,skill:weight"""

CATS = {
    'W': 'Web & Software Development', 'M': 'Mobile Development', 'D': 'Data & AI',
    'G': 'Generative AI & Emerging Tech', 'C': 'Cloud & Infrastructure', 'S': 'Cybersecurity',
    'Q': 'Quality Assurance', 'X': 'Design & Creative', 'P': 'Product, Project & Business',
    'H': 'Game, Embedded & Hardware', 'E': 'Enterprise Platforms', 'K': 'Digital Marketing & Growth',
    'F': 'Finance & Operations Analytics',
}
CATEGORIES = list(CATS.values())
NON_DEV = {'Design & Creative', 'Product, Project & Business', 'Digital Marketing & Growth',
           'Finance & Operations Analytics'}
NO_GIT = {'Business Intelligence Analyst', 'Manual QA Tester', 'Data Governance Analyst', 'Responsible AI Analyst',
          'FinOps Analyst', 'AI Product Manager', 'IT Support Specialist', 'Technical Support Engineer',
          'Network Engineer', 'GRC Analyst', 'Data Analyst'}
WEB_SKILLS = {'html', 'css', 'javascript', 'react', 'vue', 'angular', 'next.js', 'php', 'wordpress', 'electron'}

ROLES_TEXT = """
W | Full Stack Developer | - | Build both the interface and the server side of web apps. | html:3,css:3,javascript:5,git:2,react:4,node.js:4,sql:4,rest api:3,testing:2
M | Flutter Developer | - | Build cross-platform mobile apps with Dart and Flutter. | dart:5,flutter:5,state management:3,rest api:3,firebase:3,git:2,testing:2
W | Frontend Developer | - | Craft fast, accessible user interfaces for the browser. | html:4,css:4,javascript:5,react:4,git:2,typescript:2,testing:2
W | Backend Developer | - | Design servers, databases and APIs. | python:3,node.js:3,sql:4,rest api:4,django:3,git:2,docker:2,testing:2
W | Software Engineer | - | General-purpose engineering with strong fundamentals. | python:3,java:3,data structures:4,algorithms:4,git:2,sql:3,testing:2
D | Data Analyst | - | Turn raw data into decisions. | python:3,sql:5,excel:4,pandas:4,power bi:3
D | Machine Learning Engineer | - | Train, evaluate and ship machine learning models. | python:3,machine learning:5,scikit-learn:3,tensorflow:3,pytorch:3,numpy:2,statistics:3,git:1
D | Data Scientist | - | Find patterns in data and model them statistically. | python:3,statistics:4,machine learning:4,pandas:4,numpy:2,sql:3,power bi:1
D | Deep Learning Engineer | - | Build neural-network systems for vision, text and speech. | deep learning:5,pytorch:4,tensorflow:4,python:3,numpy:2,machine learning:3
D | Computer Vision Engineer | - | Teach software to understand images and video. | opencv:5,deep learning:4,python:3,numpy:2,pytorch:3
D | Business Intelligence Analyst | - | Build dashboards and reports that leaders trust. | sql:4,power bi:4,tableau:4,excel:3,statistics:2
D | Data Engineer | - | Build pipelines that move and clean data at scale. | python:3,sql:4,spark:4,airflow:3,etl:3,aws:2
C | DevOps Engineer | - | Automate building, testing and running software. | linux:4,docker:4,kubernetes:4,ci/cd:4,git:2,aws:3,terraform:2,python:1
C | Cloud Engineer | - | Design and run infrastructure on the cloud. | aws:5,azure:3,gcp:3,linux:3,networking:3,terraform:3
S | Cybersecurity Analyst | - | Protect systems and respond to threats. | cybersecurity:5,networking:4,linux:3,python:2
Q | Test Automation Engineer | - | Automate tests so releases stay safe. | testing:4,selenium:5,python:2,java:2,ci/cd:2,jira:2,git:1
Q | Manual QA Tester | - | Find bugs through careful hands-on testing. | manual testing:4,jira:3,sql:2,testing:3,agile:2
M | Android Developer | - | Build native Android apps. | kotlin:5,android:5,java:3,rest api:3,git:2,firebase:2
M | iOS Developer | - | Build native iPhone and iPad apps. | swift:5,ios:5,rest api:3,git:2,testing:1
M | React Native Developer | - | Build mobile apps with JavaScript and React. | react native:5,react:3,javascript:4,rest api:2,git:2
W | Java Backend Developer | - | Build enterprise services with Java and Spring. | java:4,spring boot:5,sql:4,rest api:3,git:2,microservices:2
W | .NET Developer | - | Build applications with C# and the .NET platform. | c#:5,.net:4,sql:3,rest api:3,git:2
W | PHP Laravel Developer | - | Build web apps with PHP and Laravel. | php:5,laravel:4,sql:4,html:2,javascript:2,rest api:2
W | Python Developer | - | Build web services and tools in Python. | python:5,django:4,sql:3,rest api:3,git:2,testing:2
W | Angular Developer | - | Build large single-page apps with Angular. | angular:5,typescript:4,javascript:3,html:2,css:2,rest api:2
W | Vue.js Developer | - | Build interactive interfaces with Vue. | vue:5,javascript:4,html:2,css:2,git:1
W | React and Next.js Developer | - | Build modern React apps with server rendering. | react:5,next.js:4,javascript:4,typescript:3,tailwind:2
W | MERN Stack Developer | - | Build apps with MongoDB, Express, React and Node. | mongodb:4,express:4,react:4,node.js:4,javascript:3
W | UI Developer | - | Turn designs into polished, responsive pages. | html:4,css:5,figma:4,tailwind:3,javascript:2,ui design:3
X | UI/UX Designer | - | Design products people love to use. | figma:5,ui design:4,ux design:4,ux research:3
H | Game Developer | - | Build games and interactive experiences. | unity:5,c#:4,c++:2,git:2
H | Embedded and IoT Engineer | - | Program devices that sense and act. | c programming:5,c++:3,arduino:3,microcontrollers:4,iot:3
C | Database Administrator | - | Keep databases fast, safe and available. | sql:5,mongodb:2,linux:2,redis:1
W | API Engineer | - | Design and integrate reliable APIs. | rest api:4,graphql:3,node.js:3,testing:2,postman:2
P | Business Analyst | - | Bridge business needs and technical teams. | excel:3,sql:3,jira:3,agile:3,power bi:2
G | Blockchain Developer | - | Build smart contracts and decentralized apps. | solidity:5,web3:3,javascript:3,git:1
W | Ruby on Rails Developer | - | Ship web apps fast with Ruby on Rails. | ruby:4,rails:5,sql:3,rest api:2,git:1
W | Go Backend Developer | - | Build fast, concurrent services in Go. | golang:5,rest api:3,sql:3,docker:2,microservices:2
W | Rust Developer | E | Write safe, high-performance systems code. | rust:5,linux:2,c++:2,git:1
W | WordPress Developer | - | Build and customise sites on WordPress. | wordpress:5,php:4,html:3,css:3,javascript:2
W | Electron Desktop Developer | - | Ship desktop apps with web technology. | electron:5,javascript:4,html:2,css:2
M | AR/VR Developer | E | Build immersive augmented and virtual reality apps. | unity:4,c#:3,webxr:2,blender:1
D | Analytics Engineer | E | Model clean, trusted data for analysts. | dbt:5,sql:5,snowflake:3,python:2,git:1
D | Streaming Data Engineer | - | Process live data streams in real time. | kafka:5,spark:3,python:3,sql:3
D | Big Data Engineer | - | Process very large datasets with Hadoop and Spark. | hadoop:4,spark:4,kafka:2,sql:3,python:2
D | Data Architect | - | Design how an organisation stores and models data. | data modeling:5,sql:4,snowflake:2,aws:2,etl:2
D | NLP Engineer | - | Build systems that understand human language. | nlp:5,python:3,transformers:4,pytorch:3,machine learning:3
D | Quantitative Analyst | - | Model markets and risk with maths and code. | python:3,statistics:4,quantitative finance:4,sql:2
D | Data Governance Analyst | E | Keep data accurate, compliant and well managed. | data governance:5,data quality:3,sql:3,excel:1
D | Robotics Engineer | - | Program robots to sense, plan and move. | ros:5,python:3,c++:4,opencv:2
G | Generative AI Engineer | E | Build products powered by large language models. | llm:5,prompt engineering:3,rag:4,langchain:3,openai api:3,python:3,vector database:3
G | LLM Application Developer | E | Wire LLMs into real apps with retrieval and tools. | llm:4,langchain:4,rag:4,vector database:3,python:3,rest api:2
G | AI Agent Developer | E | Build AI agents that plan and use tools. | ai agents:5,llm:4,langchain:3,python:3,rest api:2
G | Prompt Engineer | E | Design prompts and evaluations that make models reliable. | prompt engineering:5,llm:4,nlp:2,python:2
G | MLOps Engineer | E | Deploy, monitor and retrain models in production. | mlops:5,mlflow:3,docker:3,kubernetes:3,python:3,ci/cd:2
G | AI Product Manager | E | Lead AI product strategy and delivery. | product management:4,llm:3,machine learning:2,agile:2,roadmapping:2
G | Responsible AI Analyst | E | Keep AI systems fair, safe and accountable. | responsible ai:5,data governance:3,machine learning:2,statistics:2
G | Quantum Software Developer | E | Write programs for quantum computers. | qiskit:5,quantum computing:4,python:3
G | Edge AI Engineer | E | Run machine learning on small devices. | tinyml:4,python:3,c++:3,tensorflow:3,iot:2
G | Web3 Developer | E | Build decentralised apps and wallets. | web3:5,solidity:3,javascript:3,git:1
G | Smart Contract Auditor | E | Find security flaws in smart contracts. | solidity:4,cybersecurity:3,testing:2,web3:2
C | Site Reliability Engineer | - | Keep large systems reliable and observable. | linux:3,kubernetes:4,prometheus:3,grafana:2,python:3,ci/cd:3
C | Platform Engineer | E | Build the internal platform developers ship on. | kubernetes:4,terraform:4,ci/cd:3,golang:2,docker:2
C | DevSecOps Engineer | E | Build security into every stage of delivery. | ci/cd:3,cybersecurity:3,docker:3,owasp:3,kubernetes:2
C | Cloud Architect | - | Design cloud solutions across providers. | aws:4,azure:3,gcp:3,terraform:2,microservices:3,networking:2
C | AWS Solutions Architect | - | Design secure, scalable systems on AWS. | aws:5,networking:3,iam:3,terraform:2,microservices:2
C | Azure Administrator | - | Run and secure Microsoft Azure environments. | azure:5,networking:3,powershell:3,linux:1
C | Cloud Security Engineer | E | Secure cloud accounts, identities and workloads. | cybersecurity:3,aws:4,iam:3,terraform:2
C | FinOps Analyst | E | Control and optimise cloud spending. | finops:5,aws:3,excel:2,azure:1
C | Systems Administrator | - | Keep servers and users running smoothly. | linux:4,networking:3,windows server:3,powershell:3,bash:2
C | Network Engineer | - | Design and maintain company networks. | networking:5,cisco:4,troubleshooting:2
C | IT Support Specialist | - | Help people fix their devices and accounts. | troubleshooting:4,active directory:3,windows server:2,networking:2
C | Technical Support Engineer | - | Solve customers' technical problems. | troubleshooting:4,linux:2,sql:2,networking:2
S | Penetration Tester | - | Hack ethically to find weaknesses first. | pentesting:5,cybersecurity:3,linux:3,burp suite:3,python:2,networking:2
S | SOC Analyst | - | Watch for and respond to security alerts. | siem:5,cybersecurity:3,networking:3,incident response:3
S | GRC Analyst | - | Manage security risk, policy and audits. | grc:5,iso 27001:3,risk assessment:3,cybersecurity:2
S | Digital Forensics Analyst | - | Investigate incidents and recover evidence. | forensics:5,cybersecurity:3,linux:2,networking:2
Q | Performance Test Engineer | - | Make sure systems stay fast under load. | jmeter:5,performance testing:4,testing:3,linux:1
Q | SDET | - | Developer-level testing and automation. | testing:3,selenium:3,java:3,python:2,ci/cd:3,postman:2
X | Product Designer | - | Own the design of a product end to end. | figma:5,ux design:3,ui design:3,prototyping:3
X | UX Researcher | - | Learn what users need through research. | ux research:5,usability testing:4,figma:1
X | Graphic Designer | - | Create visuals for brands and campaigns. | photoshop:4,illustrator:4,canva:2,typography:2
X | Motion Designer | - | Animate graphics and video. | after effects:5,premiere pro:3,illustrator:2
X | 3D Artist | - | Model and texture 3D assets. | blender:5,maya:3,unity:2
X | Technical Writer | - | Explain technical products clearly. | technical writing:5,markdown:2,git:2
P | Product Manager | - | Decide what to build and why. | product management:5,jira:3,agile:3,roadmapping:3,sql:2
P | Project Manager | - | Plan, track and deliver projects. | project management:5,jira:3,agile:3,ms project:2
P | Scrum Master | - | Coach teams to deliver with Scrum. | scrum:5,agile:4,jira:3,kanban:3
H | Firmware Engineer | - | Write low-level code for hardware. | c programming:5,rtos:4,microcontrollers:4,embedded linux:3
H | VLSI Design Engineer | - | Design digital chips and FPGAs. | verilog:5,systemverilog:3,fpga:4
H | Automotive Embedded Engineer | E | Program software inside modern vehicles. | autosar:4,can bus:4,c programming:4
H | Game Designer | - | Design rules, levels and player experience. | game design:5,unity:2
E | Salesforce Developer | - | Customise the Salesforce platform. | salesforce:5,apex:4,javascript:2,sql:2
E | SAP Consultant | - | Configure and extend SAP business systems. | sap:5,abap:3,sql:2
E | ServiceNow Developer | - | Automate workflows on ServiceNow. | servicenow:5,javascript:3,rest api:2
E | Power Platform Developer | E | Build low-code apps and automations. | power apps:5,power automate:4,power bi:2,sql:1
K | Digital Marketing Specialist | - | Run online marketing across channels. | digital marketing:5,seo:4,google analytics:4,social media:3,content marketing:3
K | SEO Specialist | - | Grow organic search traffic. | seo:5,google analytics:3,keyword research:3,content marketing:2
K | Content Writer | - | Write content that informs and ranks. | content writing:5,seo:3,copywriting:3
K | Social Media Manager | - | Grow and engage an online community. | social media:5,canva:3,content marketing:3
K | Performance Marketer | - | Run paid campaigns that convert. | google ads:5,meta ads:3,google analytics:3,a/b testing:2
K | Growth Marketer | - | Find repeatable ways to grow a product. | growth hacking:4,google analytics:3,a/b testing:3,sql:2
F | Financial Analyst | - | Model and explain financial performance. | financial modeling:5,excel:4,accounting:2,power bi:1
F | People Analytics Analyst | - | Use data to improve hiring and retention. | hr analytics:4,excel:3,sql:2,power bi:2
F | Supply Chain Analyst | - | Optimise how goods and data flow. | supply chain:5,excel:3,sql:3,power bi:2
"""


def _parse(text):
    out = []
    for line in text.strip().splitlines():
        cat, title, flag, desc, sk = [x.strip() for x in line.split(' | ')]
        skills = {}
        for part in sk.split(','):
            k, w = part.rsplit(':', 1)
            skills[k.strip()] = int(w)
        out.append({'category': CATS[cat], 'title': title, 'emerging': flag == 'E', 'desc': desc, 'skills': skills})
    return out


ROLES = _parse(ROLES_TEXT)
CATEGORY_OF = {r['title']: r['category'] for r in ROLES}
EMERGING = {r['title'] for r in ROLES if r['emerging']}


def all_skills():
    return {s for r in ROLES for s in r['skills']}
