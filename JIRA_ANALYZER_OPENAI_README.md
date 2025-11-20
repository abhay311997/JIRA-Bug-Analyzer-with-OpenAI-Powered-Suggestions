# JIRA Bug Analyzer with OpenAI GPT-4o Integration

A Python GUI application that analyzes JIRA bugs using **OpenAI GPT-4o** and provides AI-powered bug fix suggestions by scanning your actual workspace codebase.
**Real AI analysis with your actual code context!**

## 🎯 Features

- 🔍 **JIRA Integration**: Fetches bug details directly from JIRA REST API v3
- 📁 **Workspace Code Scanning**: Automatically scans your project files (.java, .cpp, .h, .py, .js, .ts)
- 🤖 **OpenAI GPT-4o AI Analysis**: Real AI-powered bug analysis using OpenAI's most advanced model
- 🎯 **Workspace-Aware Recommendations**: AI analyzes your actual code and suggests specific fixes
- 💡 **Comprehensive Fix Suggestions**: Root cause analysis, code examples, testing approach, and deployment checklist
- 🎨 **Beautiful GUI**: Mobileum-branded interface with logo and professional layout
- 🌐 **Browser Integration**: Quick access to view bugs in JIRA web interface
- 🔧 **Customizable**: Works with any technology stack and project type

## Prerequisites

### Required Software:
- Python 3.8 or higher
- pip (Python package manager)

### Required Python Libraries:
```bash
pip install requests pillow
```

Note: `tkinter` usually comes pre-installed with Python. If not, install it:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Should be included with Python installation

### Required Credentials:

#### 1. JIRA API Token
- Go to: https://id.atlassian.com/manage-profile/security/api-tokens
- Click **"Create API token"**
- Give it a name (e.g., "JIRA Analyzer")
- Copy the generated token

#### 2. OpenAI API Key (Required)
- Go to: https://platform.openai.com/api-keys
- Click **"Create new secret key"**
- Give it a name (e.g., "JIRA Analyzer")
- Copy the generated key (starts with `sk-proj-...`)
- **Important**: You need an active OpenAI account with billing set up
- Check your usage: https://platform.openai.com/account/usage
- Check your billing: https://platform.openai.com/account/billing/overview

## Setup Instructions

### 1. Install Dependencies

```bash
pip install requests
pip install Pillow
```

### 2. Configure for Your Project

Edit the `jira_analyzer-OPENAI.py` file and update the hardcoded configuration section at the top of the `JiraAnalyzerGUI` class:

```python
class JiraAnalyzerGUI:
    # ========== HARDCODED CONFIGURATION ==========
    # Configure your tokens and project details here
    JIRA_BASE_URL = "https://your-company.atlassian.net"  # ← Your JIRA URL
    JIRA_EMAIL = "your.email@company.com"                 # ← Your email
    JIRA_API_TOKEN = "your_jira_api_token_here"          # ← Your JIRA token
    OPENAI_API_KEY = "sk-proj-your_openai_key_here"      # ← Your OpenAI key
    WORKSPACE_PATH = str(Path.cwd())                      # ← Workspace path
    
    # Project-specific configuration (customize for your project)
    PROJECT_NAME = "My Project"                           # ← Your project name
    PROJECT_TECHNOLOGIES = [
        "Python", "Java", "React", "Node.js", ...        # ← Your tech stack
    ]
    PROJECT_COMPONENTS = [
        "Frontend", "Backend", "Database", "API", ...     # ← Your components
    ]
    # =============================================
```

#### Get JIRA API Token:
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "JIRA Analyzer")
4. Copy the token and paste it into `JIRA_API_TOKEN`

#### Get OpenAI API Key:
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Give it a name (e.g., "JIRA Analyzer")
4. Copy the key and paste it into `OPENAI_API_KEY`
5. **Important**: Ensure you have billing set up on your OpenAI account

#### Customize Project Configuration:
1. **PROJECT_NAME**: Set your project name (e.g., "RNS-AMMS")
2. **PROJECT_TECHNOLOGIES**: List all technologies used in your project
   - Examples: Python, Java, C++, JavaScript, React, Angular, Vue, Node.js, Django, Spring Boot, .NET, Docker, Kubernetes, PostgreSQL, MongoDB, Redis, etc.
