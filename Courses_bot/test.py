from core.utils.database import db
from datetime import datetime

name_comp = 'send' + datetime.now().isoformat(timespec='hours')
name_comp = name_comp.replace("-", "_")
print(name_comp)
if not db.check_table(name_comp):
    db.create_sender_table(name_comp)
    print("yeeeeeeey")



