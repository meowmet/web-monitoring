Secure Check - Educational Email Security Demonstration Project

⚠️ IMPORTANT: This project is strictly for educational purposes only. It is designed to demonstrate concepts related to email security and web application development. Any misuse, unauthorized use, or distribution of this project for malicious purposes is strictly prohibited and illegal. The developers are not responsible for any misuse of this code.
Overview
Secure Check is an educational project that simulates an email security checking platform. The project includes a web interface for users to check the "security" of their email addresses, a backend server to handle requests, and a dashboard for viewing simulated data. The goal is to demonstrate common web development techniques, email handling, and potential security vulnerabilities in a controlled, educational environment.
This project includes HTML pages for user interaction, a Node.js backend with Express for handling API requests, and Nodemailer for sending emails. It is intended to help developers and students understand the basics of web development, server-side programming, and email integration.
Note: The project includes a simulated "security report" link in the email functionality. This is for demonstration purposes only and does not point to a real executable file. Any real-world implementation must adhere to ethical and legal standards.
Project Structure
The project consists of the following files:

Frontend (HTML Pages):

indexx.html: Main landing page for the Secure Check platform, including email checking and informational sections.
signup.html: Simulated sign-up page for creating user accounts.
login.html: Simulated login page for user authentication.
data.html: Dashboard displaying simulated victim data (for educational demonstration).
victim.html: Page listing simulated victim data.
history-logs.html: Page displaying simulated user activity logs.
index.html: Dashboard for monitoring browser activity (simulated data).


Backend:

server.js: Node.js server using Express to handle API requests and Nodemailer for sending emails.



Features

Email Security Check (indexx.html):

Users can input an email address to "check" its security.
The backend sends a simulated security report via email using Nodemailer.
The report includes a link to a placeholder "security report" (for demonstration only).


User Authentication Pages (signup.html, login.html):

Simulated sign-up and login pages to demonstrate user authentication flows.
Includes links for password recovery and account creation.


Dashboard (data.html, victim.html, index.html, history-logs.html):

Simulated dashboards for displaying "victim" data, browser activity, and user logs.
Demonstrates how data can be presented in a web application.


Backend Server (server.js):

Handles POST requests to /send-email to send emails with a simulated security report.
Uses CORS to allow requests from specified origins.
Configured with Nodemailer to send emails via a Gmail account (for demonstration purposes).



Prerequisites
To run this project locally, you need the following:

Node.js: Version 14 or higher.
NPM: Node Package Manager for installing dependencies.
Gmail Account: For sending emails via Nodemailer (requires an App Password for Gmail).
Web Browser: For viewing the HTML pages.
Code Editor: (e.g., VS Code) for editing the project files.

Setup Instructions

Clone the Repository:
git clone <repository-url>
cd secure-check


Install Dependencies:Navigate to the project directory and install the required Node.js packages:
npm install express cors nodemailer


Configure Nodemailer:

Update the server.js file with your Gmail credentials or use an App Password for security.
Replace the user and pass fields in the transporter configuration:const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-app-password' // Generate an App Password from Gmail settings
  }
});




Place HTML Files:

Create a public directory in the project root.
Place all HTML files (index.html, signup.html, login.html, data.html, victim.html, history-logs.html, index.html(for admin)) in the public directory.


Run the Server:Start the Node.js server:
node server.js

The server will run on http://localhost:3000.

Access the Application:

Open a web browser and navigate to http://localhost:3000/indexx.html to view the main page.
Other pages can be accessed similarly (e.g., http://localhost:3000/signup.html).



Usage

Email Security Check:

Navigate to http://localhost:3000/indexx.html.
Enter an email address in the input field and click "Check."
The backend will send a simulated security report to the provided email address.


Dashboard and Logs:

Access data.html, victim.html, index.html, or history-logs.html to view simulated data.
These pages demonstrate how data can be displayed in a dashboard format.


Sign Up and Login:

Visit signup.html or login.html to explore the simulated authentication flow.
Note: These pages are for demonstration only and do not have actual backend functionality.



Security Notes

Educational Purpose Only: This project is designed to demonstrate web development and email handling concepts. It must not be used to collect real user data, send malicious emails, or distribute harmful files.
Nodemailer Configuration: Use an App Password for Gmail to avoid exposing your primary password. Never share sensitive credentials in a production environment.
Simulated Data: The dashboards and logs contain placeholder data for educational purposes. They should not be used to store or display real user information.-Clear disclaimer: This project must not be used for phishing, scamming, or any illegal activities. The included email link to a "security report" is a placeholder and must not be replaced with malicious content.

Limitations

Frontend Only Pages: The HTML pages (signup.html, login.html, etc.) are static and do not have backend functionality for user authentication or data storage.
Simulated Data: The dashboard and logs display static or placeholder data, as this is an educational project.
Email Sending: The email functionality requires a valid Gmail account and App Password. Rate limits and Gmail policies may affect email delivery.
CORS Restrictions: The backend is configured to allow requests from specific origins (http://localhost:5000, https://yourfirebasedomain.web.app). Update the CORS settings if deploying to a different domain.



⚠️Disclaimer⚠️
This project is for educational purposes only. It demonstrates how a web application with email functionality might be built. Any attempt to use this code for malicious purposes, such as phishing, data theft, or distributing malware, is illegal and unethical. The developers are not responsible for any misuse of this code. Always adhere to legal and ethical guidelines when developing or deploying web applications.
License
This project is licensed under the MIT License for educational use. See the LICENSE file for details.
Contact
For questions or feedback about this educational project, please contact the project maintainers at [your-educational-contact-email].
⚠️ Reminder: Use this project responsibly and ethically. It is intended for learning purposes only.
