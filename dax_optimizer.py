#!/usr/bin/env python3
"""
DAX Expression Optimizer using GitHub Copilot API
Usage: python dax_optimizer.py input.txt output.txt
"""

import os
import sys
import time
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

Please rewrite or improve the expression accordingly.

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


def optimize_dax_expression(dax_expression, line_number):
    """Send DAX to GitHub Copilot for optimization"""
    
    prompt = COPILOT_INSTRUCTION.format(dax_expression=dax_expression)
    
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
        for header, key in sections.items():
            if header in line:
                current_section = key
                break
        else:
            # Add content to current section
            if current_section:
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
    
    # Split expressions (assuming each expression is separated by blank line)
    # Adjust this logic based on your file format
    dax_expressions = [expr.strip() for expr in content.split('\n\n') if expr.strip()]
    
    # If expressions are line-by-line instead, uncomment this:
    # dax_expressions = [line.strip() for line in content.split('\n') if line.strip()]
    
    if not dax_expressions:
        print("❌ No DAX expressions found in file!")
        return
    
    total = len(dax_expressions)
    
    print(f"🔍 Found {total} DAX expression(s)")
    print(f"⏱️  Estimated time: ~{total * 2} seconds ({total * 2 / 60:.1f} minutes)")
    print(f"🚀 Starting optimization...\n")
    
    results = []
    
    for i, dax in enumerate(dax_expressions, 1):
        print(f"[{i}/{total}] Processing expression {i}... ", end='', flush=True)
        
        # Get optimization from Copilot
        result = optimize_dax_expression(dax, i)
        
        # Parse response
        parsed = parse_response(result)
        
        # Store results
        results.append({
            "line": i,
            "original": dax,
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
    write_output(results, output_file)
    
    print(f"\n✅ Complete!")
    print(f"   📄 Output file: {output_file}")
    print(f"   📊 Processed: {len(results)} expression(s)\n")


def write_output(results, output_file):
    """Write formatted output file"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("=" * 120 + "\n")
        f.write("DAX OPTIMIZATION REPORT\n".center(120))
        f.write(f"Total Expressions Optimized: {len(results)}\n".center(120))
        f.write("=" * 120 + "\n\n")
        
        for r in results:
            # Expression header
            f.write(f"\n{'═' * 120}\n")
            f.write(f"EXPRESSION #{r['line']}\n")
            f.write(f"{'═' * 120}\n\n")
            
            # Original DAX
            f.write("┌─ ORIGINAL DAX " + "─" * 103 + "\n")
            for line in r['original'].split('\n'):
                f.write(f"│ {line}\n")
            f.write("└" + "─" * 119 + "\n\n")
            
            # Optimized DAX
            f.write("┌─ OPTIMIZED DAX " + "─" * 102 + "\n")
            for line in r['optimized'].split('\n'):
                f.write(f"│ {line}\n")
            f.write("└" + "─" * 119 + "\n\n")
            
            # Improvements
            if r['improvements']:
                f.write("┌─ IMPROVEMENTS MADE " + "─" * 98 + "\n")
                for line in r['improvements'].split('\n'):
                    f.write(f"│ {line}\n")
                f.write("└" + "─" * 119 + "\n\n")
            
            # Edge Cases
            if r['edge_cases']:
                f.write("┌─ EDGE CASES HANDLED " + "─" * 97 + "\n")
                for line in r['edge_cases'].split('\n'):
                    f.write(f"│ {line}\n")
                f.write("└" + "─" * 119 + "\n\n")
            
            # Performance Notes
            if r['performance']:
                f.write("┌─ PERFORMANCE NOTES " + "─" * 98 + "\n")
                for line in r['performance'].split('\n'):
                    f.write(f"│ {line}\n")
                f.write("└" + "─" * 119 + "\n\n")


def main():
    """Main entry point"""
    
    # Check arguments
    if len(sys.argv) != 3:
        print("\n❌ Error: Invalid arguments")
        print("\nUsage:")
        print("  python dax_optimizer.py <input_file> <output_file>")
        print("\nExample:")
        print("  python dax_optimizer.py my_dax.txt optimized_dax.txt")
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
    
    # Process the file
    process_dax_file(input_file, output_file)


if __name__ == "__main__":
    main()
