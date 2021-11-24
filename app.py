import logging as rel_log
import os
from datetime import timedelta
from flask import *
from yolov5.detect import *


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'mp4', 'avi'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = './yolov5/data/images'

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        while(1):
            if (os.path.exists('D:/teamwork/back-end/yolov5/data/images/'+file.filename))==True:
                break
        result_path,ansDict = run(source='D:/teamwork/back-end/yolov5/data/images/'+file.filename)
        return jsonify({'status': 1,'msg':'成功上传，预测完毕','path':result_path,'dict':ansDict})

    return jsonify({'status': 0})


@app.route("/download", methods=['POST'])
def download_file():
    get_data=request.get_data()
    get_data=json.loads(get_data)
    videopath=get_data.get('videopath')
    videoname=get_data.get('videoname')
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory(videopath, videoname, as_attachment=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
