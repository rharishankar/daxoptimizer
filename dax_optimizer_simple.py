#!/usr/bin/env python3
"""
DAX Expression Optimizer - SIMPLIFIED VERSION
Usage: python dax_optimizer_simple.py input.txt output.md
"""

import os
import sys
import time
import re
from openai import OpenAI

# GitHub Models API setup
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN")
)

def parse_dax_file(content):
    """Parse DAX file with dashed separators"""
    expressions = []
    lines = content.split('\n')
    
    current_measure = None
    current_dax = []
    in_dax_block = False
    
    for line in lines:
        stripped = line.strip()
        is_separator = re.match(r'^[-=]{10,}$', stripped)
        is_header = 'DAX MEASURES' in stripped
        is_measure_name = stripped.startswith('[') and ']' in stripped
        
        if is_separator:
            if current_measure and current_dax:
                dax_code = '\n'.join(current_dax).strip()
                if dax_code:
                    expressions.append({
                        'measure_name': current_measure,
                        'dax_code': dax_code
                    })
            current_measure = None
            current_dax = []
            in_dax_block = False
            
        elif is_header:
            continue
            
        elif is_measure_name:
            if current_measure and current_dax:
                dax_code = '\n'.join(current_dax).strip()
                if dax_code:
                    expressions.append({
                        'measure_name': current_measure,
                        'dax_code': dax_code
                    })
            current_measure = stripped
            current_dax = []
            in_dax_block = True
            
        elif stripped and in_dax_block:
            current_dax.append(stripped)
    
    if current_measure and current_dax:
        dax_code = '\n'.join(current_dax).strip()
        if dax_code:
            expressions.append({
                'measure_name': current_measure,
                'dax_code': dax_code
            })
    
    return expressions


def optimize_dax(measure_name, dax_code):
    """Call GitHub API to optimize DAX"""
    
    prompt = f"""Optimize this DAX expression:

{measure_name}

{dax_code}

Provide:
1. Optimized version with comments
2. What you improved
3. Edge cases handled

Format with clear sections."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a DAX expert. Optimize DAX expressions for performance and maintainability."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


def process_file(input_file, output_file):
    """Process the DAX file"""
    
    print(f"\n📖 Reading: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("🔍 Parsing expressions...")
    expressions = parse_dax_file(content)
    
    if not expressions:
        print("❌ No expressions found!")
        return
    
    total = len(expressions)
    print(f"✅ Found {total} expression(s)")
    print(f"🚀 Starting...\n")
    
    results = []
    
    for i, expr in enumerate(expressions, 1):
        name_short = expr['measure_name'][:40]
        print(f"[{i}/{total}] {name_short}... ", end='', flush=True)
        
        result = optimize_dax(expr['measure_name'], expr['dax_code'])
        
        results.append({
            'num': i,
            'name': expr['measure_name'],
            'original': expr['dax_code'],
            'response': result
        })
        
        if "ERROR:" in result:
            print("❌")
        else:
            print("✓")
        
        if i < total:
            time.sleep(1)
    
    print(f"\n💾 Writing: {output_file}")
    write_markdown(results, output_file)
    print(f"✅ Done!\n")


def write_markdown(results, output_file):
    """Write markdown output"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# DAX Optimization Report\n\n")
        f.write(f"**Total:** {len(results)}\n\n")
        f.write("---\n\n")
        
        for r in results:
            f.write(f"## {r['num']}. {r['name']}\n\n")
            
            f.write("### Original\n\n```dax\n")
            f.write(r['original'])
            f.write("\n```\n\n")
            
            f.write("### Optimization\n\n")
            f.write(r['response'])
            f.write("\n\n---\n\n")


def main():
    if len(sys.argv) != 3:
        print("\nUsage: python dax_optimizer_simple.py input.txt output.md\n")
        sys.exit(1)
    
    if not os.environ.get("GITHUB_TOKEN"):
        print("\n❌ GITHUB_TOKEN not set!")
        print("Set it: export GITHUB_TOKEN='your_token'\n")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not output_file.endswith('.md'):
        output_file += '.md'
    
    process_file(input_file, output_file)


if __name__ == "__main__":
    main()
