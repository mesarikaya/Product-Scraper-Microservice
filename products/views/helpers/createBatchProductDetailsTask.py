import random

from datetime import timedelta
from django.utils import timezone
from .createProductDetail import create_product_detail


def create_batch_product_details_task(product_class,
                                      column_name,
                                      view_json,
                                      serializer_json,
                                      task_name, batch_size=10,
                                      min_time_delay=1, max_time_delay=5):

    product_id_list = list(set(list(product_class.objects.values_list(column_name, flat=True))))
    batchStart = 0
    batchEnd = 0
    total_product_count = len(product_id_list)
    while batchStart < total_product_count:
        batchStart = batchEnd
        batchEnd = batchStart + batch_size
        if batchEnd > total_product_count:
            batchEnd = total_product_count

        if batchStart == total_product_count:
            break

        time_delay_in_seconds = random.randint(min_time_delay, max_time_delay)
        next_run = timezone.now() + timedelta(seconds=time_delay_in_seconds)
        try:
            create_product_detail(product_id_list,
                                  batchStart,
                                  batchEnd,
                                  view_json=view_json,
                                  serializer_json=serializer_json,
                                  schedule=time_delay_in_seconds,
                                  verbose_name=task_name + "-" + str(next_run))
        except Exception as e:
            raise Exception(e)