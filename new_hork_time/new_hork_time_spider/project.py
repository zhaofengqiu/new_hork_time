from flask import Flask
import config,os,re
app = Flask(__name__)

app.config.from_object(config)
@app.route('/')
def hello_world():
    log=''
    logs=open(r'/root/myproject/new_hork_time/temp.log',encoding='utf-8',errors='ignore').readlines()[-3000:]
    for t in logs:
        if len(re.findall('insert succeed| running start',t,re.S)):
            log=log+'<p>'+t+'</p>'
    return log
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
