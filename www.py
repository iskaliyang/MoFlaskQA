from application import app
from views.home.home import home

from views.home.question_answer import qa


# 公共蓝图
app.register_blueprint(home, url_prefix='/')
# 问答蓝图
app.register_blueprint(qa, url_prefix='/qa')
