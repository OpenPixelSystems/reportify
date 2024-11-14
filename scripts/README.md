
# README

The markdown_tex_generator.sh is an tool to generate a latex and pdf file from a markdown file. This is way a professional looking document can be generated from a markdown file.

## Usage of the tool

The tool can be used by running the following command:

markdown_tex_generator.sh -i <input_file> -f <input_dir> -o <output_dir>

Always add:
- -i <input_file> or -f <input_dir>
- -o <output_dir>


## Example

### Start the markdown with with the following format

\# Title

Author: \<name\>

Date: \<date\>

### The body starts from the first title

\#\# Start of body

- You can start 
- an enumeration
- with a '-'

1. Or you can start
2. an enumeration
3. with a NUMBER.
2. the order of numbers
100. does not matter

\#\# The titles will be converted to sections in the latex File

\#\#\# Subtitles will be converted to subsections in the latex File

\#\# whitespaces 

Whitespaces will be removed to keep the document clean


as 



you


can


see

\#\# Test results

To make the test results clear, the words SUCCESS and FAIL will be highlighted in green and red respectively.

[Link to result](./example/example.pdf)

