import openai
import os

# Initialize OpenAI client
client = openai.OpenAI(
    base_url="https://aiportalapi.stu-platform.live/jpe",
    api_key="sk-GlKxsGKVhd4ftqS1L33gZw"
)

# Ask user to input the path to the code file
file_path = input("🔍 Enter the full path to your code file: ").strip()
# file_path = "D:/van/learning/AI Elevate AI Application Engineer/workshop1/test/code_block.py"

# Extract directory and base name
dir_name = os.path.dirname(file_path)
base_name = os.path.basename(file_path)
name_without_ext, ext = os.path.splitext(base_name)
output_file = os.path.join(dir_name, f"{name_without_ext}_add_comment{ext}")

# Load code from input file
with open(file_path, "r", encoding="utf-8") as file:
    code_content = file.read()

# Prepare the prompt (instruct model to reply ONLY with code)
prompt = f"""
Please analyze the code and add comments for each block (e.g., class definition, method definitions, loops, conditionals).
Rule: 
Each comment should describe the purpose of the block as a whole, rather than commenting on each individual line.
The goal is to provide a brief summary of what each block of code does.
**DO NOT fix or modify any syntax errors or formatting. Even if the code is invalid, keep it as-is.
ONLY return the updated code block with comments added, NO extra text.

Code:
\"\"\"
{code_content}
\"\"\"
"""

# Call OpenAI Chat Completion API
response = client.chat.completions.create(
    model="GPT-4o-mini",
    messages=[
        {"role": "system", "content": "You're a highly skilled software engineer."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=1000,
)

# Get commented code only
commented_code = response.choices[0].message.content.strip()

# Save to new file
with open(output_file, "w", encoding="utf-8") as output:
    output.write(commented_code)

print(f"✅ Commented code saved to: {output_file}")