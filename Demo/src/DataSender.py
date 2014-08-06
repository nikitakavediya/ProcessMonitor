'''
Created on 31-Jul-2014

@author: nikita
'''
#import ProcessMonitoring
import requests  # @UnresolvedImport
import json

jlist = {} 
def send_process_information(json_list):
    
    jkeys = json_list["Processes"].keys()
    jvalues = json_list["Processes"].values()
    jlist = dict(zip(jkeys, jvalues))
    print jlist
         
    url = "http://127.0.0.1:5000/store_process_info"
   
    headers = {'Content-Type': 'application/json'}
      
    r =requests.post(url, data=json.dumps(jlist), headers=headers)
    print r
    #print r.content
    
    
    