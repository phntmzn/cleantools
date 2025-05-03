import re

def clean_transcript(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Remove heading lines
        if line.startswith("#"):
            continue
        # Remove timestamps
        line = re.sub(r'\b\d{2}:\d{2}:\d{2}\.\d{3}\b', '', line)
        # Strip whitespace and skip empty lines
        stripped = line.strip()
        if stripped:
            cleaned_lines.append(stripped)

    # Write cleaned transcript
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')

# Example usage:
clean_transcript(
    'tactiq-free-transcript-LrZIxsQSCXE.txt',
    'cleaned_transcript.txt'
)
