# DAX Expression Optimizer

Automated DAX optimization tool using GitHub Copilot API. Optimizes your DAX expressions for performance, handles edge cases, and adds inline comments. **Outputs clean Markdown files** for easy reading.

---

## 📋 Prerequisites

- Python 3.7 or higher
- GitHub account with Copilot access
- GitHub Personal Access Token

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install openai
```

### 2. Get Your GitHub Token

1. Visit: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name (e.g., "DAX Optimizer")
4. Select scope: **`repo`**
5. Click **"Generate token"**
6. Copy the token (starts with `ghp_...`)

### 3. Set Your Token

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

**Windows (Command Prompt):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
```

**Mac/Linux:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### 4. Run the Script

```bash
python dax_optimizer.py input_file.txt output.md
```

---

## 📝 Usage

### Basic Command

```bash
python dax_optimizer.py <input_file> <output_file.md>
```

### Example

```bash
python dax_optimizer.py basketball_measures.txt optimized_basketball.md
```

**Note:** The output file will automatically get a `.md` extension if you don't include it.

---

## 📄 Input File Format

Your input file should follow this format:

```
DAX MEASURES - Folder1
=========================

[Measure].[Total Points]

SUM(Game[Points])

--------------------

[Measure].[Points Per Game]

DIVIDE(SUM(Game[Points]), COUNTROWS(Game))

--------------------

[Measure].[Selected Team]

IF( ISFILTERED( Team[Name] ),
    VALUES( Team[Name] ),
    "Not Selected"
)

--------------------
```

**Key Format Requirements:**
- Measure names like: `[Measure].[Name]`
- DAX code follows the measure name
- Sections separated by dashed lines (`----`)
- Headers like "DAX MEASURES - Folder1" are optional

---

## 📤 Output Format

The script generates **two files**:

1. **Main Output (.md)** - Clean Markdown file with formatted results
2. **Debug Output (_debug.txt)** - Raw API responses for troubleshooting

### Main Output Structure

The Markdown file includes:

- Table of Contents with clickable links
- Syntax-highlighted DAX code blocks
- Organized sections for each measure
- Clear formatting with emojis for readability

- Table of Contents with clickable links
- Syntax-highlighted DAX code blocks
- Organized sections for each measure
- Clear formatting with emojis for readability

### Example Output Structure

```markdown
# DAX Optimization Report

**Total Expressions Optimized:** 5

## Table of Contents

1. [Measure].[Total Points]
2. [Measure].[Points Per Game]
...

---

## 1. [Measure].[Total Points]

### 📋 Original DAX

```dax
SUM(Game[Points])
```

### ✨ Optimized DAX

```dax
Total Points = 
-- Sum of points scored across all games
SUM(Game[Points])
```

### 🔧 Improvements Made

- Added inline comment for clarity
- Expression is already optimal

### 🛡️ Edge Cases Handled

- Handles blank values correctly
- Returns 0 for empty tables

### ⚡ Performance Notes

- Efficient for large datasets
- No context transition overhead

---
```

---

## ⚙️ Configuration

### Model Selection

By default, the script uses `gpt-4o`. To use a faster/cheaper model, edit line 131 in `dax_optimizer.py`:

```python
model="gpt-4o-mini",  # Change from "gpt-4o"
```

### Rate Limiting

Default delay between API calls is 1 second. Adjust on line 261:

```python
time.sleep(1)  # Increase if hitting rate limits
```

---

## 💡 Tips

1. **Test with Small Files First**: Start with 5-10 expressions to verify setup
2. **Backup Original Files**: Always keep a copy of your original DAX expressions
3. **Review Output**: Always review optimized expressions before deploying
4. **Token Validity**: GitHub tokens expire - regenerate if you get authentication errors
5. **View Markdown**: Use any Markdown viewer (VS Code, Typora, GitHub) to view the output beautifully

---

## 🔧 Troubleshooting

### "GITHUB_TOKEN not set"

**Problem**: Environment variable not configured

**Solution**: Run the token export command in the same terminal window:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### "No module named 'openai'"

**Problem**: OpenAI library not installed

**Solution**: Install the library:
```bash
pip install openai
```

### "No optimization provided"

**Problem**: Output shows "No optimization provided" for expressions

**Solution**:
1. Check the debug file (ending in `_debug.txt`) to see the raw API responses
2. Verify your GitHub token has API access
3. Try switching to `gpt-4o-mini` model (edit line 131 in script)
4. The script now has improved parsing - re-download the latest version

If the debug file shows actual optimizations but they're not being parsed, please share the debug output for further help.

