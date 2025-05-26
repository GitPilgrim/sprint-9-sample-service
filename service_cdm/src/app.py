
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app_config import AppConfig
from cdm_loader.cdm_message_processor_job import CDMMessageProcessor
from cdm_loader.repository.cdm_repository import CDM_Repository

app = Flask(__name__)

@app.get('/health')
def health():
    return 'healthy'

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    config = AppConfig()
    
    
    pg_connect = config.pg_warehouse_db()
    cdm_repository = CDM_Repository(pg_connect)
    cdm_proc = CDMMessageProcessor(
        config.kafka_consumer(), 
        cdm_repository,
        100, 
        app.logger
    )
    
 

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cdm_proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)
    scheduler.start()

    app.run(debug=True, host='0.0.0.0', use_reloader=False)