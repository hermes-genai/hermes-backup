#!/usr/bin/env python3
"""
Hermes Token Usage Reporter
Generates a token usage report for Slack notification
"""

import subprocess
import re
import os
import sys

def get_hermes_insights(days=1):
    """Run hermes insights command and return output"""
    try:
        result = subprocess.run(
            ['hermes', 'insights', '--days', str(days)],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None, f"Error running hermes insights: {result.stderr}"
        return result.stdout, None
    except subprocess.TimeoutExpired:
        return None, "Command timed out"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def parse_insights(output):
    """Parse hermes insights output and extract key metrics"""
    if not output:
        return None
    
    # Initialize metrics
    metrics = {
        'total_tokens': 'Unknown',
        'input_tokens': 'Unknown',
        'output_tokens': 'Unknown',
        'sessions': 'Unknown',
        'messages': 'Unknown',
        'top_model': 'Unknown',
        'top_platform': 'Unknown',
        'top_tool': 'Unknown'
    }
    
    # Parse using regex
    total_match = re.search(r'Total tokens:\s*([\d,]+)', output)
    if total_match:
        metrics['total_tokens'] = total_match.group(1)
    
    input_match = re.search(r'Input tokens:\s*([\d,]+)', output)
    if input_match:
        metrics['input_tokens'] = input_match.group(1)
    
    output_match = re.search(r'Output tokens:\s*([\d,]+)', output)
    if output_match:
        metrics['output_tokens'] = output_match.group(1)
    
    sessions_match = re.search(r'Sessions:\s*(\d+)', output)
    if sessions_match:
        metrics['sessions'] = sessions_match.group(1)
    
    messages_match = re.search(r'Messages:\s*(\d+)', output)
    if messages_match:
        metrics['messages'] = messages_match.group(1)
    
    # Extract top model
    in_models = False
    for line in output.split('\n'):
        if '🤖 Models Used' in line:
            in_models = True
            continue
        elif in_models and line.strip() == '':
            break
        elif in_models and 'nemotron' in line:
            # Take the first model line
            model_parts = line.strip().split()
            if model_parts:
                metrics['top_model'] = model_parts[0]
            break
    
    # Extract top platform (look for slack in platforms section)
    in_platforms = False
    for line in output.split('\n'):
        if '📱 Platforms' in line:
            in_platforms = True
            continue
        elif in_platforms and line.strip() == '':
            break
        elif in_platforms and 'slack' in line:
            metrics['top_platform'] = 'slack'
            break
    
    # Extract top tool
    in_tools = False
    for line in output.split('\n'):
        if '🔧 Top Tools' in line:
            in_tools = True
            continue
        elif in_tools and line.strip() == '':
            break
        elif in_tools and 'terminal' in line:
            metrics['top_tool'] = 'terminal'
            break
    
    return metrics

def format_slack_message(metrics):
    """Format metrics into a Slack-friendly message"""
    if not metrics:
        return "❌ Unable to generate token usage report"
    
    message = f"""📊 *Hermes Token Usage Report* (Last 24h)
──────────────────────────────────
🔢 *Total Tokens:* {metrics['total_tokens']}
📥 *Input:* {metrics['input_tokens']}
📤 *Output:* {metrics['output_tokens']}
👥 *Sessions:* {metrics['sessions']}
💬 *Messages:* {metrics['messages']}

*Top Model:* {metrics['top_model']}
*Top Platform:* {metrics['top_platform']}
*Top Tool:* {metrics['top_tool']}

_Full details available via:_ \`hermes insights --days 1\`"""
    
    return message

def main():
    """Main function to generate and display/send token usage report"""
    # Get insights data
    output, error = get_hermes_insights(days=1)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    # Parse the insights
    metrics = parse_insights(output)
    
    if not metrics:
        print("Error: Could not parse insights data")
        sys.exit(1)
    
    # Format for Slack
    slack_message = format_slack_message(metrics)
    
    # Print to stdout (this is what will be captured by the cron job)
    print(slack_message)
    
    # Optionally save to file
    try:
        with open('/tmp/hermes_token_report.txt', 'w') as f:
            f.write(slack_message)
    except Exception:
        pass  # Non-critical if we can't save
    
    return 0

if __name__ == '__main__':
    sys.exit(main())