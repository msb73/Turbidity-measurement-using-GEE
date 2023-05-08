from datetime import datetime
givendate = '12-05-2000'
date_obj = datetime.strptime(givendate, '%d-%m-%Y').__str__()
print(date_obj)