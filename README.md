Daily DevOps Email Agent 

This is a Email Bot that will collect news information from different RSS feed daily with particular keywords and pool them into neat and proper formatted text along with 10 questions from the devops world which will solidify the fundamentals and then end with a quotation from book of my choice.

# Setup Instructions
## Prerequisites
1. GitHub account
2. Gmail account with 2FA enabled
3. Basic understanding of Python and GitHub Actions

## Step-by-Step Setup

### 1. Create GitHub Repository
- Create a new repository on GitHub
- Clone it to your local machine

### 2. Create Project Files
Create the following files in your repository:

**daily_agent.py** - Main Python script (see main_script above)
**requirements.txt** - Python dependencies
**.github/workflows/daily-email.yml** - GitHub Actions workflow

### 3. Set up Gmail App Password
1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security > 2-Step Verification > App passwords
4. Generate a new app password for "Mail"
5. Copy the 16-character password (remove spaces)

### 4. Configure GitHub Secrets
Go to your repository Settings > Secrets and variables > Actions
Add these secrets:
- `EMAIL_USER`: Your Gmail address
- `EMAIL_PASSWORD`: The 16-character app password from Gmail
- `RECIPIENT_EMAIL`: Email address to receive daily updates

### 5. Test the Setup
1. Commit and push all files to GitHub
2. Go to Actions tab in your repository
3. Run the workflow manually to test
4. Check if email is received

### 6. Customize (Optional)
- Modify RSS feeds in the script
- Add more technical questions
- Adjust the cron schedule
- Customize email template

## Troubleshooting
- If emails weren't recieved, check GitHub Actions logs
- Ensure Gmail app password is correct
- Verify all secrets are set properly(IMPORTANT)
- Check spam folder for emails

## Cost: Completely Free!
- GitHub Actions: 2000 free minutes/month
- Gmail SMTP: Free

## Email That is recieved:
![Image](result.png)
