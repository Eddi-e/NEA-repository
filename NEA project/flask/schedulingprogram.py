import time
from datetime import datetime
datestore = 9
while True:
    weekofday = (datetime.today().weekday())
    time.sleep(300)
    if weekofday != datestore:
        datestore == weekofday
        print(True)

    else:
        print(False)