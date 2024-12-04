"""
Initializes the utils package.

This file allows Python to recognize the 'utils' directory as a package,
enabling the import of utility modules.
"""


import os

def load_prompt(prompt_filename):
    prompt_path = os.path.join(os.path.dirname(__file__), prompt_filename)
    with open(prompt_path, 'r') as file:
        prompt = file.read()
    return prompt

def load_reviewer_system_prompt_base():
    return load_prompt('reviewer_system_prompt_base.txt')

def load_reviewer_system_prompt_neg():
    return load_prompt('reviewer_system_prompt_neg.txt')

def load_reviewer_system_prompt_pos():
    return load_prompt('reviewer_system_prompt_pos.txt')