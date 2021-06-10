from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

from db import db
from resources.store import Store, StoreList

# RESTful API không sử dụng session và cookie,
# nó sử dụng một access_token với mỗi request.

# API thao tác với các Resource, và các Resource phải là các class
# vì thế trong class phải thừa kế Resource

# import request, vì khi ai đó thực hiện 1 req tới api

# Token-based authentication là phương thức xác thực bằng chuỗi má hóa.
# Một hệ thống sử dụng Token-based authentication cho phép người dùng nhập user/password
# để nhận về 1 chuỗi token.
# Chuỗi Token này được sử dụng để “xác minh” quyền truy cập vào tài nguyên
# mà không cần phải cung cấp lại username/password nữa.

# Định dạng JSON sử dụng các cặp key – value
# Chuỗi JSON được bao lại bởi dấu ngoặc nhọn {}
# các key, valuecủa JSON bắt buộc phải đặt trong dấu nháy kép {“},
# nếu bạn đặt nó trong dấu nháy đơn thì đây không phải là một chuỗi JSON đúng chuẩn
# var minh = {
#    "firstName" : "Minh",
#    "lastName" : "Nguyen",
#    "age" :  "34"
# };

# JSON Web Token là một chuỗi mã hóa mà nguồn gốc ban đầu là một chuỗi JSON.
# Chuỗi thông tin dạng JSON bằng phương pháp mã hóa nào đó,
# nó trở thành 1 chuỗi ký tự lộn xộn nhìn vào sẽ rất khó hiểu
# Bảo mật JWT là phuơng pháp xác thực quyền truy cập (Authentication) bằng JSON Web Token

# JWT trên bao gồm 3 phần:
# Header
# Payload
# Signature
# vd: <base64-encoded header>.<base64-encoded payload>.<HMACSHA256(base64-encoded signature)>

# ví dụ: muốn gửi 1 message: "Hello" và không muốn ai thấy nó, thì mình sẽ encode message đó để không ai hiểu được
# trừ khi họ có khóa giải mã cụ thể cho cái message đó
# user có 1 mã định danh riêng biệt, username, password
# user sẽ gửi cho ta username, password, sau đó ta gửi ngc lại client 1 JWT, cái JWT đó là userID
# khi client có JWT, thì họ có thể gửi bất cứ request nào

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# This turns off the flask SQLAlchemy modification tracker.
# It does not turn off the SQLAlchemy modification tracker.
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)
# jwt sẽ tạo ra endpoint mới : /auth
# khi gọi /auth thì ta sẽ gửi 1 username và password
# và jwt sẽ lấy username, password và gửi đến hàm authenticate
# nếu match thì nó sẽ gửi lại 1 object user
# /auth sẽ trả về 1 JW Token
# sau đó ta sẽ gửi cái token đó đến hàm identity: JWT sẽ  gọi hàm identity
# và nó sẽ sử dụng JWT Token để lấy userID

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# trong postman nếu ghi /item/name đầu tiên nó sẽ xem
# phương thức là GET hay POST đề vào class Item lấy phương thức đó ra mà sử dụng
# dữ liệu trả về phải là 1 dictionary, sau đó dictionary sẽ ép kiểu thành liểu str để api có thể đọc

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=2000, debug=True)
