#!/usr/bin/env python
#
# Citizen Desk
#
'''
Params:

* config data specifications where to POST the SMS
* phone number
* message text

'''

import os, sys, time
import urllib, urllib2

def send_message(method, url, params):
    if 'GET' == method:
        try:
            suffix_parts = []
            for param_name in params:
                one_suffix_part = urllib.quote_plus(param_name.encode('utf8'))
                one_suffix_part += '='
                one_suffix_part += urllib.quote_plus(params[param_name].encode('utf8'))
                suffix_parts.append(one_suffix_part)

            url += '?' if not '?' in url else '&'
            url += '&'.join(suffix_parts)

            resp = urllib2.urlopen(url)
            resp.read()
        except:
            #logging.warning('can not (GET) send SMS: ' + str(url))
            return False
        return True

    else:
        try:
            for param_key in params:
                params[param_key] = params[param_key].encode('utf8')

            post_data = urllib.urlencode(params)
            req = urllib2.Request(url, post_data)
            response = urllib2.urlopen(req)
            response.read()
        except:
            #logging.warning('can not (POST) send SMS: ' + str(url) + '\t' + str(params))
            return False
        return True

def send_sms(config, phone_number, message_text):

    if not 'method' in config:
        #logging.error('SMS sending: "method" is not provied in config ' + str(conf_path))
        return False

    url_param = 'url'
    if not url_param in config:
        #logging.error('SMS sending: "' + url_param + '" is not provied in config ' + str(conf_path))
        return False

    send_method = config['method']
    send_url = config[url_param]

    phone_number_param_use = None
    if 'phone_param' in config:
        phone_number_param_use = config['phone_param']
    if not phone_number_param_use:
        return False

    message_text_param_use = None
    if 'text_param' in config:
        message_text_param_use = config['text_param']
    if not message_text_param_use:
        return False

    send_params = {}
    send_params[phone_number_param_use] = phone_number
    send_params[message_text_param_use] = message_text

    rv = send_message(send_method, send_url, send_params)

    return rv

