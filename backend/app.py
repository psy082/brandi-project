import decimal
import datetime

from flask      import Flask
from flask.json import JSONEncoder
from flask_cors import CORS

from model      import UserDao, OrderDao
from service    import UserService, OrderService
from view       import create_user_endpoints, create_admin_user_endpoints, create_admin_order_endpoints

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        """

        Args:
            obj : json 형태로 반환하고자 하는 객체

        Returns:
            obj를 json 형태로 변경하는 기능이 추가된 JSONEncoder

        Authors:
            tnwjd060124@gmail.com (손수정)

        History:
            2020-08-24 (tnwjd060124@gmail.com) : 초기 생성

        """

        if isinstance(obj, decimal.Decimal):
            return float(obj)

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        return JSONEncoder.default(self, obj)

def create_app():
    """

    Returns :
        생성된 플라스크 앱 객체

    Authors :
        tnwjd060124@gmail.com (손수정)

    History :
        2020-08-19 (tnwjd060124@gmail.com) : 초기 생성

    """

    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    #CORS 설정
    CORS(app)
    #config 설정
    app.config.from_pyfile("config.py")
    # DAO 생성
    user_dao = UserDao()
    order_dao = OrderDao()
    # Service 생성
    user_service = UserService(user_dao)
    order_service = OrderService(order_dao)
    # view blueprint 등록
    app.register_blueprint(create_user_endpoints(user_service))
    app.register_blueprint(create_admin_user_endpoints(user_service))
    app.register_blueprint(create_admin_order_endpoints(order_service))

    return app
