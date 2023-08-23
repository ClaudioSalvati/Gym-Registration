#!/usr/bin/env python3

import requests
from scrapy import Selector
import re
import logging
import smtplib
from email.message import EmailMessage

# Variables for Elements Registration. A free account is required and the credentials will be insert below as "email" and "password"
BASE_URL = "https://slots.elements.com"
LOG_FILENAME = '<PATH TO THE FILE>\script_logs.log'
email = <EMAIL-ADDRESS> # URL encoded, i.e. "@" gets "%40"
password = <YOUR-PASSWORD> # Also URL encoded
studio_id = <ID> # The studio ID, a value between 60 and 66, from view-source:https://slots.elements.com/sheet.php


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_html(session, endpoint):
    """Fetch the HTML from the provided endpoint using the given session."""
    try:
        response = session.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching HTML: {e}")
        return None


def extract_course_sheet_id(href_string):
    """Extract the course_sheet_id using regex."""
    # Looking for a pattern 'course_sheet_id=(number)'
    match = re.search(r'course_sheet_id=(\d+)', href_string)
    return match.group(1) if match else None


def main():
    # Initialize session
    with requests.Session() as s:

        # Fetch login page
        html = fetch_html(s, f"?action=login&send=1&email={email}&password={password}")
        if not html:
            return
        
        # Extract studio information
        html = fetch_html(s, f"/sheet.php?studio_id={studio_id}")
        if not html:
            return
        selector = Selector(text=html)
        href_values = selector.xpath('//div[@class="ct-td align-right"]/span/a[@class="button"]/@href').getall()
        if not href_values:
            return
        course_sheet_id = extract_course_sheet_id(href_values[0])
        if not course_sheet_id:
            return

        # Fetch register page and extract information
        html = fetch_html(s, f"/sheet.php?action=register&course_sheet_id={course_sheet_id}&studio_id={studio_id}")
        if not html:
            return
        register_sel = Selector(text=html)
        message = register_sel.xpath('//div[@class="message"]').extract()
        if message:
            logging.info(message[0])
        else:
            logging.warning("Message not found!")
        
        success_messages = register_sel.xpath("//div[@class='ct-tr']/div[@class='ct-td'][4]/span[1]").extract()
        if success_messages:
            logging.info(success_messages[0])
        else:
            logging.warning("Success message not found!")


def send_email_with_logs():
    """Send email with log contents using Gmail."""
    # Email configuration
    GMAIL_USER = <GMAIL-ADDRESS>
    GMAIL_PASS = <GMAIL-APP-PASSWORD> # Please use the App Password instead of your Google Account Password: https://support.google.com/accounts/answer/185833?hl=en 
    TO_EMAIL = <RECIPIENT> # Can be the same email address as GMAIL_USER. 
    SUBJECT = 'Studioanmeldung Logs'

    # Read log file
    with open(LOG_FILENAME, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # Set up the email
    msg = EmailMessage()
    msg.set_content(log_content)
    msg['Subject'] = SUBJECT
    msg['From'] = GMAIL_USER
    msg['To'] = TO_EMAIL

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")


if __name__ == "__main__":
    main()
    send_email_with_logs()
