'''
Created on 04-Aug-2014

@author: nikita
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
db = SQLAlchemy()

class ProcessInfo(db.Model):
    __tablename__ = 'process_info'
    
    proc_id = db.Column(db.Integer, primary_key = True)
    process_name = db.Column(db.String(100))
    process_command = db.Column(db.String(100))
    process_id = db.Column(db.String(50))
    host = db.Column(db.String(50))
    start_time = db.Column(db.String(50))
    created_at = db.Column(db.String(50))
    process_status = db.relationship('ProcessStatus' , backref='stat', lazy='dynamic')
    __table_args__ = (UniqueConstraint('process_id', 'host', name='host_id'),{})
    
    def __init__(self, process_name, process_command, process_id, host, start_time, created_at):
        
        self.process_name = process_name
        self.process_command = process_command
        self.process_id = process_id
        self.host = host
        self.start_time = start_time
        self.created_at = created_at

class ProcessStatus(db.Model):
    __tablename__ = 'process_status'
    proc_sid = db.Column(db.Integer, primary_key = True)
    process_id = db.Column(db.Integer, ForeignKey('process_info.process_id'))
    cpu_usage = db.Column(db.Float)
    memory_usage = db.Column(db.Float)
    process_Status = db.Column(db.String(50))
    created_at = db.Column(db.String(50))
    
    def __init__(self, cpu_usage, memory_usage, process_Status, created_at):
        
        
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.process_Status = process_Status
        self.created_at = created_at