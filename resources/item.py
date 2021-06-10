from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

# resource là thứ mà api thao tác : Users, Items, Stores
# chứ không phải User
# model là thứ được đưa từ database lên dto
# resource là thứ dùng để thao tác dữ liệu dao
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store_id'
                        )

    # đặt @jwt ở đầu mỗi hàm nào, thì khi gọi hàm đó ta cần phải /auth trước,
    # nhập header, body gồm username, password, nhấn chạy thì sẽ trả về access token, copy nó
    # sau đó ở header của hàm được gọi key phải là Authorization,
    # và value phải là JWT + khoảng cách + access token vừa copy
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        # hàm find by name đáng lẽ trả về 1 dictionary nhưng nó đã được đổi
        # để trả về là 1 object

        # dữ liệu trả về phải là resource, resource là dữ liệu đã được thao tác có thể là 1 object hay list
        # sau đó resource sẽ được mã hóa .json() để chuyển thành dictionary,
        # dictionary đổi thành text đề api có thể đọc được

        if item:  # is not None
            return item.json()
        return {'message': 'Item not found'}, 404

    # dữ liệu gửi lên sẽ là 1 dictionary
    def post(self, name):
        # kiểm tra lỗi trước rồi mới tới bước tiếp theo
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exist.'}, 400
            # 400: bad request

        data = Item.parser.parse_args()
        # item = {'name': name, 'price': data['price']}

        # item = ItemModel(name, data['price'], data['store_id'])
        # ItemModel item = new ItemModel(name, data['price'])
        # ý là vậy

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item, 201
        # status :201 CREATE

    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):

        data = Item.parser.parse_args()
        # data = request.get_json()

        item = ItemModel.find_by_name(name)
        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            # update price

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
