# cdm_message_processor_job.py
import json
from logging import Logger
from datetime import datetime
from lib.kafka_connect import KafkaConsumer
from cdm_loader.repository.cdm_repository import CDM_Repository

class CDMMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 cdm_repository: CDM_Repository,
                 batch_size: int,
                 logger: Logger) -> None:
        self._consumer = consumer
        self._cdm_repository = cdm_repository
        self._logger = logger
        self._batch_size = batch_size

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        for _ in range(self._batch_size):
            msg = self._consumer.consume()
            if not msg:
                self._logger.info(f"{datetime.utcnow()}: No messages received")
                break

            try:
                if isinstance(msg, bytes):
                    msg = json.loads(msg.decode('utf-8'))
                elif isinstance(msg, str):
                    msg = json.loads(msg)

                self._logger.info(f"{datetime.utcnow()}: Message received")
                self._logger.debug(f"Message content: {msg}")

                # Process categories
                for category in msg['categories']:
                    self._cdm_repository.cdm_user_category_counters_insert(
                        user_id=msg['user_id'],
                        category_id=category['id'],
                        category_name=category['name'],
                        order_cnt=category['count']
                    )

                # Process products
                for product in msg['products']:
                    self._cdm_repository.cdm_user_product_counters_insert(
                        user_id=msg['user_id'],
                        product_id=product['id'],
                        product_name=product['name'],
                        order_cnt=product['count']
                    )

                self._logger.info(f"{datetime.utcnow()}: Data successfully loaded to CDM")

            except Exception as e:
                self._logger.error(f"{datetime.utcnow()}: Error processing message. Reason: {e}")
                continue

        self._logger.info(f"{datetime.utcnow()}: FINISH")