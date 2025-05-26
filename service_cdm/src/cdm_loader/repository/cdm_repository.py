# cdm_repository.py
from datetime import datetime
from decimal import Decimal
from lib.pg import PgConnect

class CDM_Repository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def cdm_user_category_counters_insert(self,
                                        user_id: str,
                                        category_id: str,
                                        category_name: str,
                                        order_cnt: int) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO cdm.user_category_counters (
                        user_id,
                        category_id,
                        category_name,
                        order_cnt
                    ) VALUES (
                        %(user_id)s::uuid,
                        %(category_id)s::uuid,
                        %(category_name)s,
                        %(order_cnt)s
                    )
                    ON CONFLICT (user_id, category_id) DO UPDATE SET
                        order_cnt = cdm.user_category_counters.order_cnt + EXCLUDED.order_cnt,
                        category_name = EXCLUDED.category_name
                    """,
                    {
                        'user_id': user_id,
                        'category_id': category_id,
                        'category_name': category_name,
                        'order_cnt': order_cnt
                    }
                )

    def cdm_user_product_counters_insert(self,
                                       user_id: str,
                                       product_id: str,
                                       product_name: str,
                                       order_cnt: int) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO cdm.user_product_counters (
                        user_id,
                        product_id,
                        product_name,
                        order_cnt
                    ) VALUES (
                        %(user_id)s::uuid,
                        %(product_id)s::uuid,
                        %(product_name)s,
                        %(order_cnt)s
                    )
                    ON CONFLICT (user_id, product_id) DO UPDATE SET
                        order_cnt = cdm.user_product_counters.order_cnt + EXCLUDED.order_cnt,
                        product_name = EXCLUDED.product_name
                    """,
                    {
                        'user_id': user_id,
                        'product_id': product_id,
                        'product_name': product_name,
                        'order_cnt': order_cnt
                    }
                )