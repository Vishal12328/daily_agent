import smtplib
import ssl
import os
import requests
import feedparser
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DailyDevOpsAgent:
    def __init__(self):
        # Validate environment variables
        self.email_user = os.environ.get('EMAIL_USER')
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        self.recipient_email = os.environ.get('RECIPIENT_EMAIL')
        
        if not all([self.email_user, self.email_password, self.recipient_email]):
            raise ValueError("Missing required environment variables: EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL")
        
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # Updated RSS feeds with more reliable sources
        self.rss_feeds = [
            "https://devops.com/feed/",
            "https://blog.docker.com/feed/",
            "https://kubernetes.io/feed.xml",
            "https://aws.amazon.com/blogs/devops/feed/",
            "https://github.blog/feed/",
            "https://www.redhat.com/en/rss/blog"
        ]

        # Expanded technical questions pool
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
            "How do you implement circuit breaker pattern in microservices?",
            "What is the difference between RollingUpdate and Recreate deployment strategies?",
            "How do you implement horizontal pod autoscaling in Kubernetes?",
            "What are the best practices for container security?",
            "How do you handle persistent storage in Kubernetes?",
            "What is the difference between StatefulSet and Deployment?",
            "How do you implement health checks in Docker containers?",
            "What are the key metrics to monitor in a containerized environment?",
            "How do you manage secrets rotation in production?",
            "What is the difference between ingress and service mesh?",
            "How do you implement GitOps workflows?"
        ]

        # 5AM Club quotes
        self.quotes = [
            "The time you least feel like doing something is the best time to do it.",
            "Dream Big. Start small. Begin Now.",
            "World-Class begins where your comfort zone ends.",
            "All change is hard at first, messy in the middle and gorgeous at the end.",
            "Nothing works for those who don't do the work.",
            "Once you know better you can achieve bigger.",
            "Small things matter when it comes to mastery.",
            "Your excuses are nothing more than the lies your fears have sold you.",
            "Change is never a matter of ability, it's always a matter of motivation.",
            "The moment when you most feel like giving up is the moment when you need to keep pushing forward."
        ]

        # Micro habits
        self.micro_habits = [
            "Start your day with a 10-minute code review of yesterday's work",
            "Write one line of documentation for every 10 lines of code",
            "Learn one new terminal command every day",
            "Spend 5 minutes reading system logs before starting work",
            "Practice explaining complex concepts in simple terms",
            "Set up one automated test per feature you develop",
            "Review and update one monitoring alert threshold",
            "Read one page of a technical book during lunch",
            "Write a brief summary of what you learned today",
            "Practice a new keyboard shortcut in your IDE",
            "Refactor one small function to improve readability",
            "Update one piece of outdated documentation"
        ]

    def fetch_devops_news(self):
        """Fetch latest DevOps/MLOps news from RSS feeds"""
        news_items = []
        
        for feed_url in self.rss_feeds:
            try:
                logger.info(f"Fetching feed: {feed_url}")
                
                # Add timeout and user agent for better reliability
                headers = {'User-Agent': 'DailyDevOpsAgent/1.0'}
                response = requests.get(feed_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    for entry in feed.entries[:2]:  # Get top 2 from each feed
                        news_items.append({
                            'title': entry.title,
                            'link': entry.link,
                            'published': entry.get('published', 'N/A'),
                            'source': feed.feed.title if hasattr(feed.feed, 'title') else 'Unknown'
                        })
                    logger.info(f"Successfully fetched {len(feed.entries[:2])} items from {feed_url}")
                else:
                    logger.warning(f"No entries found in feed: {feed_url}")
                    
            except Exception as e:
                logger.error(f"Error fetching {feed_url}: {e}")

        logger.info(f"Total news items collected: {len(news_items)}")
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

                <h2 style="color: #27ae60; margin-top: 30px;">📰 Part 1: Latest DevOps & MLOps Advancements</h2>
        """

        if news_items:
            html_content += '<ul style="padding-left: 20px;">'
            for item in news_items:
                html_content += f"""
                        <li style="margin-bottom: 10px;">
                            <strong><a href="{item['link']}" style="color: #3498db; text-decoration: none;">{item['title']}</a></strong>
                            <br><span style="color: #7f8c8d; font-size: 0.9em;">Source: {item['source']} | {item['published']}</span>
                        </li>
                """
            html_content += '</ul>'
        else:
            html_content += '<p style="color: #e74c3c;">No news items available today. Check back tomorrow!</p>'

        html_content += f"""
                <h2 style="color: #e74c3c; margin-top: 30px;">❓ Part 2: 10 Technical Questions (Practice + Reinforcement)</h2>
                <ol style="padding-left: 20px;">
        """

        for i, question in enumerate(questions, 1):
            html_content += f"""
                    <li style="margin-bottom: 8px;">{question}</li>
            """

        html_content += f"""
                </ol>

                <h2 style="color: #9b59b6; margin-top: 30px;">💡 Part 3: Daily Quote from "The 5AM Club"</h2>
                <blockquote style="background: #f8f9fa; padding: 15px; border-left: 4px solid #9b59b6; margin: 20px 0; font-style: italic;">
                    "{quote}"
                    <br><strong>- Robin Sharma, The 5AM Club</strong>
                </blockquote>

                <h2 style="color: #f39c12; margin-top: 30px;">🎯 Part 4: Micro Habit or Engineering Insight</h2>
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border: 1px solid #ffeaa7;">
                    <strong>Today's Micro Habit:</strong><br>
                    {habit}
                </div>

                <div style="margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 5px; text-align: center;">
                    <p style="margin: 0; color: #7f8c8d;">
                        This automated report was generated by your Daily DevOps Agent<br>
                        <small>Stay curious, keep learning, and build amazing things! 🚀</small>
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
            logger.info("Creating email message...")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Daily DevOps Update - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.email_user
            msg['To'] = self.recipient_email

            # Create HTML content
            html_content = self.create_email_content()
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            logger.info("Connecting to SMTP server...")
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_user, self.email_password)
                server.send_message(msg)

            logger.info(f" Daily email sent successfully to {self.recipient_email}")
            return True

        except Exception as e:
            logger.error(f" Error sending email: {e}")
            return False

    def test_connection(self):
        """Test SMTP connection without sending email"""
        try:
            logger.info("Testing SMTP connection...")
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_user, self.email_password)
            logger.info(" SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False

def main():
    try:
        agent = DailyDevOpsAgent()
        
        # Test connection first
        if agent.test_connection():
            agent.send_email()
        else:
            logger.error("Connection test failed, not sending email")
            
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")

if __name__ == "__main__":
    main()