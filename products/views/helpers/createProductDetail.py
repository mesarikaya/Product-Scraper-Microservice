import logging
import jsonpickle
from background_task import background


@background(schedule=5)
def create_product_detail(ids, view_json, serializer_json):

    product_id_list = ids
    view_class = jsonpickle.loads(view_json)
    serializer_class = jsonpickle.loads(serializer_json)

    for product_id in view_class.get_product_id(product_id_list):
        print('Creating product detail for product id: {product_id}'.format(product_id=product_id))
        result = view_class.get_json_data(product_id)
        data = list()
        if result:
            data.append(result)
            serializer = serializer_class(data=data, many=True)
            if serializer.is_valid():
                try:
                    print('product_id: {product_id}'.format(product_id=product_id))
                    serializer.save()
                except Exception as e:
                    print("Error in serialize.save() for batch product id:", product_id, "with cause: ", e.__cause__)
            else:
                print("Serializer is invalid with errors:", serializer.errors)
        else:
            print("No data is available to serialize for result:", result)
