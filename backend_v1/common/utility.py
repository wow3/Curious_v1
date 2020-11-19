import random, string
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

class ImageCode:
    # 生成绘制字符串的随机颜色
    def random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return red, green, blue

    # 生成四位随机字符
    def get_text(self):
        # 可以从列表或字符串中，随机取得n个字符，构建一个子列表
        list = random.sample(string.ascii_letters+string.digits, 4)
        # print(list)
        return ''.join(list)

    # 随机画线
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.get_text()
        width, height = 120, 50     # 图片大小
        img = Image.new('RGB', (width, height), 'white')    # 背景白色
        # 选择字体及大小
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(img)      # 创建ImageDraw对象
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)), text=code[i], fill=self.random_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 2, width, height)
        # img.show()    # 临时调试，显示
        return img, code

    # 生成图片验证码，并返回
    def get_code(self):
        img, code = self.draw_verify_code()
        buf = BytesIO()
        img.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring


from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header


# 发送qq邮箱验证码，参数为收件箱地址和随机生成的验证码
def send_email(receiver, ecode):
    # 发件者
    sender = 'TwowD <497536112@qq.com>'
    # 邮件内容html格式
    content = f"<br/>欢迎注册Curious社区账号，您的邮箱验证码为："\
            f"<span style='color:red; font-size: 20px;'>{ecode}</span>, "\
            f"请复制到注册窗口完成注册，感谢您的支持。<br/>"
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('Curious社区注册验证码', 'utf-8')
    message['From'] = sender
    message['To'] = receiver

    smtpObj = SMTP_SSL('smtp.qq.com')
    smtpObj.login(user='497536112@qq.com', password='lxagzlefoatzbhcf')
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()


# 生成6位随机字符床作为邮箱验证码
def get_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)


if __name__ == '__main__':
    code = get_email_code()
    print(code)
    # send_email('170200810@stu.hit.edu.cn', code)
    send_email('2513105294@qq.com', code)