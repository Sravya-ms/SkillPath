import re
from .catalog import all_skills

VOCAB = ['html', 'css', 'javascript', 'typescript', 'git', 'react', 'node.js', 'express', 'sql', 'mongodb',
         'python', 'django', 'rest api', 'testing', 'docker', 'java', 'c++', 'flutter', 'dart', 'firebase',
         'state management', 'data structures', 'algorithms', 'pandas', 'excel', 'power bi',
         'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'numpy', 'scikit-learn', 'statistics',
         'opencv', 'tableau', 'spark', 'airflow', 'etl', 'aws', 'azure', 'gcp', 'linux', 'kubernetes', 'ci/cd',
         'terraform', 'networking', 'cybersecurity', 'selenium', 'manual testing', 'android', 'kotlin', 'swift',
         'ios', 'c#', '.net', 'c programming', 'unity', 'php', 'laravel', 'spring boot', 'angular', 'vue',
         'next.js', 'react native', 'tailwind', 'figma', 'ui design', 'ux design', 'ux research', 'graphql',
         'microservices', 'agile', 'jira', 'redis', 'postman', 'solidity', 'web3', 'microcontrollers',
         'arduino', 'iot', 'golang']
VOCAB = sorted(set(VOCAB) | all_skills())
ALIASES = {'js': 'javascript', 'nodejs': 'node.js', 'reactjs': 'react', 'mysql': 'sql', 'postgresql': 'sql',
           'postgres': 'sql', 'github': 'git', 'rest': 'rest api', 'restful': 'rest api', 'api': 'rest api',
           'apis': 'rest api', 'dsa': 'data structures', 'unit testing': 'testing', 'bloc': 'state management',
           'provider': 'state management', 'riverpod': 'state management', 'ml': 'machine learning',
           'sklearn': 'scikit-learn', 'k8s': 'kubernetes', 'amazon web services': 'aws', 'google cloud': 'gcp',
           'cicd': 'ci/cd', 'jenkins': 'ci/cd', 'github actions': 'ci/cd', 'nextjs': 'next.js', 'vuejs': 'vue',
           'angularjs': 'angular', 'asp.net': '.net', 'dotnet': '.net', 'cyber security': 'cybersecurity',
           'information security': 'cybersecurity', 'ux': 'ux design', 'ui/ux': 'ui design', 'tcp/ip': 'networking',
           'pyspark': 'spark', 'apache spark': 'spark', 'neural networks': 'deep learning', 'keras': 'tensorflow',
           'smart contracts': 'solidity', 'ethereum': 'solidity', 'raspberry pi': 'iot', 'embedded c': 'c programming',
           'ruby on rails': 'rails', 'langgraph': 'ai agents', 'agentic': 'ai agents', 'llms': 'llm',
           'large language models': 'llm', 'generative ai': 'llm', 'gen ai': 'llm', 'chatgpt': 'prompt engineering',
           'retrieval augmented generation': 'rag', 'pinecone': 'vector database', 'chromadb': 'vector database',
           'faiss': 'vector database', 'openai': 'openai api', 'hugging face': 'transformers',
           'huggingface': 'transformers', 'bert': 'transformers', 'natural language processing': 'nlp',
           'a/b test': 'a/b testing', 'search engine optimization': 'seo', 'ga4': 'google analytics',
           'adwords': 'google ads', 'facebook ads': 'meta ads', 'microsoft project': 'ms project', 'pmp': 'project management',
           'pen testing': 'pentesting', 'penetration testing': 'pentesting', 'burp': 'burp suite', 'splunk': 'siem',
           'ccna': 'cisco', 'adobe photoshop': 'photoshop', 'adobe illustrator': 'illustrator',
           'verilog hdl': 'verilog', 'financial modelling': 'financial modeling', 'google analytics 4': 'google analytics',
           'power app': 'power apps', 'amazon redshift': 'etl', 'apache kafka': 'kafka', 'iso27001': 'iso 27001'}


def extract_skills(text):
    """Keyword-dictionary extraction. Returns a sorted list of canonical skill names."""
    t = (text or '').lower()
    found = set()
    for term, canon in [(v, v) for v in VOCAB] + list(ALIASES.items()):
        if re.search(r'(?<![a-z0-9+#.])' + re.escape(term) + r'(?![a-z0-9+#])', t):
            found.add(canon)
    return sorted(found)
