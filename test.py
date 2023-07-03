from datetime import datetime
from time import sleep


def formatDifference(difference):
    hours = int(difference / 3600)
    minutes = int(difference % 3600 / 60)
    seconds = int((difference % 3600) % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'



# sT = datetime.strptime('04/04/21 09:31:22', '%d/%m/%y %H:%M:%S')
sT = datetime.now().replace(microsecond=0)
startDate = sT.strftime("%d-%m-%Y")
startTime = sT.strftime("%H:%M:%S")

sleep(1)

eT = datetime.now().replace(microsecond=0)
endDate = eT.strftime("%d-%m-%Y")
endTime = eT.strftime("%H:%M:%S")
difference = (eT - sT).total_seconds()

print(sT)
print(startDate)
print(startTime)

print(difference)

print(formatDifference(difference))