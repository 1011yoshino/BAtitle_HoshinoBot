from .draw import draw_pic
import os
from io import BytesIO
from hoshino import Service, R
from hoshino.typing import CQEvent

sv = Service(
    'ba标题', 
    enable_on_default=True
    )

@sv.on_prefix(('ba标题', 'balogo', 'balg'))
async def balogo(bot, ev: CQEvent):
    msg_list = []
    key = ev.message.extract_plain_text().strip()
    try:
        keyword: str = key
        if "｜" in keyword:
            keyword = keyword.replace("｜", "|")
        upper = keyword.split("|")[0].strip()
        downer = keyword.split("|")[1].strip()
        #进行图片加工
        img_raw = draw_pic(front=upper, back=downer)
        #初始化一个空字节流
        img = BytesIO()
        #把我们得图片以‘PNG’保存到空字节流
        img_raw.save(img, format="png")
        #无视指针，获取全部内容，类型由io流变成bytes。
        img_bytes: bytes = img.getvalue()
        # 保存到本地
        with open(os.path.join("res/img/batitlelogo.png"),'wb') as file:
            file.write(img_bytes)  # 保存到本地
        img_raw.close()
        img.close()
        pic = R.img(f"batitlelogo.png").cqcode
        msg_list = pic
    except OSError:
        msg_list = "生成失败……请检查字体文件设置是否正确"
    except IndexError:
        msg_list = "生成失败……请检查命令格式是否正确"
    await bot.send(ev, msg_list)