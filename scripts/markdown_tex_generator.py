import re
import argparse
import os

# Define command line flags
parser = argparse.ArgumentParser(description="A sample script to read command line flags.")

parser.add_argument('-i', '--input', type=str, help='Path to input markdown file', required=True)
parser.add_argument('-o', '--output-directory', type=str, help='Path to output directory', required=True)

args = parser.parse_args()

print(f"input: {args.input}")
print(f"output directory: {args.output_directory}")


# Read markdown file
with open(args.input, "r", encoding="utf-8") as file:
    markdown_content = file.read()


# Itemize
markdown_content = repr(markdown_content)
lines = markdown_content.split(r'\n')
modified_lines = []
in_bullets = False

# Process each line
for line in lines:
    print(line)
    # Replace - with \item
    if re.match(r'- ', line):
        line = re.sub(r'- ', r'\\item ', line)
        if not in_bullets:
            # If we're starting a new block of bullet points, add 'xxx' before
            modified_lines.append(r"\begin{enumerate}")
            in_bullets = True
        modified_lines.append(line)

    # Replace number. with \item
    elif re.match(r'^\d+\.', line):
        line = re.sub(r'^\d+\.', r'\\item', line)
        if not in_bullets:
            modified_lines.append(r"\begin{enumerate}")
            in_bullets = True
        modified_lines.append(line)

    # End enumerate
    else:
        if in_bullets:
            modified_lines.append(r"\end{enumerate}")
            in_bullets = False
        modified_lines.append(line)

# If the last lines were bullet points, end enumerate
if in_bullets:
    modified_lines.append(r"\end{enumerate}")

markdown_content = "\n".join(modified_lines[:-1])
markdown_content = markdown_content.replace('\n\\item', r'\item')
markdown_content = markdown_content.replace('\n\\end', r'\end')


# Parse markdown header
filename_pattern = re.compile(r"File name:\s*(.+)", re.IGNORECASE)
filename = filename_pattern.findall(markdown_content)

title_pattern = re.compile(r"# \s*(.+)", re.IGNORECASE)
title = title_pattern.findall(markdown_content)

name_pattern = re.compile(r"Author:\s*(.+)", re.IGNORECASE)
name = name_pattern.findall(markdown_content)

date_pattern = re.compile(r"Date:\s*(.+)", re.IGNORECASE)
date = date_pattern.findall(markdown_content)


# Parse markdown body 
body_pattern = re.compile(r"^##.*\n(.*)", re.DOTALL | re.MULTILINE)
body_match = body_pattern.search(markdown_content)
body = body_match.group(0)  # Captures everything including the ## line


# replace chapter with section
subsection_pattern = re.compile(r"###\s*(.*)")
body = subsection_pattern.sub(r"\\subsection{\1}", body)

section_pattern = re.compile(r"##\s*(.*)")
body = section_pattern.sub(r"\\section{\1}", body)


# remove empty lines
body = re.sub(r"^\s*$\n", "", body, flags=re.MULTILINE)


# Add \\ to end of line with an enter (\n)
body = re.sub(r"^(?!\\)(.*)$", r"\1\\\\", body, flags=re.MULTILINE)


# Higlight PASS and FAIL
body = body.replace('SUCCESS', r'\colorbox{lightgreen}{\textbf{SUCCES}}')
body = body.replace('FAIL', r'\colorbox{red}{\textbf{FAIL}}')


# write to tex file
filename = args.input.replace('.md', '.tex')
filename = os.path.basename(filename)
filepath = os.path.join(args.output_directory, filename)
with open(filepath, "w", encoding="utf-8") as file:
    file.write( '\\documentclass{article}\n')
    file.write( '\\usepackage{ops-document-template/template}\n')
    file.write( '\\usepackage{xcolor}\n')
    file.write( '\\definecolor{lightgreen}{rgb}{0.56, 0.93, 0.56}\n\n')
    file.write( '\\begin{document}\n')
    file.write( '\\title{' + title[0] + '}\n')
    file.write( '\\author{' + name[0] + '}\n')
    file.write( '\\date{' + date[0] + '}\n')
    file.write( '\\maketitle\n')
    file.write( '\\newpage\n\n')
    file.write( body + '\n\n')
    file.write( '\\end{document}')
print("LaTeX file created successfully!")
