'''
Created on 31-Jul-2014

@author: nikita
'''
from flask import Flask, request, render_template
from flask.helpers import url_for
from werkzeug import redirect
import json
from flask.json import jsonify
import socket

from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__) 
app.secret_key = 'process key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/process'
from models import db, ProcessInfo, ProcessStatus
db.init_app(app)

@app.route('/store_process_info', methods=['POST'])
def store_process_info():
    
    req = json.loads(request.data)
    host = socket.gethostbyname(socket.gethostname())  
    
    for key, val in req.iteritems():
        process_info = json.loads(val)
        cpu_usage = process_info["cpu_usage"]
        memory_usage = process_info["memory_usage"]
        process_id = process_info["process_id"]
        process_Status = process_info["process_Status"]
        start_time = process_info["start_time"]
        process_name = process_info["process_name"]
        process_command = process_info["process_command"]
                       
        #print "{} -> Memory Usage {}".format(key, process_info["memory_usage"])
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proc_data = ProcessInfo(process_name, process_command, process_id, host, start_time, created_at)
        try:
            
            db.session.add(proc_data)
            #db.session.flush()
            db.session.commit() 
        
        except IntegrityError :
            db.session.rollback()
           
        proc_status = ProcessStatus(cpu_usage, memory_usage, process_Status, created_at)
        
        proc_status.process_id = proc_data.process_id
        db.session.add(proc_status)
        db.session.commit() 
        
        
    return "200 OK"
       
@app.route("/")
def index():
   
    elapsed_time = []
    json_results = []
    
    que = db.session.query(ProcessInfo.host.distinct().label("host"))
    proc_data_host = [row.host for row in que.all()]
    proc_data = ProcessInfo.query.offset(0).all()
    proc_stat = ProcessStatus.query.filter_by(process_id = ProcessInfo.process_id).all()
    
    if proc_data is None:
        return "No data"
    else:
        
        for data in proc_data:
            d1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(data.start_time, "%Y-%m-%d %H:%M:%S")
            elapsed_time.append(abs((d2 - d1))) 
       
        json_results = zip(proc_data,proc_stat,elapsed_time)
        return render_template('index.html', json_results=json_results, proc_data_host=proc_data_host, length=len(proc_data_host))
    
@app.route('/load_ajax/<pid>', methods=["GET"])
def load_ajax(pid):
        
        result = ProcessStatus.query.filter_by(process_id = pid).all()
        cpu_mem = []
        cpu_use = []
        mem_use = []
        time_str = []
        for data in result:
            created_time = data.created_at
            cpu_use.append(data.cpu_usage)
            mem_use.append(data.memory_usage)
        
        created_time = datetime.strptime(created_time, "%Y-%m-%d %H:%M:%S")
        time_str.append(created_time.year) 
        time_str.append(created_time.month) 
        time_str.append(created_time.day) 
        time_str.append(created_time.hour) 
        time_str.append(created_time.minute) 
           
        cpu_mem.append(cpu_use)
        cpu_mem.append(mem_use)
        cpu_mem.append(time_str)
        return json.dumps(cpu_mem)


app.run(debug=True)   