3. **PROJECT_COMPONENTS**: List main components/modules of your project
   - Examples: Frontend, Backend, API Gateway, Database, Authentication, Payment Processing, Notification Service, etc.

This customization helps the AI provide more relevant and accurate bug analysis specific to your project!

---

## 🤖 **OpenAI GPT-4o Integration**

### **How It Works:**

This tool uses **OpenAI's GPT-4o** (the most advanced model) to provide AI-powered bug analysis:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Fetch JIRA Bug                                          │
│    └─> JIRA REST API v3                                    │
│    └─> Parse bug details and description                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Scan Workspace (Deep Analysis)                          │
│    └─> Scan up to 100 code files                           │
│    └─> Read up to 1000 lines per file                      │
│    └─> Collect .java, .cpp, .h, .py, .js, .ts files        │
│    └─> Build workspace structure (30 items max)            │
│    └─> Prepare 15 file summaries                           │
│    └─> Extract 8 code samples (1500 chars each)            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Send to OpenAI GPT-4o                                    │
│    └─> API: https://api.openai.com/v1/chat/completions     │
│    └─> Model: gpt-4o                                       │
│    └─> Context includes:                                   │
│        • Bug ID, summary, description                      │
│        • Project name and technologies                     │
│        • Workspace structure (directories/files)           │
│        • File summaries (15 files)                         │
│        • Code samples (8 files, 1500 chars each)           │
│    └─> Max output: 3000 tokens                             │
│    └─> Temperature: 0.7 (balanced creativity/accuracy)     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Display AI Analysis                                      │
│    └─> Root cause analysis                                 │
│    └─> Specific files to review                            │
│    └─> Code fix suggestions                                │
│    └─> Testing approach                                    │
│    └─> Deployment checklist                                │
└─────────────────────────────────────────────────────────────┘
```

### **What Makes This Powerful:**

1. **Real AI Analysis**: Uses OpenAI's most advanced GPT-4o model
2. **Deep Code Context**: Sends actual code snippets from your workspace
3. **Project-Aware**: AI understands your tech stack and components
4. **Comprehensive**: Analyzes bug + workspace together for accurate recommendations

### **Cost Estimation:**

OpenAI GPT-4o pricing (as of 2024):
- **Input tokens**: $2.50 per 1M tokens
- **Output tokens**: $10.00 per 1M tokens

Typical analysis:
- Input: ~8,000-15,000 tokens (bug + workspace context)
- Output: ~2,000-3,000 tokens (analysis)
- **Cost per analysis**: ~$0.02-$0.05 (2-5 cents)

### **Quota and Billing:**

⚠️ **Important**: You need an active OpenAI account with billing:

1. **Free Trial**: New accounts get $5 free credit (expires in 3 months)
2. **Pay-as-you-go**: Add payment method for continued access
3. **Rate Limits**: Free tier has lower rate limits than paid tier

**Check your status:**
- Usage: https://platform.openai.com/account/usage
- Billing: https://platform.openai.com/account/billing/overview
- API Keys: https://platform.openai.com/api-keys

### **Quota Exceeded Error:**

If you see this error:
```
❌ OPENAI API ERROR (429):
You exceeded your current quota, please check your plan and billing details.
```

**Resolution steps:**
1. **Check usage**: https://platform.openai.com/account/usage
2. **Add payment method**: https://platform.openai.com/account/billing/overview
3. **Generate new API key**: https://platform.openai.com/api-keys
4. **Wait for quota reset**: Free tier quotas reset monthly

**Automatic Fallback**: The tool automatically falls back to pattern-based analysis if OpenAI API fails.

---

### 3. Run the Application

```bash
python3 jira_analyzer-OPENAI.py
```

## Usage

### Analyzing Bugs

1. **Launch Application**
   ```bash
   python3 jira_analyzer-OPENAI.py
   ```

2. **Enter JIRA Bug ID**
   - Example: `PROJ-123`, `DEV-456`, etc.
   - Format depends on your JIRA project key
   
3. **Optional: View in Browser**
   - Click "View in Browser" to open JIRA in your web browser
   
4. **Analyze with OpenAI**
   - Click "🤖 Analyse with OpenAI"
   - Wait for OpenAI GPT-4o to analyze (5-15 seconds)
   
5. **Review AI-Powered Results**
   - **Bug Details**: Shows JIRA bug information
   - **AI Bug Fix Analysis**: Real AI analysis including:
     - Deep understanding of your bug in context of your codebase
     - Specific files from YOUR workspace that need attention
     - Root cause analysis with code-level insights
     - Recommended fixes with actual code examples
     - Testing approach tailored to your project
     - Deployment considerations

---

## 📊 **Example Output**

```
╔══════════════════════════════════════════════════════════════════╗
║      OPENAI GPT-4o AI ANALYSIS FOR RNS-123                      ║
╚══════════════════════════════════════════════════════════════════╝

