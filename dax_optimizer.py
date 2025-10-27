#!/usr/bin/env python3
"""
DAX Expression Optimizer using GitHub Copilot API
Usage: python dax_optimizer.py input.txt output.md
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

# Optimization instruction template
COPILOT_INSTRUCTION = """Please review and optimize the following DAX expression.

Requirements:
1. The expression must be **efficient** and suitable for use in large semantic models with many visuals.
2. It must return a **scalar value** (text or numeric), not a table or mixed types.
3. If the logic involves filters:
   - Use `ISFILTERED` to detect whether a column is filtered.
   - Use `HASONEVALUE` or `SELECTEDVALUE` to detect single selections.
   - Use `CONCATENATEX` to return multiple selected values as a comma-separated string.
4. Avoid using `VALUES` directly in conditional logic unless wrapped in a scalar function.
5. Ensure compatibility with visuals such as cards, tables, matrix, and tooltips.
6. Add inline comments for clarity and maintainability.
7. Suggest performance improvements if applicable, especially for large datasets or complex filter contexts.

This expression is part of a broader model with 100+ DAX measures and visualizations, so the solution must be **generalizable**, **robust**, and aligned with best practices.

Measure Name: {measure_name}

DAX Expression:
{dax_expression}

Provide your response in this exact format:

OPTIMIZED DAX:
[Your optimized DAX code with inline comments]

IMPROVEMENTS MADE:
[Bullet points of specific changes]

EDGE CASES HANDLED:
[Bullet points of edge cases addressed]

