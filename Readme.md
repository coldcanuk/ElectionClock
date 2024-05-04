# Election Clock Website

## Overview
The Election Clock website is a Flask-based web application that counts down to the next Canadian federal election. This project includes a dynamic visual display of a countdown timer and features integration with Twitter for social sharing capabilities.

## Features
- Countdown to the Canadian federal election.
- Dynamic visual updates every second.
- Social sharing button to share the countdown on Twitter.

## Technologies Used
- Flask
- Python
- HTML/CSS
- JavaScript

## Setup
1. Clone the repository:
   git clone https://github.com/yourusername/election-clock.git
2. Install dependencies:
   pip install -r requirements.txt
3. Test the application locally:
   flask run
4. Set Up Your Linode Server
   Deploy an Ubuntu Server:
   Log into Linode and create a new Linode.
   Choose an Ubuntu image and select a plan that fits your needs.
   Follow the setup process to launch your server.
5. Domain Configuration:
   After setting up your Linode, configure your domain mydomain.com to point to the IP address of your Linode server.
   Log into your domain registrar's control panel.
   Locate the DNS management section.
   Replace the existing A record with the public IP address of your Linode.
   If necessary, add CNAME records for subdomains.
   Update or confirm the correct NS records if managing DNS via Linode.
6. Connect to your Ubuntu server. With Linode you can use their LISH remote console shell.
7. Copy/Paste LinodeSetup.sh locally and run it. vi should already be included.
8. Next, you will need to create a local user. This is a security step as we do not want to be deploying with the user root.
### Create the user "deployuser"
1. Login to the server as root
2. Run the command to add a new user:
```bash
adduser deployuser
```
   Follow the prompts to set the password and fill out any additional information as desired.
### Grant Sudo Privileges
1. Add the new user to the 'sudo' group to allow administrative privileges:
```bash
usermod -aG sudo deployuser
```
### Set Up SSH Access
1. Switch to the new user:
```bash
su - deployuser
```
2. Create a directory for SSH keys:
```bash
mkdir ~/.ssh
chmod 700 ~/.ssh
```
3. Create or edit the authorized_keys file
```bash
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```
4. Add your public SSH key to this file. You can do this by editing authorized_keys with a text editor and pasting your SSH public key.
### Test SSH Access
1. Logout from your current session and try loggin in with the new user:
```bash
ssh deployuser@your_server_ip
```
Make sure you can log in without issues using the SSH key.
By following these steps, you create a secure user environment that minimizes the risk of root access exploits and ensures that administrative tasks can be handled safely. Make sure to use this user for your deployment processes.

## Contributing
Feel free to fork this repository and submit pull requests to contribute to its development.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
