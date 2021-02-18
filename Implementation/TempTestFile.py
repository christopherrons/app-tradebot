import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Utils.TradebotUtils import TradeBotUtils

current_formation_log_file = os.path.realpath(__file__).replace("Implementation/TempTestFile.py",
                                                                "logs/current_formation_log.csv")  # Shitty solution
successful_trade_log_file = os.path.realpath(__file__).replace("Implementation/TempTestFile.py",
                                                               "logs/trades_logs.csv")  # Shitty solution

email_source = TradeBotUtils.get_email_source()
email_source_password = TradeBotUtils.get_email_source_password()
email_target = TradeBotUtils.get_email_target()

message = MIMEMultipart()
message['From'] = email_source
message['To'] = email_target
message['Subject'] = "Trade Occured"
message.attach(MIMEText('Trade Occured test', 'plain'))

current_information_log = open(current_formation_log_file, "rb")
trade_log = open(successful_trade_log_file, "rb")

part_information = MIMEBase('applications', 'octet-stream')
part_information.set_payload(current_information_log.read())
encoders.encode_base64(part_information)
part_information.add_header('Content-Disposition',
                            'attachment; filename=%s' % os.path.basename(current_formation_log_file))
message.attach(part_information)

part_trade = MIMEBase('applications', 'octet-stream')
part_trade.set_payload(trade_log.read())
encoders.encode_base64(part_information)
part_trade.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(successful_trade_log_file))
message.attach(part_trade)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

server.login(email_source, email_source_password)
text = message.as_string()
server.sendmail(email_source, email_target, text)
server.quit()

current_information_log.close()
trade_log.close()
