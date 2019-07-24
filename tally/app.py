import json
import logging
import os

from flask import Flask, jsonify

from models import *

__author__ = "Foo Bar"
__version__ = "0.0.1"
__maintainer__ = "Enterprise Security"
__email__ = "foo.bar@twitter.com"
__status__ = "alpha"

try:
  logging.basicConfig(filename="./tally.log", level="DEBUG")
  # flask service
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tally.db"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
except Exception as e:
  raise Exception("Core database loading errors have occured.")

@app.route("/api/v2/machines/<int:id>", methods=["GET"])
def get_machines_by_id(id):
  try:
    Machine.query.count()
  except Exception:
    load_example_data()
  try:
    machine = Machine.query.get(id)
    payload = jsonify(machine.to_json())
    return payload, 200
  except Exception as e:
    # What if machine doesn't exist?
    logging.exception(str(e))
    return jsonify({"success": False}), 400

# TODO:
# @app.route("/api/v2/machines", methods=["GET"])
# ...


def load_example_data():
  db.create_all()
  with open("example_data.json") as f:
    machines = json.load(f)["machines"]
  for machine_data in machines:
    db.session.add(Machine(**machine_data))
    db.session.commit()
    print(f"loaded example data: {len(machines)} machines")


app.run(port=8080, debug=True)
