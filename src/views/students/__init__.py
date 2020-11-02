from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime.today()

dated = today.strftime("%d-%m-%Y %H:%M:%S")

students_dated = today.strftime("%d-%m-%Y")

end_dated = today + relativedelta(years=4)
end_dated = end_dated.strftime("%d-%m-%Y")
