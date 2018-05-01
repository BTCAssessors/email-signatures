# Imports
import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

# Load environment
env = Environment(
	loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'signatures')),
	autoescape=select_autoescape(['html'])
)

# Load template
template = env.get_template('generic@btcassessors.com.html')

# Load data
data = json.load(open('data.json'))

# Render
sample = {"name": "John Doe", "position" : "IT Engineer", "phone" : "+376 123 456"}

for person in data:
	print template.render(**person)
	print "*"*80

