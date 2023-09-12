#! /bin/bash
sudo sed -i "s/backend-app-[0-9]*\.us-east-1\.elb\.amazonaws\.com/$1/g" /etc/nginx/sites-available/fabapp
sudo service nginx restart
sudo service fabapp restart