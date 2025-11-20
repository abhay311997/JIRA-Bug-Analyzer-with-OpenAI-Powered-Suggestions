#!/usr/bin/env python3
"""
JIRA Bug Analyzer with GitHub Copilot Integration
This script provides a GUI to analyze JIRA bugs and get AI-powered bug fix suggestions.

All configurations are hardcoded - no external config files needed!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk
import os
import json

class JiraAnalyzerGUI:
    # ========== HARDCODED CONFIGURATION ==========
    # Configure your tokens and project details here
    JIRA_BASE_URL = "https://abc.atlassian.net/"  # Replace with your JIRA URL
    JIRA_EMAIL = "name@org.com"  # Replace with your JIRA email
    JIRA_API_TOKEN = ""  # Replace with your JIRA API token
    OPENAI_API_KEY = ""  # Your OpenAI API Key
    WORKSPACE_PATH = str(Path.cwd())  # Current directory
    
    # Project-specific configuration (customize for your project)
    PROJECT_NAME = "project name "  # Your project name
    PROJECT_TECHNOLOGIES = [
        "Java", "C++"
    ]  # List technologies used in your project like ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "Django", "Spring Boot", "Docker", "Kubernetes"]
    PROJECT_COMPONENTS = [
        "Frontend", "Backend", "Database", "API", "Cache"
    ]  # List main components of your project like ["Frontend", "Backend", "Database", "API", "Authentication", "Cache", "Message Queue", "File Processing"]
    # =============================================
    
    def __init__(self, root):
        self.root = root
        self.root.title("JIRA Bug Analyzer with Copilot")
        self.root.geometry("900x700")
        
        # Use hardcoded configuration
        self.config = {
            "jira_base_url": self.JIRA_BASE_URL,
            "jira_email": self.JIRA_EMAIL,
            "jira_api_token": self.JIRA_API_TOKEN,
            "openai_api_key": self.OPENAI_API_KEY,
            "workspace_path": self.WORKSPACE_PATH
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI components"""
        # Main Analysis Frame (no tabs needed)
        analysis_frame = ttk.Frame(self.root)
        analysis_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add logo at the top
        self.add_logo(analysis_frame)
        
        self.setup_analysis_tab(analysis_frame)
    
    def add_logo(self, parent):
        """Add company logo at the top of the GUI"""
        try:
            # Download logo symbol from URL
            logo_url = "https://blog.org.com/hubfs/logo.png"
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()
            
            # Load image
            image_data = BytesIO(response.content)
            symbol_img = Image.open(image_data)
            
            # Resize logo symbol (smaller size)
            symbol_width = 350
            ratio = symbol_width / symbol_img.width
            symbol_height = int(symbol_img.height * ratio)
            symbol_img = symbol_img.resize((symbol_width, symbol_height), Image.Resampling.LANCZOS)
            
            # Crop to show only left half of the logo
            crop_width = symbol_width // 7
            symbol_img = symbol_img.crop((0, 0, crop_width, symbol_height))
            
            # Convert to PhotoImage
            self.logo_image = ImageTk.PhotoImage(symbol_img)
            
            # Create logo frame with white background - centered with minimal height
            logo_frame = tk.Frame(parent, bg='white')
            logo_frame.pack(pady=(0, 5), fill='x')
            
            # Container for horizontal layout - centered
            logo_container = tk.Frame(logo_frame, bg='white')
            logo_container.pack(anchor='center', pady=(2, 2))
            
            # Left side: M symbol with minimal padding
            logo_label = tk.Label(logo_container, image=self.logo_image, bg='white')
            logo_label.pack(side='left', padx=(0, 2), pady=(5, 0))
            
            # Right side: Text frame (Company_name + tagline)
            text_frame = tk.Frame(logo_container, bg='white')
            text_frame.pack(side='left')
            
            # "XYZ Organisation" text in larger font
            company_name = tk.Label(text_frame, text="XYZ Organisation", 
                                   font=('Arial', 40, 'normal'), 
                                   fg='black', bg='white')
            company_name.pack(anchor='w', pady=(0, 0))
            
            # Tagline in smaller font below - shifted right and closer to top
            tagline = tk.Label(text_frame, text="Organisation Tag Line", 
                             font=('Arial', 10), 
                             fg='black', bg='white')
            tagline.pack(anchor='w', padx=(20, 0), pady=(0, 5))
            
        except Exception as e:
            # If logo fails to load, just continue without it
            print(f"Could not load logo: {e}")
    
    def setup_analysis_tab(self, parent):
        """Setup the main analysis tab"""
        # JIRA Bug ID Input Section
        input_frame = ttk.LabelFrame(parent, text="JIRA Bug Details", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(input_frame, text="JIRA Bug ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.bug_id_entry = ttk.Entry(input_frame, width=30, font=('Arial', 11))
        self.bug_id_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        self.bug_id_entry.insert(0, "")  # Placeholder example
        
        # View in Browser Button
        view_button = ttk.Button(input_frame, text="View in Browser", 
                                 command=self.view_in_browser)
        view_button.grid(row=0, column=2, padx=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Analyze Button
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.analyze_button = ttk.Button(button_frame, text="🤖 Analyse with OpenAI", 
                                         command=self.analyze_bug,
                                         style='Accent.TButton')
        self.analyze_button.pack(pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(button_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(parent, text="Analysis Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Bug Details Section
        ttk.Label(results_frame, text="Bug Details:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.bug_details_text = scrolledtext.ScrolledText(results_frame, height=8, 
                                                          wrap=tk.WORD, font=('Courier', 9))
        self.bug_details_text.pack(fill='both', expand=True, pady=5)
        
        # Bug Fix Suggestions Section
        ttk.Label(results_frame, text="AI-Powered Bug Fix Suggestions:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.bug_fix_text = scrolledtext.ScrolledText(results_frame, height=12, 
                                                      wrap=tk.WORD, font=('Courier', 9))
        self.bug_fix_text.pack(fill='both', expand=True, pady=5)
        
        # Status Bar
        self.status_label = ttk.Label(parent, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(fill='x', side='bottom', padx=10, pady=5)
    
    def view_in_browser(self):
        """Open JIRA bug in browser"""
        bug_id = self.bug_id_entry.get().strip()
        if bug_id:
            url = f"{self.config['jira_base_url']}/browse/{bug_id}"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Warning", "Please enter a JIRA Bug ID")
    
    def fetch_jira_bug(self, bug_id):
        """Fetch bug details from JIRA"""
        try:
            url = f"{self.config['jira_base_url']}/rest/api/3/issue/{bug_id}"
            
            auth = HTTPBasicAuth(self.config['jira_email'], self.config['jira_api_token'])
            headers = {"Accept": "application/json"}
            
            response = requests.get(url, headers=headers, auth=auth, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch JIRA bug: {str(e)}")
    
    def format_bug_details(self, bug_data):
        """Format bug details for display"""
        try:
            fields = bug_data.get('fields', {})
            
            # Handle description - it can be a string or a dict (ADF format)
            description_raw = fields.get('description', 'No description available')
            if isinstance(description_raw, dict):
                description = self.extract_text_from_adf(description_raw)
            else:
                description = str(description_raw) if description_raw else 'No description available'
            
            # Handle environment field
            environment_raw = fields.get('environment')
            if isinstance(environment_raw, dict):
                environment = self.extract_text_from_adf(environment_raw)
            else:
                environment = str(environment_raw) if environment_raw else 'Not specified'
            
            details = f"""
Bug ID: {bug_data.get('key', 'N/A')}
Summary: {fields.get('summary', 'N/A')}
Status: {fields.get('status', {}).get('name', 'N/A')}
Priority: {fields.get('priority', {}).get('name', 'N/A')}
Reporter: {fields.get('reporter', {}).get('displayName', 'N/A')}
Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}
Created: {fields.get('created', 'N/A')[:10]}
Updated: {fields.get('updated', 'N/A')[:10]}

Description:
{description}

Environment:
{environment}

Components:
{', '.join([c.get('name', '') for c in fields.get('components', [])]) or 'None'}

Labels:
{', '.join(fields.get('labels', [])) or 'None'}
            """.strip()
            
            return details
        except Exception as e:
            return f"Error formatting bug details: {str(e)}"
    
    def generate_copilot_analysis(self, bug_data):
        """Generate AI-powered bug fix suggestions using OpenAI API with workspace context"""
        try:
            fields = bug_data.get('fields', {})
            bug_id = bug_data.get('key', 'Unknown')
            summary = fields.get('summary', '')
            
            # Handle description - it can be a string or a dict (ADF format)
            description_raw = fields.get('description', '')
            if isinstance(description_raw, dict):
                # JIRA API v3 uses Atlassian Document Format (ADF)
                description = self.extract_text_from_adf(description_raw)
            else:
                description = str(description_raw) if description_raw else ''
            
            # Scan workspace for relevant code files
            self.status_label.config(text="Scanning workspace for relevant code files...")
            self.root.update()
            workspace_context = self.scan_workspace_files()
            
            # Call OpenAI API for real AI analysis
            self.status_label.config(text="Analyzing with OpenAI GPT-4...")
            self.root.update()
            analysis = self.call_openai_api(bug_id, summary, description, workspace_context)
            
            return analysis
            
        except Exception as e:
            return f"Error generating AI analysis: {str(e)}"
    
    def scan_workspace_files(self):
        """Scan workspace and collect relevant code files"""
        workspace_path = Path(self.config['workspace_path'])
        code_extensions = {'.java', '.cpp', '.h', '.py', '.js', '.ts', '.jsx', '.tsx', '.c', '.cc'}
        
        relevant_files = []
        file_count = 0
        max_files = 100  # Limit to avoid token overflow
        max_lines_per_file = 1000  # Limit lines per file
        
        try:
            for ext in code_extensions:
                if file_count >= max_files:
                    break
                    
                for file_path in workspace_path.rglob(f'*{ext}'):
                    if file_count >= max_files:
                        break
                    
                    # Skip common directories to ignore
                    if any(skip in file_path.parts for skip in ['node_modules', '.git', 'build', 'dist', 'target', '__pycache__']):
                        continue
                    
                    try:
                        # Read file content
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()[:max_lines_per_file]
                            content = ''.join(lines)
                            
                        relative_path = file_path.relative_to(workspace_path)
                        relevant_files.append({
                            'path': str(relative_path),
                            'content': content,
                            'lines': len(lines)
                        })
                        file_count += 1
                    except Exception as e:
                        continue
            
            return {
                'total_files': file_count,
                'files': relevant_files,
                'workspace_structure': self.get_workspace_structure()
            }
        except Exception as e:
            return {
                'total_files': 0,
                'files': [],
                'error': str(e)
            }
    
    def get_workspace_structure(self):
        """Get high-level workspace structure"""
        workspace_path = Path(self.config['workspace_path'])
        structure = []
        
        try:
            for item in workspace_path.iterdir():
                if item.name.startswith('.'):
                    continue
                if item.is_dir():
                    structure.append(f"[DIR] {item.name}/")
                else:
                    structure.append(f"[FILE] {item.name}")
        except Exception:
            pass
        
        return structure[:30]  # Limit to first 30 items
    
    def call_openai_api(self, bug_id, summary, description, workspace_context):
        """Call OpenAI API for real AI-powered bug analysis"""
        try:
            openai_api_key = self.config.get('openai_api_key', '').strip()
            
            if not openai_api_key:
                raise Exception("No OpenAI API key available. Please configure OPENAI_API_KEY in the script.")
            
            # OpenAI API endpoint
            api_url = "https://api.openai.com/v1/chat/completions"
            
            # Construct comprehensive prompt with workspace context
            workspace_files_summary = "\n".join([
                f"- {f['path']} ({f['lines']} lines)" 
                for f in workspace_context.get('files', [])[:15]
            ])
            
            workspace_structure = "\n".join(workspace_context.get('workspace_structure', []))
            
            # Include sample code from relevant files
            code_samples = ""
            for idx, file_info in enumerate(workspace_context.get('files', [])[:8], 1):
                code_samples += f"\n--- File {idx}: {file_info['path']} ---\n"
                code_samples += file_info['content'][:1500]  # First 1500 chars
                code_samples += "\n"
            
            prompt = f"""You are an expert software engineer analyzing a JIRA bug with access to the actual codebase.

**JIRA BUG DETAILS:**
Bug ID: {bug_id}
Summary: {summary}
Description: {description}

**PROJECT CONTEXT:**
- Project: {self.PROJECT_NAME}
- Technologies: {', '.join(self.PROJECT_TECHNOLOGIES)}
- Components: {', '.join(self.PROJECT_COMPONENTS)}
- Workspace: {self.config['workspace_path']}

**WORKSPACE ANALYSIS:**
Total Files Scanned: {workspace_context.get('total_files', 0)}

Workspace Structure:
{workspace_structure}

Relevant Code Files:
{workspace_files_summary}

**CODE SAMPLES FROM WORKSPACE:**
{code_samples}

**TASK:**
Analyze this bug in the context of the actual codebase above. Provide a comprehensive analysis with:

1. **Root Cause Analysis**: Based on the code patterns observed, identify the likely root cause
2. **Affected Files/Components**: List specific files from the workspace that might be affected
3. **Detailed Fix Recommendations**: 
   - Provide step-by-step fix recommendations
   - Include code examples that match the project's technology stack
   - Suggest specific changes to the files listed above
4. **Testing Approach**: Recommend unit tests, integration tests specific to this codebase
5. **Potential Side Effects**: Warn about potential impacts on related components
6. **Implementation Steps**: Provide a clear action plan

Focus on providing actionable, code-specific suggestions based on the actual project structure and code samples provided.
"""

            # OpenAI API headers
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Payload for OpenAI
            payload = {
                "model": "gpt-4o-2024-11-20",  # Using latest GPT-4o model (Nov 2024)
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert software engineer specializing in bug analysis and debugging. Provide detailed, actionable suggestions based on the codebase provided. Format your response clearly with sections and bullet points."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 3000
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                ai_analysis = result['choices'][0]['message']['content']
                
                # Add metadata about workspace analysis
                full_analysis = f"""
╔══════════════════════════════════════════════════════════════════╗
║     AI-POWERED BUG FIX ANALYSIS FOR {bug_id} (GPT-4o-2024-11-20) ║
╚══════════════════════════════════════════════════════════════════╝

PROJECT: {self.PROJECT_NAME}
WORKSPACE: {self.config['workspace_path']}

📁 WORKSPACE SCAN RESULTS:
   • Total files analyzed: {workspace_context.get('total_files', 0)}
   • File types: {', '.join(self.PROJECT_TECHNOLOGIES)}
   • Workspace structure: {len(workspace_context.get('workspace_structure', []))} items

═══════════════════════════════════════════════════════════════════

{ai_analysis}

═══════════════════════════════════════════════════════════════════

💡 NOTE: This analysis was generated by OpenAI GPT-4o (Nov 2024) based on:
   - JIRA bug details (Bug ID, Summary, Description)
   - Actual workspace code structure
   - {workspace_context.get('total_files', 0)} source code files scanned
   - Project technologies: {', '.join(self.PROJECT_TECHNOLOGIES)}
   - Code samples from key files

═══════════════════════════════════════════════════════════════════
"""
                return full_analysis
            else:
                # Handle API errors
                error_msg = f"OpenAI API Error: {response.status_code}"
                error_detail = ""
                try:
                    error_json = response.json()
                    error_message = error_json.get('error', {}).get('message', str(error_json))
                    error_detail = f"\nDetails: {error_message}"
                    
                    # Special handling for quota exceeded (429)
                    if response.status_code == 429:
                        error_detail += """

🔴 QUOTA EXCEEDED - ACTION REQUIRED:
   
   Your OpenAI API key has exceeded its usage quota.
   
   📋 Steps to resolve:
   
   1. Check your OpenAI account:
      https://platform.openai.com/account/usage
   
   2. Check billing and add payment method:
      https://platform.openai.com/account/billing/overview
   
   3. Options:
      • Add a payment method if free trial expired
      • Upgrade your plan for higher limits
      • Wait for quota reset (monthly cycle)
      • Generate a new API key
   
   4. Current API key starts with: {}...
   
   For now, using fallback pattern-based analysis.
""".format(openai_api_key[:20] if openai_api_key else "N/A")
                except:
                    error_detail = f"\nResponse: {response.text[:200]}"
                
                print(f"❌ OpenAI API Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                
                # Fallback to pattern-based analysis if API fails
                fallback = self.generate_intelligent_analysis(bug_id, summary, description)
                return f"""
⚠️  OpenAI API unavailable ({error_msg}{error_detail})
Providing pattern-based analysis instead:

{fallback}
"""
        except Exception as e:
            # Fallback to pattern-based analysis
            print(f"❌ Exception calling OpenAI: {str(e)}")
            fallback = self.generate_intelligent_analysis(bug_id, summary, description)
            return f"""
⚠️  OpenAI API Error: {str(e)}
Providing pattern-based analysis instead:

{fallback}
"""
    
    def extract_text_from_adf(self, adf_content):
        """Extract plain text from Atlassian Document Format (ADF)"""
        try:
            text_parts = []
            
            def extract_text(node, depth=0):
                if isinstance(node, dict):
                    node_type = node.get('type', '')
                    
                    # Handle paragraph breaks
                    if node_type == 'paragraph' and depth > 0:
                        text_parts.append('\n')
                    
                    # Handle text nodes
                    if node_type == 'text':
                        text_parts.append(node.get('text', ''))
                    
                    # Handle hard breaks
                    if node_type == 'hardBreak':
                        text_parts.append('\n')
                    
                    # Handle list items
                    if node_type in ['bulletList', 'orderedList']:
                        text_parts.append('\n')
                    
                    if node_type == 'listItem':
                        text_parts.append('\n• ')
                    
                    # Recursively process content
                    if 'content' in node:
                        for child in node['content']:
                            extract_text(child, depth + 1)
                    
                    # Add paragraph break after paragraph
                    if node_type == 'paragraph':
                        text_parts.append('\n')
                        
                elif isinstance(node, list):
                    for item in node:
                        extract_text(item, depth)
            
            extract_text(adf_content)
            result = ''.join(text_parts).strip()
            # Clean up multiple consecutive newlines
            import re
            result = re.sub(r'\n{3,}', '\n\n', result)
            return result
        except Exception as e:
            return f"[Could not parse description: {str(e)}]"
    
    def generate_intelligent_analysis_with_context(self, bug_id, summary, description, workspace_context):
        """Generate intelligent bug fix suggestions WITH workspace context"""
        
        # Get the base analysis
        base_analysis = self.generate_intelligent_analysis(bug_id, summary, description)
        
        # Add workspace-specific insights
        workspace_files = workspace_context.get('files', [])
        total_files = workspace_context.get('total_files', 0)
        
        workspace_section = f"""

📁 WORKSPACE ANALYSIS:
   • Total code files scanned: {total_files}
   • Technologies detected: {', '.join(self.PROJECT_TECHNOLOGIES)}
   
🔍 RELEVANT FILES IN WORKSPACE:
"""
        
        if workspace_files:
            for idx, file_info in enumerate(workspace_files[:10], 1):
                workspace_section += f"   {idx}. {file_info['path']} ({file_info['lines']} lines)\n"
            
            workspace_section += f"""

💡 RECOMMENDED FILES TO CHECK:
   Based on the bug description and workspace scan, start by reviewing:
"""
            # Match keywords from bug to files
            text_lower = (summary + " " + description).lower()
            matched_files = []
            
            for file_info in workspace_files:
                file_path_lower = file_info['path'].lower()
                # Check if bug keywords match file names
                if any(keyword in file_path_lower for keyword in ['handler', 'manager', 'service', 'controller', 'processor', 'worker']):
                    matched_files.append(file_info['path'])
            
            if matched_files:
                for file_path in matched_files[:5]:
                    workspace_section += f"   • {file_path}\n"
            else:
                workspace_section += f"   • Review the files listed above that match the bug's component/area\n"
        else:
            workspace_section += "   ⚠️  No code files found in workspace scan\n"
        
        # Insert workspace section after the header
        enhanced_analysis = base_analysis.replace(
            f"PROJECT: {self.PROJECT_NAME}",
            f"PROJECT: {self.PROJECT_NAME}{workspace_section}"
        )
        
        return enhanced_analysis
    
    def generate_intelligent_analysis(self, bug_id, summary, description):
        """Generate intelligent bug fix suggestions based on project context"""
        
        # Ensure description is a string
        if not isinstance(description, str):
            description = str(description)
        
        # Analyze keywords in summary and description
        text = (summary + " " + description).lower()
        
        analysis = f"""
╔══════════════════════════════════════════════════════════════════╗
║           AI-POWERED BUG FIX ANALYSIS FOR {bug_id}              ║
╚══════════════════════════════════════════════════════════════════╝

PROJECT: {self.PROJECT_NAME}
WORKSPACE: {self.config['workspace_path']}

📊 ROOT CAUSE ANALYSIS:
"""
        
        # Generic issue pattern detection
        issues_found = False
        
        if any(keyword in text for keyword in ['memory', 'leak', 'crash', 'segfault', 'null pointer', 'nullptr']):
            analysis += """
   • Potential memory management issue detected
   • May involve improper pointer handling or resource cleanup
   • Check for null pointer dereferences and memory leaks
"""
            issues_found = True
        
        if any(keyword in text for keyword in ['performance', 'slow', 'timeout', 'latency', 'hang', 'freeze']):
            analysis += """
   • Performance bottleneck identified
   • May involve database queries, network calls, or inefficient algorithms
   • Review transaction processing, caching, and optimization
"""
            issues_found = True
        
        if any(keyword in text for keyword in ['database', 'sql', 'query', 'connection', 'deadlock']):
            analysis += """
   • Database connectivity or query issue
   • May involve connection pool exhaustion or query optimization
   • Review database transaction handling and indexing
"""
            issues_found = True
        
        if any(keyword in text for keyword in ['authentication', 'login', 'auth', 'permission', 'access denied']):
            analysis += """
   • Authentication/Authorization issue detected
   • May involve incorrect credentials, tokens, or permissions
   • Review security configuration and access control logic
"""
            issues_found = True
        
        if any(keyword in text for keyword in ['api', 'rest', 'endpoint', 'http', '404', '500', 'response']):
            analysis += """
   • API/REST endpoint issue detected
   • May involve incorrect routing, request/response handling
   • Review API controllers, middleware, and error handling
"""
            issues_found = True
        
        if any(keyword in text for keyword in ['frontend', 'ui', 'display', 'render', 'css', 'javascript']):
            analysis += """
   • Frontend/UI issue detected
   • May involve rendering problems, styling, or client-side logic
   • Review component logic, state management, and CSS
"""
            issues_found = True
        
        if any(keyword in text for keyword in ['error', 'exception', 'stack trace', 'failed']):
            analysis += """
   • Exception/Error handling issue detected
   • May involve unhandled exceptions or improper error propagation
   • Review try-catch blocks and error handling middleware
"""
            issues_found = True
        
        if not issues_found:
            analysis += """
   • General bug analysis required
   • Review the bug description and affected functionality
   • Identify the specific area of code related to the issue
"""
        
        analysis += f"""

🎯 AFFECTED COMPONENTS:

Based on your project components: {', '.join(self.PROJECT_COMPONENTS)}

"""
        
        # Suggest components based on keywords
        component_suggestions = []
        for component in self.PROJECT_COMPONENTS:
            if component.lower() in text:
                component_suggestions.append(f"   • {component} component")
        
        if component_suggestions:
            analysis += '\n'.join(component_suggestions) + "\n"
        else:
            analysis += """   • Review all relevant components mentioned in the bug description
   • Check files related to the reported functionality
   • Examine recent code changes in the affected area
"""
        
        analysis += f"""

🔧 RECOMMENDED FIXES:

1. Code Review Priority:
   • Review error handling in affected components
   • Check for proper resource cleanup (memory, connections, locks)
   • Validate input parameters and boundary conditions
   • Ensure thread-safety in concurrent operations
   • Review recent changes in the affected area

2. Implementation Steps:
   a) Add comprehensive logging at critical points
   b) Implement defensive programming checks
   c) Add unit tests for edge cases and bug scenario
   d) Review and optimize relevant queries/algorithms
   e) Update error handling with proper exception management
   f) Add validation for inputs and outputs

3. Technology-Specific Considerations:
"""
        
        # Add technology-specific recommendations
        for tech in self.PROJECT_TECHNOLOGIES:
            tech_lower = tech.lower()
            if tech_lower in text or any(t.lower() in text for t in ['bug', 'error', 'issue']):
                if 'python' in tech_lower:
                    analysis += """
   • Python: Check for proper exception handling, use type hints
"""
                elif 'java' in tech_lower:
                    analysis += """
   • Java: Review try-catch blocks, check for resource leaks
"""
                elif 'c++' in tech_lower or 'cpp' in tech_lower:
                    analysis += """
   • C++: Verify memory management, use smart pointers
"""
                elif 'javascript' in tech_lower or 'js' in tech_lower or 'node' in tech_lower:
                    analysis += """
   • JavaScript/Node.js: Check async/await usage, handle promises
"""
                elif 'react' in tech_lower:
                    analysis += """
   • React: Review component lifecycle, state management
"""
                elif 'database' in tech_lower or 'sql' in tech_lower:
                    analysis += """
   • Database: Optimize queries, check indexes, review transactions
"""
                elif 'docker' in tech_lower or 'kubernetes' in tech_lower:
                    analysis += """
   • Container/Orchestration: Review configurations, resource limits
"""

        analysis += """

4. Generic Code Pattern Example:
   ```
   // Add proper error handling and validation
   function processRequest(input) {
       // Validate input
       if (!isValid(input)) {
           logger.error("Invalid input detected");
           throw new ValidationError("Invalid input");
       }
       
       try {
           // Main business logic
           const result = performOperation(input);
           
           // Validate output
           if (!isValidResult(result)) {
               throw new ProcessingError("Invalid result");
           }
           
           return result;
       } catch (error) {
           logger.error("Error processing request", error);
           // Proper error handling
           throw error;
       } finally {
           // Cleanup resources
           cleanup();
       }
   }
   ```

🧪 TESTING APPROACH:

1. Unit Testing:
   • Create test cases for the specific bug scenario
   • Test boundary conditions and edge cases
   • Validate error handling paths
   • Mock external dependencies
   • Aim for high code coverage

2. Integration Testing:
   • Test with real data similar to the bug scenario
   • Verify end-to-end workflow
   • Check database state consistency
   • Monitor logs for errors or warnings
   • Test with different environments

3. Regression Testing:
   • Run existing test suite
   • Verify no side effects on other components
   • Check backward compatibility
   • Test related features

⚠️  POTENTIAL SIDE EFFECTS:

   • Performance impact on related operations
   • Changes may affect dependent components
   • Database schema changes require migration
   • API changes need version management
   • Configuration changes may require restart
   • Caching behavior might change

📋 DEPLOYMENT CHECKLIST:

   ✓ Code review completed
   ✓ Unit tests added and passing
   ✓ Integration tests executed
   ✓ Performance impact assessed
   ✓ Documentation updated
   ✓ Configuration changes documented
   ✓ Rollback plan prepared
   ✓ Monitoring and alerts configured
   ✓ Stakeholders notified

🔗 RECOMMENDED NEXT STEPS:

   1. Review the workspace files related to the issue
   2. Add comprehensive logging to understand the flow
   3. Write failing tests that reproduce the bug
   4. Implement the fix incrementally
   5. Validate with the test cases
   6. Get code review from team members
   7. Test in staging environment
   8. Deploy with monitoring

═══════════════════════════════════════════════════════════════════

💡 RECOMMENDATION:
   Start with thorough code review and add comprehensive logging
   before implementing fixes. Ensure all changes are backed by
   unit tests and validated in a staging environment.

═══════════════════════════════════════════════════════════════════
"""
        
        return analysis
    
    def analyze_bug(self):
        """Main analysis function"""
        bug_id = self.bug_id_entry.get().strip()
        
        if not bug_id:
            messagebox.showwarning("Warning", "Please enter a JIRA Bug ID")
            return
        
        # Validate configuration
        if not self.config.get('jira_email') or not self.config.get('jira_api_token'):
            messagebox.showerror("Error", 
                               "Please configure JIRA credentials in the Configuration tab")
            return
        
        # Clear previous results
        self.bug_details_text.delete(1.0, tk.END)
        self.bug_fix_text.delete(1.0, tk.END)
        
        # Disable button and show progress
        self.analyze_button.config(state='disabled')
        self.progress.start()
        self.status_label.config(text=f"Fetching JIRA bug {bug_id}...")
        self.root.update()
        
        try:
            # Fetch JIRA bug
            self.status_label.config(text=f"Analyzing {bug_id} with JIRA API...")
            self.root.update()
            bug_data = self.fetch_jira_bug(bug_id)
            
            # Format and display bug details
            bug_details = self.format_bug_details(bug_data)
            self.bug_details_text.insert(1.0, bug_details)
            
            # Generate AI analysis
            self.status_label.config(text="Generating AI-powered bug fix suggestions...")
            self.root.update()
            analysis = self.generate_copilot_analysis(bug_data)
            self.bug_fix_text.insert(1.0, analysis)
            
            self.status_label.config(text=f"✓ Analysis completed for {bug_id}")
            messagebox.showinfo("Success", f"Bug {bug_id} analyzed successfully!")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.status_label.config(text="Error occurred during analysis")
            self.bug_fix_text.insert(1.0, error_msg)
            messagebox.showerror("Error", error_msg)
        
        finally:
            # Re-enable button and stop progress
            self.analyze_button.config(state='normal')
            self.progress.stop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JiraAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