PERFORMANCE NOTES:
[Any performance considerations or warnings]
"""


def parse_dax_file(content):
    """Parse DAX file with dashed separators and measure names"""
    
    expressions = []
    
    # Split by lines that are mostly dashes (at least 10 dashes)
    lines = content.split('\n')
    
    current_measure = None
    current_dax = []
    in_dax_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check if line is a separator (lots of dashes or equals)
        is_separator = re.match(r'^[-=]{10,}$', stripped)
        
        # Check if line is a header like "DAX MEASURES - Folder1"
        is_header = 'DAX MEASURES' in stripped or 'Folder' in stripped
        
        # Check if line is a measure name like [Measure].[Patient State]
        is_measure_name = stripped.startswith('[') and ']' in stripped
        
        if is_separator:
            # If we have accumulated DAX code, save it
            if current_measure and current_dax:
                dax_code = '\n'.join(current_dax).strip()
                if dax_code:
                    expressions.append({
                        'measure_name': current_measure,
                        'dax_code': dax_code
                    })
            
            # Reset for next expression
            current_measure = None
            current_dax = []
            in_dax_block = False
            
        elif is_header:
            # Skip headers
            continue
            
        elif is_measure_name:
            # Save previous expression if exists
            if current_measure and current_dax:
                dax_code = '\n'.join(current_dax).strip()
                if dax_code:
                    expressions.append({
                        'measure_name': current_measure,
                        'dax_code': dax_code
                    })
            
            # Start new measure
            current_measure = stripped
            current_dax = []
            in_dax_block = True
            
        elif stripped and in_dax_block:
            # Add to current DAX code
            current_dax.append(stripped)
    
    # Don't forget the last expression
    if current_measure and current_dax:
        dax_code = '\n'.join(current_dax).strip()
        if dax_code:
            expressions.append({
                'measure_name': current_measure,
                'dax_code': dax_code
            })
    
    return expressions


def optimize_dax_expression(measure_name, dax_expression):
    """Send DAX to GitHub Copilot for optimization"""
    
    prompt = COPILOT_INSTRUCTION.format(
        measure_name=measure_name,
        dax_expression=dax_expression
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Change to "gpt-4o-mini" for faster/cheaper
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert DAX optimization specialist with deep knowledge of Power BI semantic models, performance optimization, and best practices. You focus on creating efficient, maintainable, and robust DAX expressions."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"ERROR: {str(e)}"


def parse_response(response):
    """Parse the structured response from Copilot"""
    result = {
        "optimized": "",
        "improvements": "",
        "edge_cases": "",
        "performance": ""
    }
    
    sections = {
        "OPTIMIZED DAX:": "optimized",
        "IMPROVEMENTS MADE:": "improvements",
        "EDGE CASES HANDLED:": "edge_cases",
        "PERFORMANCE NOTES:": "performance"
    }
    
    current_section = None
    lines = response.split('\n')
    
    for line in lines:
        # Check if this line is a section header
        found_header = False
        for header, key in sections.items():
            if header in line:
                current_section = key
                found_header = True
                break
        
        # If not a header and we're in a section, add the line
        if not found_header and current_section:
            result[current_section] += line + "\n"
    
    # Clean up whitespace
    for key in result:
        result[key] = result[key].strip()
    
    return result


def process_dax_file(input_file, output_file):
    """Process entire DAX file"""
    
    print(f"\n📖 Reading: {input_file}")
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found!")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # Parse expressions
    print(f"🔍 Parsing DAX expressions...")
    expressions = parse_dax_file(content)
    
    if not expressions:
        print("❌ No DAX expressions found in file!")
        print("\nExpected format:")
        print("  [Measure].[Name]")
        print("  ")
        print("  DAX code here")
        print("  --------------------")
        return
    
    total = len(expressions)
    
    print(f"✅ Found {total} DAX expression(s)")
    print(f"⏱️  Estimated time: ~{total * 2} seconds ({total * 2 / 60:.1f} minutes)")
    print(f"🚀 Starting optimization...\n")
    
    results = []
    
    for i, expr in enumerate(expressions, 1):
        print(f"[{i}/{total}] Processing: {expr['measure_name'][:50]}... ", end='', flush=True)
        
        # Get optimization from Copilot
        result = optimize_dax_expression(expr['measure_name'], expr['dax_code'])
        
        # Parse response
        parsed = parse_response(result)
        
        # Store results
        results.append({
            "number": i,
            "measure_name": expr['measure_name'],
            "original": expr['dax_code'],
            "optimized": parsed["optimized"],
            "improvements": parsed["improvements"],
            "edge_cases": parsed["edge_cases"],
            "performance": parsed["performance"]
        })
        
        print("✓")
        
        # Rate limiting (adjust if needed)
        if i < total:
            time.sleep(1)
    
    # Write output
    print(f"\n💾 Writing output to: {output_file}")
    write_markdown_output(results, output_file)
    
    print(f"\n✅ Complete!")
    print(f"   📄 Output file: {output_file}")
    print(f"   📊 Processed: {len(results)} expression(s)\n")


def write_markdown_output(results, output_file):
    """Write formatted Markdown output file"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("# DAX Optimization Report\n\n")
        f.write(f"**Total Expressions Optimized:** {len(results)}\n\n")
        f.write("---\n\n")
        
        # Table of Contents
        f.write("## Table of Contents\n\n")
        for r in results:
            measure_safe = r['measure_name'].replace('[', '').replace(']', '').replace('.', '-')
            f.write(f"{r['number']}. [{r['measure_name']}](#{r['number']}-{measure_safe.lower().replace(' ', '-')})\n")
        f.write("\n---\n\n")
        
        # Each expression
        for r in results:
            f.write(f"## {r['number']}. {r['measure_name']}\n\n")
            
            # Original DAX
            f.write("### 📋 Original DAX\n\n")
            f.write("```dax\n")
            f.write(r['original'])
            f.write("\n```\n\n")
            
            # Optimized DAX
            f.write("### ✨ Optimized DAX\n\n")
            if r['optimized']:
                f.write("```dax\n")
                f.write(r['optimized'])
                f.write("\n```\n\n")
            else:
                f.write("*No optimization provided*\n\n")
            
            # Improvements
            if r['improvements']:
                f.write("### 🔧 Improvements Made\n\n")
                f.write(r['improvements'])
                f.write("\n\n")
            
            # Edge Cases
            if r['edge_cases']:
                f.write("### 🛡️ Edge Cases Handled\n\n")
                f.write(r['edge_cases'])
                f.write("\n\n")
            
            # Performance
            if r['performance']:
                f.write("### ⚡ Performance Notes\n\n")
                f.write(r['performance'])
                f.write("\n\n")
            
            f.write("---\n\n")


def main():
    """Main entry point"""
    
    # Check arguments
    if len(sys.argv) != 3:
        print("\n❌ Error: Invalid arguments")
        print("\nUsage:")
        print("  python dax_optimizer.py <input_file> <output_file>")
        print("\nExample:")
        print("  python dax_optimizer.py input_file.txt output.md")
        print()
        sys.exit(1)
    
    # Check GitHub token
    if not os.environ.get("GITHUB_TOKEN"):
        print("\n❌ Error: GITHUB_TOKEN environment variable not set!")
        print("\nPlease set your GitHub Personal Access Token:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print("\nGet your token at: https://github.com/settings/tokens")
        print()
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Auto-add .md extension if not present
    if not output_file.endswith('.md'):
        output_file += '.md'
    
    # Process the file
    process_dax_file(input_file, output_file)


if __name__ == "__main__":
    main()
