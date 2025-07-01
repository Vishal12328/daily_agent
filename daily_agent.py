import smtplib
import ssl
import os
import requests
import feedparser
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DailyDevOpsAgent:
    def __init__(self):
        self.email_user = os.environ.get('EMAIL_USER')
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        self.recipient_email = os.environ.get('RECIPIENT_EMAIL')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # RSS feeds for DevOps/MLOps content
        self.rss_feeds = [
            "https://devops.com/feed/",
            "https://blog.docker.com/feed/",
            "https://kubernetes.io/feed.xml",
            "https://aws.amazon.com/blogs/devops/feed/"
        ]

        # Technical questions pool
        self.questions_pool = [
            "What is the difference between Docker ADD and COPY commands?",
            "How do you troubleshoot a CrashLoopBackOff pod in Kubernetes?",
            "What are the benefits of using multi-stage Docker builds?",
            "How does Kubernetes service discovery work?",
            "What is the purpose of init containers in Kubernetes?",
            "How do you implement blue-green deployment?",
            "What is the difference between ConfigMap and Secret in Kubernetes?",
            "How do you optimize Docker image size?",
            "What are Kubernetes admission controllers?",
            "How do you implement circuit breaker pattern in microservices?"
        ]

        # 5AM Club quotes
        self.quotes = [
            "The time you least feel like doing something is the best time to do it.",
            "Dream Big. Start small. Begin Now.",
            "World-Class begins where your comfort zone ends.",
            "All change is hard at first, messy in the middle and gorgeous at the end.",
            "Nothing works for those who don't do the work.",
            "Once you know better you can achieve bigger.",
            "Small things matter when it comes to mastery."
        ]

        # Micro habits
        self.micro_habits = [
            "Start your day with a 10-minute code review of yesterday's work",
            "Write one line of documentation for every 10 lines of code",
            "Learn one new terminal command every day",
            "Spend 5 minutes reading system logs before starting work",
            "Practice explaining complex concepts in simple terms",
            "Set up one automated test per feature you develop"
        ]

    def fetch_devops_news(self):
        """Fetch latest DevOps/MLOps news from RSS feeds"""
        news_items = []

        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:2]:  # Get top 2 from each feed
                    news_items.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', 'N/A'),
                        'source': feed.feed.title if hasattr(feed.feed, 'title') else 'Unknown'
                    })
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")

        return news_items[:5]  # Return top 5 items

    def generate_technical_questions(self):
        """Generate 10 random technical questions"""
        return random.sample(self.questions_pool, min(10, len(self.questions_pool)))

    def get_daily_quote(self):
        """Get a random quote from 5AM Club"""
        return random.choice(self.quotes)

    def get_micro_habit(self):
        """Get a random micro habit"""
        return random.choice(self.micro_habits)

    def create_email_content(self):
        """Create the complete email content"""
        news_items = self.fetch_devops_news()
        questions = self.generate_technical_questions()
        quote = self.get_daily_quote()
        habit = self.get_micro_habit()

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2c3e50; border-bottom: 2px solid #3498db;">Daily DevOps & MLOps Update</h1>
                <p style="color: #7f8c8d; font-style: italic;">Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M UTC')}</p>

                <h2 style="color: #27ae60; margin-top: 30px;">ðŸ“° Part 1: Latest DevOps & MLOps Advancements</h2>
                <ul style="padding-left: 20px;">
        """

        for item in news_items:
            html_content += f"""
                    <li style="margin-bottom: 10px;">
                        <strong><a href="{item['link']}" style="color: #3498db; text-decoration: none;">{item['title']}</a></strong>
                        <br><span style="color: #7f8c8d; font-size: 0.9em;">Source: {item['source']} | {item['published']}</span>
                    </li>
            """

        html_content += f"""
                </ul>

                <h2 style="color: #e74c3c; margin-top: 30px;">â“ Part 2: 10 Technical Questions (Practice + Reinforcement)</h2>
                <ol style="padding-left: 20px;">
        """

        for i, question in enumerate(questions, 1):
            html_content += f"""
                    <li style="margin-bottom: 8px;">{question}</li>
            """

        html_content += f"""
                </ol>

                <h2 style="color: #9b59b6; margin-top: 30px;">ðŸ’¡ Part 3: Daily Quote from "The 5AM Club"</h2>
                <blockquote style="background: #f8f9fa; padding: 15px; border-left: 4px solid #9b59b6; margin: 20px 0; font-style: italic;">
                    "{quote}"
                    <br><strong>- Robin Sharma, The 5AM Club</strong>
                </blockquote>

                <h2 style="color: #f39c12; margin-top: 30px;">ðŸŽ¯ Part 4: Micro Habit or Engineering Insight</h2>
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border: 1px solid #ffeaa7;">
                    <strong>Today's Micro Habit:</strong><br>
                    {habit}
                </div>

                <div style="margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 5px; text-align: center;">
                    <p style="margin: 0; color: #7f8c8d;">
                        This automated report was generated by your Daily DevOps Agent<br>
                        <small>Stay curious, keep learning, and build amazing things! ðŸš€</small>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return html_content

    def send_email(self):
        """Send the daily email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Daily DevOps Update - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.email_user
            msg['To'] = self.recipient_email

            # Create HTML content
            html_content = self.create_email_content()
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_user, self.email_password)
                server.send_message(msg)

            print(f"âœ… Daily email sent successfully to {self.recipient_email}")

        except Exception as e:
            print(f"âŒ Error sending email: {e}")

def main():
    agent = DailyDevOpsAgent()
    agent.send_email()

if __name__ == "__main__":
    main()
