from dotenv import load_dotenv
import openai
import os

load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = os.getenv("OPENAI_BASE_URL")
)

# Ask user to input the path to the code file
file_path = input("🔍 Enter the full path to your code file: ").strip()

# Extract directory and base name
dir_name = os.path.dirname(file_path)
base_name = os.path.basename(file_path)
name_without_ext, ext = os.path.splitext(base_name)
output_file = os.path.join(dir_name, f"{name_without_ext}_add_comment{ext}")

# Load code from input file
with open(file_path, "r", encoding="utf-8") as file:
    code_content = file.read()

# Prepare the prompt (instruct model to reply ONLY with code)
with open("comment_prompt.txt", "r", encoding="utf-8") as prompt_file:
    prompt_template = prompt_file.read()

prompt = prompt_template.replace("{{CODE_CONTENT}}", code_content)

# Call OpenAI Chat Completion API
response = client.chat.completions.create(
    model="GPT-4o-mini",
    messages=[
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