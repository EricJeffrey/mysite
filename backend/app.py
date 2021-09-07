import os
from flask import Flask
from flask import request, abort
from queue import SimpleQueue
from collections import deque
from flask.helpers import send_from_directory, url_for
import urllib.parse

APP_BASE_DIR_PATH = "/data/site-of-jeff/"
STATIC_FILE_DIR_PATH = APP_BASE_DIR_PATH + "static/"


# --------------- PASTOR ---------------
PASTE_TEXT_LIST_MAX_SIZE = 100
pasteTextQ = deque()


def addToPastor(text):
    if len(pasteTextQ) >= PASTE_TEXT_LIST_MAX_SIZE:
        pasteTextQ.popleft()
    pasteTextQ.append(text)


# --------------- FILE-TRANSFER ---------------
FILE_TRANSFER_DIR_PATH = APP_BASE_DIR_PATH + "file-transfer/"


def putFile(file):
    # Bug: filename maybe fake, werkzeug.secure_filename() can help, but won't work for Chinese
    file.save(FILE_TRANSFER_DIR_PATH + urllib.parse.quote(file.filename))


def listAllFile():
    """ return: [{name:name, size:size-in-MB}] """
    return [{"name": urllib.parse.unquote(x), "size": os.path.getsize(FILE_TRANSFER_DIR_PATH + x) / 1024 / 1024}
            for x in os.listdir(FILE_TRANSFER_DIR_PATH)]


# --------------- FLASKAPP ---------------


def wrapResp(content, ok=True):
    return {"code": 1 if ok else 0, "content": content}


os.makedirs(STATIC_FILE_DIR_PATH, exist_ok=True)
os.makedirs(FILE_TRANSFER_DIR_PATH, exist_ok=True)

app = Flask(__name__, static_folder=STATIC_FILE_DIR_PATH)


@app.route("/")
def appIndex():
    return send_from_directory(STATIC_FILE_DIR_PATH, "index.html")


@app.route("/api/pastor/getall")
def pastorGetAllPastes():
    return wrapResp([x for x in pasteTextQ])


@app.route("/api/pastor/paste", methods=['POST'])
def pastorPaste():
    data = request.get_json()
    if data is not None and "content" in data:
        addToPastor(data["content"])
        return wrapResp("success")
    else:
        return wrapResp("Text not found", ok=False)


@app.route("/api/file-transfer/put", methods=["POST"])
def fileTransferPutFile():
    putFile(request.files['file'])
    return wrapResp("Doone")


@app.route("/api/file-transfer/listall", methods=["GET"])
def fileTransferListAllFile():
    return wrapResp(listAllFile())


@app.route("/api/file-transfer/download", methods=["GET"])
def fileTransferDownloadFile():
    filename = request.args.get("name")
    if filename is not None:
        filepath = FILE_TRANSFER_DIR_PATH + urllib.parse.quote(filename)
        if os.path.exists(filepath):
            return send_from_directory(FILE_TRANSFER_DIR_PATH,
                                       urllib.parse.quote(filename))
        else:
            return abort(404)
    else:
        return abort(400)