### "No DAX expressions found in file!"

**Problem**: Input file format doesn't match expected format

**Solution**: 
- Make sure measure names start with `[` and contain `]`
- Ensure sections are separated by dashed lines (`----`)
- Check that DAX code appears after measure names

### "File not found"

**Problem**: Input file path is incorrect

**Solution**: 
- Use full file path: `python dax_optimizer.py C:\path\to\file.txt output.md`
- Or run from the same directory as your input file

### Authentication Error

**Problem**: Invalid or expired GitHub token

**Solution**: Generate a new token at https://github.com/settings/tokens

### Rate Limit Error

**Problem**: Too many API calls too quickly

**Solution**: Increase delay in line 261:
```python
time.sleep(2)  # Increase from 1 to 2 seconds
```

---

## 📊 Processing Time & Cost

### Estimated Processing Time
- **Per Expression**: ~2 seconds
- **50 Expressions**: ~2 minutes
- **40 Files (2000 expressions)**: ~60-70 minutes

### Estimated Cost (GitHub Models API)
- **gpt-4o**: ~$0.60 per 50-expression file
- **gpt-4o-mini**: ~$0.15 per 50-expression file
- **40 Files**: ~$6-25 total (depending on model)

---

## 🎯 What Gets Optimized

The tool focuses on:

1. ✅ **Performance**: Replaces slow patterns with faster alternatives
2. ✅ **Edge Cases**: Handles blanks, nulls, division by zero, empty tables
3. ✅ **Best Practices**: Uses SELECTEDVALUE, HASONEVALUE, ISFILTERED appropriately
4. ✅ **Scalar Returns**: Ensures compatibility with cards, tooltips, and visuals
5. ✅ **Comments**: Adds inline documentation
6. ✅ **Filter Logic**: Optimizes filter contexts and calculations

---

## 📖 Example Workflow

```bash
# 1. Navigate to your project directory
cd C:\Users\YourName\Desktop\dax_optimizer

# 2. Set your GitHub token (Windows PowerShell)
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 3. Test with one file
python dax_optimizer.py input_file.txt optimized_output.md

# 4. Review the output (opens in Markdown viewer)
code optimized_output.md

# 5. Process remaining files
python dax_optimizer.py file2.txt optimized_file2.md
python dax_optimizer.py file3.txt optimized_file3.md
```

---

## 🔄 Batch Processing Multiple Files

To process multiple files at once:

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="your_token_here"

Get-ChildItem *.txt | ForEach-Object {
    $output = "optimized_$($_.Name.Replace('.txt', '.md'))"
    Write-Host "Processing $($_.Name)..."
    python dax_optimizer.py $_.Name $output
}
```

**Mac/Linux (Bash):**
```bash
export GITHUB_TOKEN="your_token_here"

for file in *.txt; do
    output="optimized_${file%.txt}.md"
    echo "Processing $file..."
    python dax_optimizer.py "$file" "$output"
done
```

---

## 📞 Support

For issues with:
- **GitHub API**: https://docs.github.com/en/rest
- **GitHub Copilot**: https://docs.github.com/en/copilot
- **This Script**: Check troubleshooting section above

---

## 🎓 Sample Input File

Create a file called `basketball_measures.txt`:

```
DAX MEASURES - Basketball Stats
================================

[Measure].[Total Points]

SUM(Game[Points])

--------------------

[Measure].[Points Per Game]

DIVIDE(SUM(Game[Points]), COUNTROWS(Game))

--------------------

[Measure].[Current Season Points]

CALCULATE(SUM(Game[Points]), Season[IsCurrent] = TRUE)

--------------------

[Measure].[Selected Team]

VALUES(Team[TeamName])

--------------------

[Measure].[Win Rate]

DIVIDE(COUNTROWS(FILTER(Game, Game[Result] = "Win")), COUNTROWS(Game))

--------------------
```

### Run Optimization

```bash
python dax_optimizer.py basketball_measures.txt optimized_basketball.md
```

Then open `optimized_basketball.md` in any Markdown viewer!

---

## ⚡ Key Features

- ✨ Automated optimization using GitHub Copilot
- 📝 Adds inline comments for maintainability
- 🛡️ Handles edge cases (blanks, nulls, division by zero)
- 🚀 Performance improvements for large datasets
- 📊 **Beautiful Markdown output** with syntax highlighting
- 🔗 **Clickable Table of Contents** for easy navigation
- 🔄 Batch processing support
- 💯 Best practices enforcement

---

## 📜 License

Free to use for personal and commercial projects.

---

**Ready to optimize your DAX! 🎉**
