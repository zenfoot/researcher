# import subprocess
# import os

# def compile_latex(latex_file_path):
#     commands = [
#         ['pdflatex', '-interaction=nonstopmode', 'template.tex'],
#         ['bibtex', 'template'],
#         ['pdflatex', '-interaction=nonstopmode', 'template.tex'],
#         ['pdflatex', '-interaction=nonstopmode', 'template.tex']
#     ]
#     cwd = os.path.dirname(latex_file_path)
#     for cmd in commands:
#         process = subprocess.run(
#             cmd,
#             cwd=cwd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         if process.returncode != 0:
#             print(f"Error during compilation: {process.stderr}")
#             return False
#     return True

# def check_latex_errors(latex_file_path):
#     # Implement LaTeX error checking, possibly using 'chktex' or similar tools
#     errors = ''
#     # Run error checking tools and capture errors
#     return errors


import subprocess
import os
import shutil

def compile_latex(latex_file_path, output_dir):
    cwd = os.path.dirname(latex_file_path)
    commands = [
        ['pdflatex', '-interaction=nonstopmode', 'template.tex'],
        ['bibtex', 'template'],
        ['pdflatex', '-interaction=nonstopmode', 'template.tex'],
        ['pdflatex', '-interaction=nonstopmode', 'template.tex']
    ]
    for cmd in commands:
        subprocess.run(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf_path = os.path.join(cwd, 'template.pdf')
    shutil.move(pdf_path, os.path.join(output_dir, 'final_report.pdf'))