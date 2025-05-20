# flask用于搭建 Web 服务，接收用户的请求，处理数据，并将图表数据或图表文件传递给前端
# Flask 创建 Flask Web 应用实例的核心类
# render_template 用于渲染 HTML 模板文件
from flask import Flask, render_template
# random库提供生成随机数的函数
import random

# 创建了一个 Flask 应用实例，并将其赋值给变量 app
# __name__是一个 Python 内置的特殊变量，它表示当前模块的名称。当直接运行这个脚本时，__name__ 的值是 '__main__'
app = Flask(__name__)

# @app.route('/'): 这是一个装饰器（Decorator）。在 Python 中，装饰器是一种修改函数行为的简洁方式。
# @app.route('/') 的作用是将函数 index() 绑定到 Web 应用的根路径 /。
# 当用户在浏览器中访问应用的根 URL (例如 http://127.0.0.1:5000/) 时，Flask 会调用 index() 函数
@app.route('/')
def index():
    # 准备图表数据
    # labels 行创建了一个包含月份名称的列表，这个列表将作为图表的 X 轴标签
    labels = ["January", "February", "March", "April", "May", "June"]
    # data 行使用列表推导式创建了一个包含随机整数的列表
    data = [random.randint(10, 100) for _ in range(len(labels))]
    # 调用了 render_template() 函数，它的作用是渲染名为 index.html 的 HTML 模板文件，并将 labels 和 data 这两个 Python 变量传递给该模板
    # Flask 会在默认的 templates 文件夹中查找 index.html 文件
    return render_template('index.html', labels=labels, data=data)


app.run(debug=True)