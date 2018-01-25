from .. import db
from utils import to_datetime

class Param(db.Model):
    __tablename__ = 'common_info'

    common_info_id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, nullable= False)
    biz_serial_no = db.Column(db.String(48), nullable= False, unique= True)
    imei = db.Column(db.String(32))
    cplc = db.Column(db.String(84), nullable= False)
    mobile_number = db.Column(db.String(11))
    rom_version = db.Column(db.String(128))
    api_level = db.Column(db.String(32))
    ws_version = db.Column(db.String(64))
    package_version_code = db.Column(db.String(16))
    create_timestamp = db.Column(db.datetime, nullable=False, server_default=db.FetchedValue())
    update_timestamp = db.Column(db.datetime, nullable=False, server_default=db.FetchedValue())
