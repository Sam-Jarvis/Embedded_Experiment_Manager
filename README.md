# Embedded_Experiment_Manager
Embedded system to manage and log an experiment testing external factors (mechanical vibration, exposure to sunlight, storage duration, temperature) on LBC samples.

## Installation

This project has 2 parts, the experiment manager itself and the flask file upload server. The file upload server is used to proved the experiment manager with an experiment configuration file.

### File upload server
This is a typical (and simple) Flask application. The idea is that this runs on the Raspberry Pi and triggers the experiment manager to parse the configuration file and start the experiment a new configuration file is uploaded through it. Thus, it should be deployed on the Raspberry Pi. This can be done in multiple ways but I simply followed these instructions:

https://realpython.com/kickstarting-flask-on-ubuntu-setup-and-deployment/

### Experiment manager
For this to work, the `config_watchdog` script must be running in the background. It waits for a new configuration file to appear and then triggers the whole parsing and scheduling process. As of yet, I have not made an install script that does this however, coming soon! For now, so long as the `config_watchdog` script is always running, it will work.
