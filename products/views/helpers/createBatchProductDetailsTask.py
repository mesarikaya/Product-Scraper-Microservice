import logging
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
    batchEnd = 0
    total_product_count = len(product_id_list)
    max_iteration_count = (total_product_count // batch_size) + 1
    print("Total product count:", total_product_count)
    print("Max iteration count: ", max_iteration_count)
    iteration = 0
    while iteration < max_iteration_count:
        batchStart = batchEnd
        batchEnd = batchStart + batch_size
        iteration += 1

        if batchStart > total_product_count-1:
            break

        time_delay_in_seconds = random.randint(min_time_delay, max_time_delay)
        next_run = timezone.now() + timedelta(seconds=time_delay_in_seconds)

        try:
            print('Iteration count {iteration} Creating product details for batch start:{batchStart}-end:{batchEnd}'
                  .format(iteration=iteration, batchStart=batchStart, batchEnd=batchEnd))

            create_product_detail(product_id_list[batchStart:batchEnd],
                                  view_json=view_json,
                                  serializer_json=serializer_json,
                                  schedule=time_delay_in_seconds,
                                  verbose_name=task_name + "-" + "batch start-" +
                                               str(batchStart) + "-" + "batch end-" +
                                               str(batchEnd) + str(next_run))
        except Exception as e:
            print("Error in batch product details task creation.", e)


