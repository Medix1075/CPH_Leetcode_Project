from bs4 import BeautifulSoup
import json
import os

def convert_problem_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract main problem description
    description = soup.find('p').get_text()
    
    # Extract examples
    examples = []
    example_blocks = soup.find_all('div', class_='example-block')
    
    for block in example_blocks:
        example = {}
        # Extract input and output
        inputs = block.find_all('span', class_='example-io')
        if inputs:
            example['input'] = inputs[0].get_text().strip()
        
        output_text = block.find_all('span', class_='example-io')
        if output_text:
            example['output'] = output_text[1].get_text().strip()
        else:
            example['output'] = "Output not found"
            
        # Extract explanation if exists
        explanation = block.find('strong', text='Explanation:')
        if explanation and explanation.find_next('p'):
            example['explanation'] = explanation.find_next('p').get_text().strip()
            
        examples.append(example)
    
    # Extract constraints
    constraints = []
    constraints_section = soup.find('strong', text='Constraints:')
    if constraints_section:
        constraints_list = constraints_section.find_next('ul')
        if constraints_list:
            constraints = [li.get_text().strip() for li in constraints_list.find_all('li')]
    
    # Create the problem dictionary
    problem_json = {
        'description': description,
        'examples': examples,
        'constraints': constraints
    }
    
    # Save JSON to file
    file_name = 'problem_data.json'
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'w') as json_file:
        json.dump(problem_json, json_file, indent=4)
    
    # Return the path of the saved file
    return file_path
