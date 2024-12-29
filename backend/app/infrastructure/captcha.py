from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random
import string
import os

class CaptchaGenerator:
    def __init__(self):
        # 字体文件路径
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'arial.ttf')
        self.font = ImageFont.truetype(font_path, 28)
        
    def generate(self) -> tuple[str, bytes]:
        """生成验证码"""
        # 生成随机验证码
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=4))
        
        # 创建图片
        width = 120
        height = 36
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # 添加干扰
        self._add_noise(draw, width, height)
        
        # 绘制文字
        for i, char in enumerate(code):
            x = 20 * i + 15
            y = random.randint(2, 6)
            draw.text((x, y), char, font=self.font, fill=self._random_color())
            
        # 转换为bytes
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        
        return code, buffer.getvalue()
    
    def _add_noise(self, draw: ImageDraw, width: int, height: int):
        """添加干扰元素"""
        # 添加干扰点
        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=self._random_color())
            
        # 添加干扰线
        for _ in range(3):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line(((x1, y1), (x2, y2)), fill=self._random_color())
    
    def _random_color(self) -> tuple:
        """生成随机颜色"""
        return (
            random.randint(32, 127),
            random.randint(32, 127),
            random.randint(32, 127)
        )

captcha_generator = CaptchaGenerator() 