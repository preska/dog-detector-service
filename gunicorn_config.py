# Databricks notebook source

import os

workers = 6 # int(os.environ.get('GUNICORN_PROCESSES', '3'))
threads = 1 # int(os.environ.get('GUNICORN_THREADS', '1'))
timeout = 120 # int(os.environ.get('GUNICORN_TIMEOUT', '120'))
bind = '0.0.0.0:8080' #os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')

forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
