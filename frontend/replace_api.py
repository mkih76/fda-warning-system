import os
import glob

old = "const API = window.location.origin + '/api'"
new = "const API = import.meta.env.VITE_API_URL || (window.location.origin + '/api')"

for f in glob.glob("src/views/**/*.vue", recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if old in content:
        content = content.replace(old, new)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated: {f}")

print("Done!")
