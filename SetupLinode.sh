#!/bin/bash

# Update and install necessary packages
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install nginx gunicorn python3-pip python3-dev git -y

# Setup firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Configure Nginx to proxy requests to Gunicorn
echo "server {
    listen 80;
    server_name voteh.ca;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}" | sudo tee /etc/nginx/sites-available/electionclock

sudo ln -s /etc/nginx/sites-available/electionclock /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Setup Gunicorn to serve the Flask app
gunicorn --workers 3 --bind unix:electionclock.sock -m 007 wsgi:app

# Generate and add SSH keys for GitHub Actions
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

echo "Add the following public key to GitHub and Linode for SSH access:"
cat ~/.ssh/id_rsa.pub

# Add user for deployment and configure sudoers for passwordless commands
sudo adduser deployuser --gecos "First Last,RoomNumber,WorkPhone,HomePhone" --disabled-password
echo "deployuser:password" | sudo chpasswd
echo "deployuser ALL=(ALL) NOPASSWD: /bin/systemctl restart gunicorn, /usr/bin/git pull" | sudo EDITOR='tee -a' visudo

# Create directory for web applications and set permissions
sudo mkdir -p /home/deployuser/web
sudo chown deployuser:deployuser /home/deployuser/web

# Clone the repository into the specified directory
sudo -u deployuser -H sh -c 'cd /home/deployuser/web; git clone https://github.com/YOURUSERNAMEHERE/election-clock.git electionclock'
echo "Setup is complete. Replace 'password' with a secure password!"