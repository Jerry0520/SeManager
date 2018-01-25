from .. import db
from utils import to_datetime

class Param(db.Model):
    __tablename__ = 'common_info'

    common_info_id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, )
    biz_serial_no
    imei
    cplc
    mobile_number
    rom_version
    api_level
    ws_version
    package_version_code
    create_timestamp
    update_timestamp
