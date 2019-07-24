# For reference:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records

# 3rd party lib imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text, DateTime

__author__ = "Foo Bar"
__version__ = "0.0.1"
__maintainer__ = "Enterprise Security"
__email__ = "foo.bar@twitter.com"
__status__ = "beta"

db = SQLAlchemy()

vulnscan_association_table = db.Table(
  'machine_vulnscan',
  db.metadata,
  db.Column('machine_id', db.Integer, db.ForeignKey('machine.id')),
  db.Column('vulnscan_id', db.Integer, db.ForeignKey('vulnscan.id')),
)


class Machine(db.Model):
  __tablename__ = 'machine'
  id = db.Column(Integer, primary_key=True)
  ip_addr = db.Column(String(100))
  # TODO hostname = ??? what to put here ???
  # vulnscan = db.relationship(
  #   "VulnScan",
  #   backref="machine",
  #   order_by="desc(VulnScan.id)",
  # )

  def to_json(self, vulnscan=False):
    result = {
      "id": self.id,
      "ip_addr": self.ip_addr,
      # "hostname": self.hostname,
    }
    if vulnscan == True:
      result["vulnscans"] = [o.to_json() for o in self.vulnscan]
    return result

  def count_vulnscans(self):
    raise NotImplementedError('''
TODO: return the total count of vuln scans that have run against this machine:
  {
    "id": 22,
    "ip_addr": "",
    "hostname": "example.twitter.com",
    "count": 123
  }
    ''')


class VulnScan(db.Model):
  __tablename__ = "vulnscan"
  id = db.Column(Integer, primary_key=True)
  # TODO need to track if it's been soft deleted or not
  # TODO need to track the number of vulnerabilities we observed
  # TODO need to track a description of the CVEs
  # TODO need to track when exactly this was observed

  @classmethod
  def run_vulnscan(cls):
    # TODO
    for machine in Machine.query.all():
      # Assume the description is always "CVE-2019-0001" and that every machine
      # matches.
      pass
    raise NotImplementedError()

  def to_json(self):
    raise NotImplementedError()

  def most_recent(self, start_date=None):
    raise NotImplementedError('''
TODO: get the most recent vulnscans and machine ids affected. Example:
  {
    "machine_ids": [1, 2, 3],
    "description": "this is our scan of CVE-2019-001 and CVE-2019-002",
    "count": 333
  }
    ''')
