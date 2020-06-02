import logging
import jsonpickle

from background_task import background


@background(schedule=5)
def create_product_detail(ids, start, end, view_json, serializer_json):
    product_id_list = ids[start:end]
    data = list()
    view_class = jsonpickle.loads(view_json)
    serializer_class = jsonpickle.loads(serializer_json)
    for product_id in view_class.get_product_id(product_id_list):
        result = view_class.get_json_data(product_id)
        if result:
            data.append(result)

        serializer = serializer_class(data=data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                logging.debug("Error in serialize.save() for batch product id load.")
        else:
            logging.debug("Serializer is invalid with errors:", serializer.errors)
