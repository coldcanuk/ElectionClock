
# ElectionClock Website

## Overview
The ElectionClock website is a dynamic Flask-based web application that provides a real-time countdown to the next Canadian federal election. This visually engaging app tracks time down to the second and includes functionality for users to share the countdown via Twitter directly from the interface.

## Features
- **Countdown to the Canadian Federal Election:** Displays a real-time countdown to the next election.
- **Dynamic Visual Updates:** The countdown clock refreshes every second.
- **Social Sharing:** Allows users to share the countdown on Twitter.

## Technologies Used
- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, JavaScript

## Setup
### Prerequisites
- **Python 3.8+**: Make sure Python is installed.
- **Git**: For cloning the repository.
- **Pip**: For managing dependencies.

### Local Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/coldcanuk/ElectionClock.git
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r ElectionClock/requirements.txt
   ```
3. **Run the Application Locally:**
   ```bash
   flask run
   ```
   - This command starts a local server. Open your browser and go to `http://localhost:5000` to view the app.

### Linode Server Deployment
1. **Set Up Your Linode Server:**
   - **Deploy an Ubuntu Server:**
     - Log into Linode and create a new Linode.
     - Choose an Ubuntu image and select a plan that fits your needs.
     - Follow the setup process to launch your server.

2. **Configure Your Domain (voteh.ca):**
   - Configure the domain to point to the IP address of your Linode server.
   - Log into your domain registrar's control panel.
   - Locate the DNS management section.
   - Replace the existing A record with the public IP address of your Linode.
   - Add CNAME records for subdomains if needed.
   - Update or confirm the correct NS records if managing DNS via Linode.

3. **Connect to Your Ubuntu Server:**
   - Use the Linode LISH remote console shell or SSH.

4. **Run the `SetupLinode.sh` Script:**
   - Download and run the script to set up your Linode server.
   ```bash
   curl -o SetupLinode.sh https://raw.githubusercontent.com/coldcanuk/ElectionClock/main/SetupLinode.sh
   chmod +x SetupLinode.sh
   ./SetupLinode.sh
   ```

### Create the User `deployuser`
1. **Add a New User:**
   - Log in to the server as root.
   - Add a new user named `deployuser`.
   ```bash
   adduser deployuser
   ```
   Follow the prompts to set the password and fill out any additional information as needed.

2. **Grant `deployuser` Sudo Privileges:**
   ```bash
   usermod -aG sudo deployuser
   ```

### Set Up SSH Access
1. **Switch to the New User:**
   ```bash
   su - deployuser
   ```
2. **Create a Directory for SSH Keys:**
   ```bash
   mkdir ~/.ssh
   chmod 700 ~/.ssh
   ```
3. **Create or Edit the `authorized_keys` File:**
   ```bash
   touch ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```
4. **Add Your Public SSH Key:**
   - Edit `authorized_keys` with a text editor and paste your public SSH key.

### Test SSH Access
1. **Log in Using the New User:**
   ```bash
   ssh deployuser@your_server_ip
   ```
Make sure you can log in without issues using the SSH key.

### Scheduled Maintenance and Data Updates
The `maestro.py` script ensures all law data is up to date. It runs once a week, managed by the crontab scheduler.

1. **Run the Crontab Setup Script:**
   ```bash
   ./update_law_crontab.sh
   ```

## Contributing
Feel free to fork this repository and submit pull requests to contribute to its development.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

