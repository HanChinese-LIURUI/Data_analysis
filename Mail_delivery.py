from email.mime.text import MIMEText  # 专门发送正文
from email.mime.multipart import MIMEMultipart  # 发送多个部分
from email.mime.application import MIMEApplication  # 发送附件
import smtplib  # 发送邮件


def Mail(path):
    try:
        filepath = path  # 附件路径
        send_user = 'pythonhalp@163.com'  # 发件人
        password = 'xinghan1996'  # 授权码/密码
        receive_users = '1090339852@qq.com'  # 收件人，可为list
        subject = '数据查重数据回传'  # 邮件主题
        email_text = '删除数据'  # 邮件正文
        server_address = 'smtp.163.com'  # 服务器地址

        # 构造一个邮件体：正文 附件
        msg = MIMEMultipart()
        msg['Subject'] = subject  # 主题
        msg['From'] = send_user  # 发件人
        msg['To'] = receive_users  # 收件人

        # 构建正文
        part_text = MIMEText(email_text)
        msg.attach(part_text)  # 把正文加到邮件体里面去

        # 构建邮件附件
        # file = file           #获取文件路径
        part_attach1 = MIMEApplication(open(filepath, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=filepath)  # 为附件命名
        msg.attach(part_attach1)  # 添加附件

        # 发送邮件 SMTP
        smtp = smtplib.SMTP(server_address, 25)  # 连接服务器，SMTP_SSL是安全传输
        smtp.login(send_user, password)
        smtp.sendmail(send_user, receive_users, msg.as_string())  # 发送邮件
    except:
        pass


if __name__ == "__main__":
    Mail(r'C:\Users\LIURUI\Desktop\1.txt')
