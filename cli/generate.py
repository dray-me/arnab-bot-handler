import os
import sys

def generate_command(name, category, type):
    template = f"""import discord

metadata = {{
    "name": "{name}",
    "description": "Auto-generated {type} command",
    "category": "{category}",
    "cooldown": 5
}}

async def execute(bot, ctx_or_interaction, *args):
    await ctx_or_interaction.send("This is the {name} command!")
"""
    path = f"commands/{type}/{category}/{name}.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(template)
    print(f"Generated command: {path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate.py <name> <category> <slash/prefix>")
    else:
        generate_command(sys.argv[1], sys.argv[2], sys.argv[3])
