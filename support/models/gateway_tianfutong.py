from .. import db
from ..import utils

class Param(db.Model):
    __tablename__ = 'common_info'
    
    common_info_id
    device_id
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