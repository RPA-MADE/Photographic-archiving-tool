import ctypes
import msvcrt
import os
import shutil
import exifread
from datetime import datetime

__author__ = 'Duckweeds7'
__website__ = 'https://www.duckweeds7.com'
__mail__ = 'root@duckweeds7.com'
__copyright__ = 'Copyright © 2023 RPA-MADE'
__product__ = "简易摄影作品归档工具"
ctypes.windll.kernel32.SetConsoleTitleW(__product__)
logo = f"""
 ____  ____   _         __  __    _    ____  _____ 
|  _ \|  _ \ / \       |  \/  |  / \  |  _ \| ____|
| |_) | |_) / _ \ _____| |\/| | / _ \ | | | |  _|  
|  _ <|  __/ ___ \_____| |  | |/ ___ \| |_| | |___ 
|_| \_\_| /_/   \_\    |_|  |_/_/   \_\____/|_____|\n
欢迎使用<{__product__}>，联系邮箱：root@duckweeds7.com\n
软件功能为将指定文件夹内的文件（文件后缀名为'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi'）按照文件的摄影日期或修改日期进行分类，分类产生的文件夹命名格式为：年_月_日
"""
print(logo)
# 输入源文件夹路径
source_folder = input("请输入文件夹路径<直接按回车键为整理程序所在位置的文件夹>：")
if not source_folder:
    source_folder = os.getcwd()
print(f"文件夹路径：{source_folder}")
destination_folder = source_folder
os.makedirs(destination_folder, exist_ok=True)

# 遍历源文件夹中的文件
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    try:

        # 检查文件是否为图片或视频
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi')):

            # 尝试从文件的元数据中获取原始拍摄日期
            try:
                with open(file_path, 'rb') as file:
                    tags = exifread.process_file(file, stop_tag='EXIF DateTimeOriginal')
                    date_taken = datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
            except (KeyError, FileNotFoundError):
                # 获取不到拍摄日期时使用修改日期
                date_taken = datetime.fromtimestamp(os.path.getmtime(file_path))

            # 根据日期创建目标文件夹路径
            destination_subfolder = os.path.join(destination_folder, date_taken.strftime('%Y_%m_%d'))
            os.makedirs(destination_subfolder, exist_ok=True)

            # 移动文件到目标文件夹
            destination_path = os.path.join(destination_subfolder, filename)
            shutil.move(file_path, destination_path)
    except Exception as e:
        print(e)

# 完成分类
print("归档完成！按任意键退出程序")
msvcrt.getch()
