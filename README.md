# DAX Expression Optimizer

Automated DAX optimization tool using GitHub Copilot API. Optimizes your DAX expressions for performance, handles edge cases, and adds inline comments.

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
python dax_optimizer.py input_file.txt output_file.txt
```

---

## 📝 Usage

### Basic Command

```bash
python dax_optimizer.py <input_file> <output_file>
```

### Example

```bash
python dax_optimizer.py basketball_measures.txt optimized_basketball_measures.txt
```

---

## 📄 Input File Format

Your input file should contain DAX expressions. Two formats are supported:

### Option 1: Separated by Blank Lines (Recommended)

```dax
Total Points = SUM(Game[Points])

Points Per Game = DIVIDE(SUM(Game[Points]), COUNTROWS(Game), 0)

Top Scorer = 
CALCULATE(
    MAX(Player[Name]),
    TOPN(1, Player, Player[Points], DESC)
)
```

### Option 2: One Expression Per Line

```dax
Total Points = SUM(Game[Points])
Points Per Game = DIVIDE(SUM(Game[Points]), COUNTROWS(Game), 0)
Top Scorer = CALCULATE(MAX(Player[Name]), TOPN(1, Player, Player[Points], DESC))
```

---

## 📤 Output Format

The script generates a formatted report with:

- **Original DAX**: Your input expression
- **Optimized DAX**: Improved version with inline comments
- **Improvements Made**: List of specific changes
- **Edge Cases Handled**: Edge cases addressed (blanks, nulls, division by zero, etc.)
- **Performance Notes**: Performance considerations

### Example Output

```
════════════════════════════════════════════════════════════════════════════
                              DAX OPTIMIZATION REPORT
                           Total Expressions Optimized: 3
════════════════════════════════════════════════════════════════════════════

════════════════════════════════════════════════════════════════════════════
EXPRESSION #1
════════════════════════════════════════════════════════════════════════════

┌─ ORIGINAL DAX ─────────────────────────────────────────────────────────────
│ Total Points = SUM(Game[Points])
└────────────────────────────────────────────────────────────────────────────

┌─ OPTIMIZED DAX ────────────────────────────────────────────────────────────
│ Total Points = 
│ -- Sum of points scored across all games
│ SUM(Game[Points])
└────────────────────────────────────────────────────────────────────────────

┌─ IMPROVEMENTS MADE ────────────────────────────────────────────────────────
│ - Added inline comment for clarity
│ - Expression is already optimal for performance
└────────────────────────────────────────────────────────────────────────────
```

---

## ⚙️ Configuration

### Model Selection

By default, the script uses `gpt-4o`. To use a faster/cheaper model, edit line 28 in `dax_optimizer.py`:

```python
model="gpt-4o-mini",  # Change from "gpt-4o"
```

### Rate Limiting

Default delay between API calls is 1 second. Adjust on line 143:

```python
time.sleep(1)  # Increase if hitting rate limits
```

---

## 💡 Tips

1. **Test with Small Files First**: Start with 5-10 expressions to verify setup
2. **Backup Original Files**: Always keep a copy of your original DAX expressions
3. **Review Output**: Always review optimized expressions before deploying
4. **Token Validity**: GitHub tokens expire - regenerate if you get authentication errors

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

### "File not found"

**Problem**: Input file path is incorrect

**Solution**: 
- Use full file path: `python dax_optimizer.py /full/path/to/file.txt output.txt`
- Or run from the same directory as your input file

### Authentication Error

**Problem**: Invalid or expired GitHub token

**Solution**: Generate a new token at https://github.com/settings/tokens

### Rate Limit Error

**Problem**: Too many API calls too quickly

**Solution**: Increase delay in line 143:
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
cd /path/to/your/dax/files

# 2. Set your GitHub token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 3. Test with one file
python dax_optimizer.py league_measures.txt optimized_league.txt

# 4. Review the output
cat optimized_league.txt

# 5. Process remaining files
python dax_optimizer.py team_measures.txt optimized_team.txt
python dax_optimizer.py player_measures.txt optimized_player.txt
```

---

## 🔄 Batch Processing Multiple Files

To process multiple files at once, create a bash script:

```bash
#!/bin/bash
# batch_process.sh

export GITHUB_TOKEN="your_token_here"

for file in *.txt; do
    echo "Processing $file..."
    python dax_optimizer.py "$file" "optimized_$file"
done

echo "All files processed!"
```

Run it:
```bash
chmod +x batch_process.sh
./batch_process.sh
```

---

## 📞 Support

For issues with:
- **GitHub API**: https://docs.github.com/en/rest
- **GitHub Copilot**: https://docs.github.com/en/copilot
- **This Script**: Check troubleshooting section above

---

## 🎓 Sample DAX Expressions

### Example Input File (basketball_measures.txt)

```dax
Total Points = SUM(Game[Points])

Average Points Per Game = DIVIDE(SUM(Game[Points]), COUNTROWS(Game))

Current Season Points = CALCULATE(SUM(Game[Points]), Season[IsCurrent] = TRUE)

Selected Team = VALUES(Team[TeamName])

Win Rate = DIVIDE(COUNTROWS(FILTER(Game, Game[Result] = "Win")), COUNTROWS(Game))
```

### Run Optimization

```bash
python dax_optimizer.py basketball_measures.txt optimized_basketball_measures.txt
```

---

## ⚡ Key Features

- ✨ Automated optimization using GitHub Copilot
- 📝 Adds inline comments for maintainability
- 🛡️ Handles edge cases (blanks, nulls, division by zero)
- 🚀 Performance improvements for large datasets
- 📊 Structured output with detailed explanations
- 🔄 Batch processing support
- 💯 Best practices enforcement

---

## 📜 License

Free to use for personal and commercial projects.

---

**Ready to optimize your DAX! 🎉**