PROJECT: RNS-SrsInternational
WORKSPACE: /home/user/project/SrsInternational
AI MODEL: GPT-4o

📁 WORKSPACE CONTEXT SENT TO AI:
   • Code files scanned: 42
   • File summaries: 15
   • Code samples: 8 (1500 chars each)
   • Total tokens: ~12,000
   
🤖 AI ANALYSIS:

📊 ROOT CAUSE ANALYSIS:
Based on the bug description and your workspace code, I've identified 
that this issue stems from improper connection handling in the 
SrsMessageQueue component. The code in `cpp/SrsMessageQueue.cpp` 
shows a pattern where connections are not being properly released 
after timeout scenarios.

� SPECIFIC FILES TO REVIEW:
1. cpp/SrsMessageQueue.cpp (Lines 145-178)
   • Connection timeout handling needs improvement
   • Missing proper cleanup in error path
   
2. cpp/SrsOCServiceHandler.cpp (Lines 89-112)
   • Service handler doesn't validate connection state
   • Should check isConnected() before operations

3. java/src/core/DatabaseManager.java (Lines 234-267)
   • Connection pool exhaustion during peak load
   • Consider implementing connection retry logic

� RECOMMENDED FIXES:

1. In SrsMessageQueue.cpp:
```cpp
// Add proper cleanup in timeout handler
void SrsMessageQueue::handleTimeout() {
    if (m_connection && m_connection->isOpen()) {
        m_connection->close();
        m_connection.reset();  // Release smart pointer
    }
    logWarning("Connection timeout, cleaned up resources");
}
```

2. In SrsOCServiceHandler.cpp:
```cpp
// Validate connection before use
bool SrsOCServiceHandler::processRequest(Request& req) {
    if (!m_queue || !m_queue->isConnected()) {
        return handleDisconnectedState();
    }
    // ... rest of processing
}
```

🧪 TESTING APPROACH:
1. Unit Tests:
   • Test timeout scenarios with mock connections
   • Verify proper cleanup in error paths
   • Test connection pool under load

2. Integration Tests:
   • Simulate network timeouts
   • Test with actual database under load
   • Monitor connection pool metrics

⚠️  POTENTIAL SIDE EFFECTS:
   • Performance: Adding connection validation adds ~2ms per request
   • Memory: Connection cleanup may delay resource release
   • Concurrency: Ensure thread-safe connection state checks

✅ DEPLOYMENT CHECKLIST:
   • Update connection pool configuration
   • Monitor connection metrics in production
   • Add alerts for connection pool exhaustion
   • Review logs for proper cleanup confirmation

