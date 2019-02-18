# BoundingBox project: Web Service

from flask import Flask,request,Response,render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image, ImageDraw
import json,cPickle,os,subprocess
from random import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "eef65aea452450e107aff71df4c8511124e58b58b70e03a2344a6c53426e381e"
CORS(app)
socketio = SocketIO(app)

global server_host, server_port, base_images, edit_counts, saved_coords, localdb, localdbf

server_host = "172.31.27.245"
server_port = 3024
base_images = {
    "bottles":"/home/ec2-user/app/static/bottles_%s.jpg",
    "xmen":"/home/ec2-user/app/static/xmen_%s.jpg"
}
saved_coords = {
    "bottles":[],
    "food":[],
    "xmen":[]
}
localdbf = os.getcwd()+"/localdb.pkl"

def set_db(data):
    p = open(localdbf,"wb+")
    p.write(cPickle.dumps(data))
    p.close()
    return None

def get_db():
    p = open(localdbf,"rb+")
    data = cPickle.loads(p.read())
    p.close()
    return data

# initialize localdb
try:
    localdb = get_db()
except:
    set_db(saved_coords)
    localdb = get_db()

edit_counts = {}
for image in base_images:
    edit_counts[image] = len(localdb[image])

def nonce():
    return int(100000*random())

def run(cmds):
    try:
        proc = subprocess.Popen([cmds],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,) ; stdout_value = proc.communicate()
        return stdout_value[0]
    except Exception as Error:
        return str(Error)

def make_points(coordset):
    return map(lambda x:tuple(x),coordset)

def add_bounding_box_to_image(base_image,coordset):
    # PIL based image editing
    global edit_counts, localdb
    source_img = Image.open(base_images[base_image] % edit_counts[base_image]).convert("RGBA")
    edit_counts[base_image]+=1
    draw = ImageDraw.Draw(source_img)
    draw.line(make_points(coordset), fill="yellow", width=2)
    source_img.save(base_images[base_image] % edit_counts[base_image], "JPEG")
    # update DB with latest boundingbox coordinates
    localdb = get_db()
    localdb[base_image].append(coordset)
    set_db(localdb)
    return None

def responsify(status,message,data={}):
    code = int(status)
    a_dict = {"data":data,"message":message,"code":code}
    return Response(json.dumps(a_dict), status=code, mimetype='application/json')

def return_url(file):
    return "http://app.tr1pp.me/hosted/files/%s?nonce=%s" % (file,nonce())

@app.route("/boundingbox/api/new_box",methods=["POST"])
def new_box():
    # write new bounding box to image, return updated URL
    formdata = request.get_json(force=True)
    box = formdata["box"]; first = box[0]; box.append(first) # close box boundary
    image = formdata["image"]
    add_bounding_box_to_image(image,box)
    return responsify(200,"load this URL",{"url":"http://app.tr1pp.me:3024/boundingbox/api/serve_image?image=%s&index=%s&nonce=%s" % (image,edit_counts[image],nonce())})

@app.route("/boundingbox/api/new_session/<path:image>")
def new_session(image):
    global localdb, edit_counts
    # clear image edits
    for i in xrange(edit_counts[image]):
        run("sudo rm /home/ec2-user/app/static/%s_%s.jpg" % (image,i+1))
    # reset image database entry and image edit count
    localdb = get_db(); localdb[image] = []; set_db(localdb)
    edit_counts[image] = 0
    return responsify(200,"Session Reset OK")

@app.route("/boundingbox/api/serve_image")
def serve_image():
    # serve images from browser
    args = dict(request.args); args = {x:args[x][0] for x in args}
    if args:
        if "image" in args and "index" in args:
            base_image = args["image"]; index = args["index"]
            return render_template("bbdisplay.html",image=return_url("%s_%s.jpg" % (base_image,index)))
        else:
            return render_template("bbdisplay.html",image=return_url("404.png"))
    else:
        return render_template("bbdisplay.html",image=return_url("404.png"))

if __name__ == "__main__":
   socketio.run(app,host=server_host,port=server_port)
