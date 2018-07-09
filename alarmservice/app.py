# -*- coding: UTF-8 -*-
"""
Created on 8 Jul 2018

@author: Fredrik
hello_flask: First Python-Flask webapp
""" 
import configparser
import logging
import sectoralarm
import os


from flask import Flask, request  # From module flask import class Flask
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

class alarmservice:

    def __init__(self):
            config = configparser.ConfigParser()
            config.read('config.cfg')
            numeric_level = getattr(logging, config.get('Logging', 'level').upper(), None)
            log_location = config.get('Logging', 'log_location')
            logfile = os.path.join(log_location, 'alarmservice.log')
            logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename=logfile, level=numeric_level)
            self.alarm_email = config.get('Alarm', 'email')
            self.alarm_password = config.get('Alarm', 'password')
            self.alarm_siteId = config.get('Alarm', 'siteId')
            self.alarm_panel_code = config.get('Alarm', 'panel_code')
            self.arlo_email = config.get('Arlo', 'email')
            self.arlo_password = config.get('Arlo', 'password')
            self.alarm = sectoralarm.connect(self.alarm_email, self.alarm_password, self.alarm_siteId, self.alarm_panel_code)

    def arm_annex(self):
        '''
        Arms the Annex. If notify is set it will send an e-mail on
        state change.
        '''
        
        try:
            self.alarm.arm_annex()

        except:
            logging.error('Could not arm annex.', exc_info=True)
    
    def annex_status(self):
        try:
            status = self.alarm.status()
            return status['StatusAnnex']
        except:
            logging.error('Could not get status for annex.', exc_info=True)
        

@app.route('/annex', methods = ['POST', 'GET', 'DELETE'])
def annex():
    if request.method == 'POST':
        service.arm_annex()
        return 'success'
    elif request.method == 'GET':
        status = service.annex_status()
        return status

if __name__ == '__main__':  # Script executed directly?
    service = alarmservice()
    app.run("0.0.0.0", port=5000, debug=True)  # Launch built-in web server and run this Flask webapp
    