═══════════════════════════════════════════════════════════════════
```

---

## Features Explained

### Real AI Analysis with OpenAI GPT-4o

The tool provides **real AI-powered analysis** by:
- Sending your bug details to OpenAI's most advanced GPT-4o model
- Including actual code snippets from your workspace (up to 8 files)
- Providing file summaries and workspace structure for context
- Getting AI-generated insights specific to YOUR codebase
- Receiving code-level recommendations from advanced AI
- Understanding complex interactions between components

### Deep Workspace Scanning

Enhanced workspace scanning for AI context:
- Scans up to **100 code files** (vs 20 in pattern-based version)
- Reads up to **1000 lines per file** (vs 100 in pattern-based version)
- Sends 15 file summaries to AI for broad context
- Includes 8 complete code samples (1500 chars each) for deep analysis
- AI sees actual code structure, patterns, and implementation details

### Customizable for Any Project

The analyzer is fully customizable for any type of application:
- **Web Applications**: React, Angular, Vue, Django, Flask, Spring Boot, .NET, etc.
- **Mobile Apps**: React Native, Flutter, iOS, Android
- **Desktop Applications**: Electron, Qt, JavaFX, WPF
- **Backend Services**: Node.js, Python, Java, C#, Go, Ruby
- **Data Systems**: Databases, Data Pipelines, ETL, Analytics
- **DevOps/Infrastructure**: Docker, Kubernetes, CI/CD, Cloud platforms
- **Embedded Systems**: IoT, Firmware, Real-time systems

### AI-Powered Fix Suggestions Include

1. **Deep Root Cause Analysis**
   - AI analyzes bug + code together
   - Identifies actual problematic code patterns
   - Explains why the bug occurs at code level
   - Considers component interactions

2. **Specific File and Line References**
   - AI points to exact files in YOUR workspace
   - Sometimes even specific line numbers
   - Explains what's wrong in each file
   - Prioritizes files by importance

3. **Code-Level Recommendations**
   - Actual code snippets for fixes
   - Language-specific best practices
   - Considers your tech stack and frameworks
   - Multiple solution approaches when applicable

4. **Comprehensive Testing Approach**
   - Unit tests specific to your bug
   - Integration test scenarios
   - Edge cases to consider
   - Test data suggestions

5. **Production Deployment Guidance**
   - Deployment risks and considerations
   - Monitoring recommendations
   - Rollback strategies
   - Performance impact analysis

## Troubleshooting

### "Failed to fetch JIRA bug"
- Verify JIRA credentials are properly set in the script
- Check internet connectivity
- Ensure JIRA bug ID is valid
- Verify you have access to the JIRA project

### "Please configure JIRA credentials"
- Edit the `jira_analyzer-OPENAI.py` file
- Update `JIRA_EMAIL` and `JIRA_API_TOKEN` in the hardcoded configuration section
- Save the file and restart the application

### "OpenAI API Error (401): Unauthorized"
- Your OpenAI API key is invalid or expired
- Generate a new key at: https://platform.openai.com/api-keys
- Update `OPENAI_API_KEY` in the script
- Ensure the key starts with `sk-proj-` or `sk-`

### "OpenAI API Error (429): Quota Exceeded"
- **You exceeded your current quota**
- This means your free trial expired or monthly limit reached

**Resolution steps:**
1. Check usage: https://platform.openai.com/account/usage
2. Add payment method: https://platform.openai.com/account/billing/overview
3. Generate new API key: https://platform.openai.com/api-keys
4. Or use the free pattern-based version: `jira_analyzer.py`

**Automatic Fallback**: The tool automatically falls back to pattern-based analysis if OpenAI fails

### "OpenAI API taking too long"
- OpenAI GPT-4o typically responds in 5-15 seconds
- Large codebases may take up to 30 seconds
- Check your internet connection
- Verify OpenAI service status: https://status.openai.com/

### No workspace files found in analysis
- Verify you're running from the project root directory
- Check `WORKSPACE_PATH` configuration in the script
- Ensure project has .java, .cpp, .py, .js, or .ts files
- Files in node_modules, .git, build, dist, target are automatically excluded

### GUI doesn't open
- Ensure `tkinter` is installed
- Check Python version (3.6+ required)
- Run: `python3 -m tkinter` to test tkinter installation

### Token Security
- Keep your script secure - it contains API tokens
- Don't commit the script with real tokens to public repositories
- Consider using environment variables for extra security
- Regenerate tokens if compromised
- **OpenAI API keys are sensitive** - treat them like passwords

## Example Workflow

1. Edit `jira_analyzer-OPENAI.py` and configure for your project (first time only)
2. Ensure OpenAI account has billing set up
3. Launch application: `python3 jira_analyzer-OPENAI.py`
4. Enter bug ID: `PROJ-123` (your project's bug ID format)
5. Click "🤖 Analyse with OpenAI"
6. Wait for GPT-4o analysis (5-15 seconds)
7. Review AI-powered bug analysis and specific file recommendations
8. Apply recommended fixes to your code
9. Test and validate changes

**Cost**: ~$0.02-$0.05 per analysis (2-5 cents)

## Support

For issues or questions:
1. Verify all prerequisites are installed
2. Check JIRA API token is valid
3. Verify OpenAI API key is valid and has quota
4. Check OpenAI billing: https://platform.openai.com/account/billing/overview
5. Ensure JIRA URL is correct
6. Review project configuration matches your tech stack
7. Check Python and library versions
8. Verify OpenAI service status: https://status.openai.com/

## Use Cases

This tool is perfect for:
- **Developers**: AI-powered bug analysis with code-level insights
- **Team Leads**: Understand bug impact with AI assistance
- **QA Engineers**: Better understand bugs through AI analysis
- **New Team Members**: Learn codebase through AI-explained bugs
- **Code Reviews**: Get AI insights during bug fix reviews
- **Complex Bugs**: Leverage AI for hard-to-diagnose issues

## Comparison: OpenAI vs Pattern-Based Version

### jira_analyzer-OPENAI.py (This Version)
✅ **Real AI analysis** using GPT-4o
✅ **Code-level insights** from actual AI
✅ **Specific file/line recommendations**
✅ **Deep understanding** of code interactions
✅ **Advanced reasoning** for complex bugs
❌ **Costs money**: ~$0.02-$0.05 per analysis
❌ **Requires internet** and OpenAI account

### jira_analyzer.py (Pattern-Based Version)
✅ **Completely free** - no API costs
✅ **No quota limits** - unlimited usage
✅ **Fast** - instant analysis
✅ **Privacy** - no data sent externally
✅ **80%+ accuracy** for common bugs
❌ **Pattern-based** - not true AI
❌ **Less specific** - general recommendations

**Recommendation**: 
- Use **OpenAI version** for complex/critical bugs
- Use **pattern-based version** for quick analysis or cost savings

## Use Cases

This tool is perfect for:
- **Developers**: Quick bug analysis and fix suggestions
- **Team Leads**: Understand bug impact and estimate effort
- **QA Engineers**: Better understand bug context for testing
- **New Team Members**: Learn about codebase through bug analysis
- **Code Reviews**: Get additional insights during bug fix reviews

## License

Open source - use and modify as needed for your projects!

## Advanced Usage

### Customizing Analysis Patterns

The tool includes automatic fallback to pattern-based analysis if OpenAI fails. You can customize:
1. Workspace scanning depth (currently 100 files, 1000 lines each)
2. Number of files sent to AI (currently 15 summaries + 8 samples)
3. Token limits for AI responses (currently 3000 tokens)
4. AI temperature setting (currently 0.7 for balanced output)

### Integration Options

The tool can be extended to integrate with:
- **Alternative AI Models**: Claude, Google Gemini, Azure OpenAI
- **Local LLMs**: Ollama, LLaMA for offline/private analysis
- Code analysis tools (SonarQube, ESLint, etc.)
- CI/CD pipelines for automated bug analysis
- Slack/Teams for bug notifications
- Git repositories for blame analysis
- Custom AI prompts for specific bug types

### Cost Optimization

To reduce OpenAI costs:
1. **Use pattern-based fallback** for simple bugs
2. **Scan fewer files**: Reduce from 100 to 50 files
3. **Shorter code samples**: Reduce from 1500 to 1000 chars
4. **Lower max tokens**: Reduce from 3000 to 2000
5. **Batch multiple bugs** before analysis (manual approach)
6. **Use GPT-4o-mini** instead of GPT-4o (edit model name in script)

## Security Notes

- All API tokens are hardcoded in the script
- Keep `jira_analyzer-OPENAI.py` secure and private
- Don't commit the script with real tokens to public repositories
- Consider creating a template version with placeholder tokens for sharing
- Use read-only JIRA tokens when possible
- Regularly rotate API tokens
- **OpenAI API keys are highly sensitive** - treat like passwords
- **Your code is sent to OpenAI** - ensure compliance with your organization's policies
- Consider using Azure OpenAI for enterprise scenarios with data residency requirements

## Quick Start Guide

```bash
# 1. Install dependencies
pip install requests Pillow

