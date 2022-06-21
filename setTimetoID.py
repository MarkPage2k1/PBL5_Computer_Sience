from datetime import datetime

# current dateTime
now = datetime.now()

# convert to string
date_time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
print('DateTime String:', date_time_str)

# Output 2021-07-20 16:26:24