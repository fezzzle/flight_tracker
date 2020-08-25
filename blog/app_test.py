import threading
import asyncio

from flask import Flask, jsonify


print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)

@app.route("/toy", methods=["GET"])
def index():
    print(f"Inside flask function: {threading.current_thread().name}")

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(hello())

    return jsonify({"result": result})


async def hello():
    await asyncio.sleep(1)
    return 1


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4567, debug=False)