# 2. Get OpenAI API Key
# Go to: https://platform.openai.com/api-keys
# Create new secret key
# Add payment method: https://platform.openai.com/account/billing/overview

# 3. Edit the script and configure for your project
nano jira_analyzer-OPENAI.py  # or use your preferred editor

# 4. Update these sections in the script:
#    JIRA_BASE_URL = "https://your-company.atlassian.net"
#    JIRA_EMAIL = "your.email@company.com"
#    JIRA_API_TOKEN = "your_actual_token"
#    OPENAI_API_KEY = "sk-proj-your_actual_key"
#    
#    PROJECT_NAME = "Your Project Name"
#    PROJECT_TECHNOLOGIES = ["Tech1", "Tech2", ...]
#    PROJECT_COMPONENTS = ["Component1", "Component2", ...]

# 5. Run the application
python3 jira_analyzer-OPENAI.py

# 6. Enter JIRA bug ID (e.g., PROJ-123) and click "🤖 Analyse with OpenAI"
# 7. Wait 5-15 seconds for AI analysis
# 8. Cost: ~$0.02-$0.05 per analysis
```

## Example Configurations

### Web Application (React + Node.js + PostgreSQL)
```python
PROJECT_NAME = "E-Commerce Platform"
PROJECT_TECHNOLOGIES = [
    "React", "Node.js", "Express", "PostgreSQL", "Redis",
    "Docker", "Kubernetes", "AWS", "TypeScript"
]
PROJECT_COMPONENTS = [
    "Frontend UI", "Backend API", "Database", "Authentication",
    "Payment Gateway", "Order Processing", "Inventory Management",
    "Notification Service", "Admin Dashboard"
]
```

### Mobile Application (React Native)
```python
PROJECT_NAME = "Social Media App"
PROJECT_TECHNOLOGIES = [
    "React Native", "Node.js", "MongoDB", "Firebase",
    "Redux", "GraphQL", "AWS S3", "Push Notifications"
]
PROJECT_COMPONENTS = [
    "Mobile App", "Backend API", "Database", "Authentication",
    "Media Storage", "Real-time Chat", "User Profiles",
    "Feed Algorithm", "Search Service"
]
```

### Microservices Architecture
```python
PROJECT_NAME = "Banking Platform"
PROJECT_TECHNOLOGIES = [
    "Java", "Spring Boot", "Kafka", "PostgreSQL", "Redis",
    "Docker", "Kubernetes", "Elasticsearch", "Prometheus"
]
PROJECT_COMPONENTS = [
    "API Gateway", "User Service", "Account Service",
    "Transaction Service", "Notification Service", "Audit Service",
    "Authentication", "Message Queue", "Database Cluster"
]
```

## Frequently Asked Questions (FAQ)

### Q: How much does it cost per analysis?
**A**: Approximately **$0.02-$0.05** (2-5 cents) per bug analysis using GPT-4o.

### Q: What if I run out of OpenAI quota?
**A**: The tool automatically falls back to pattern-based analysis. You can also use the free `jira_analyzer.py` version.

### Q: Is my code secure when sent to OpenAI?
**A**: OpenAI API calls are encrypted via HTTPS. However, your code is processed by OpenAI's servers. For sensitive code, consider:
- Using Azure OpenAI with private deployment
- Using the pattern-based version (`jira_analyzer.py`)
- Using local LLMs (Ollama, LLaMA)

### Q: How long does analysis take?
**A**: Typically **5-15 seconds** with OpenAI GPT-4o. Complex codebases may take up to 30 seconds.

### Q: Can I use GPT-3.5 to save money?
**A**: Yes! Edit the script and change `model: "gpt-4o"` to `model: "gpt-3.5-turbo"`. This reduces cost to ~$0.001-$0.003 per analysis but with lower quality.

### Q: What's the difference between this and GitHub Copilot?
**A**: GitHub Copilot Chat API doesn't support Personal Access Tokens. This tool uses OpenAI's public API instead, which provides similar AI capabilities for bug analysis.

### Q: Can I analyze multiple bugs at once?
**A**: Currently, the tool analyzes one bug at a time. You can run it multiple times for different bugs.

### Q: What if my workspace is very large (1000+ files)?
**A**: The tool scans up to 100 files and sends 15 summaries + 8 samples to AI. This balances comprehensive analysis with API costs.

## Alternatives

If OpenAI doesn't work for you:

### Free Alternatives:
1. **jira_analyzer.py** (included) - Pattern-based analysis, no API, free
2. **Ollama** - Local LLM, completely free, private
3. **Groq** - Free API with higher limits than OpenAI free tier
4. **Google Gemini** - Free tier available

### Paid Alternatives:
1. **Claude API** (Anthropic) - Similar to OpenAI, sometimes better for code
2. **Azure OpenAI** - Enterprise version with data residency
3. **AWS Bedrock** - Multiple models, enterprise features

## License

Open source - use and modify as needed for your projects!
