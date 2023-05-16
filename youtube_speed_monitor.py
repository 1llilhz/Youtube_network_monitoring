import requests
import time
import base64
import time
import subprocess


# 定义 ADB 命令
adb_ip = 'adb connect 192.168.100.2'
print(adb_ip)
start_youtube = 'adb shell am start -W -a android.intent.action.VIEW -d "https://www.youtube.com/watch?v=rw7bxTqkYYs"  -n com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity'
capture_screen = 'adb shell screencap /sdcard/screenshot.png'

save_path = 'C:/Users/TCL/Desktop/Img'
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 执行 ADB 命令控制 Android 设备
subprocess.run('adb kill-server', shell=True)
subprocess.run(adb_ip, shell=True)
subprocess.run(start_youtube, shell=True)
print("视频已播放")
time.sleep(10)    # 等待 YouTube 视频加载完毕

# 设置持续时间，单位为秒
play_time = 15 * 60 * 60

# 设置截图间隔，单位为秒
screenshot_interval = 10

# 记录开始时间
start_time = time.time()

i = 1

while (time.time() - start_time) < play_time:
     
    subprocess.run(capture_screen, shell=True)
    subprocess.run(f'adb pull /sdcard/screenshot.png {save_path}/screenshot{i}.png', shell=True)
    time.sleep(1)    # 等待截图保存完成
    
    print(f'第{i}张图已保存，路径为 {save_path}/screenshot{i}.png')

    # 等待指定时间后继续下一次循环
    time_to_sleep = screenshot_interval - ((time.time() - start_time) % screenshot_interval)
    time.sleep(time_to_sleep)
    i += 1

    
# 关闭 YouTube 应用
subprocess.run('adb shell am force-stop com.google.android.youtube', shell=True)


connection_speed_list = []
fail_list = {}
res_data=''

# Get a list of all PNG files in the directory
png_files = [filename for filename in os.listdir(save_path) if filename.endswith('.png')]

# Sort the list by the numeric value in the filename
sorted_files = sorted(png_files, key=lambda x: int(x.strip("screenshot").strip(".png")))

# Print the sorted list of filenames
for filename in sorted_files:
    print(f'current processing: {os.path.join(save_path, filename)}')

    with open(os.path.join(save_path, filename), 'rb') as f:
        img = base64.b64encode(f.read())
        data = '{"image":"%s"}' % str(img)[2:]
        response = requests.post(
        'https://www.paddlepaddle.org.cn/paddlehub-api/image_classification/chinese_ocr_db_crnn_mobile',
         data=data)
        res_data = response.json()['result'].strip('\n')

    try:
        connection_speed = re.search('Connection Speed\s*(\d+)\s*K[bp]ps', res_data).group()
        output = connection_speed.lstrip('Connection Speed').rstrip('Kbps').strip()
        print(output)
        connection_speed_list.append(output)
        # print("________________")
    except Exception as e:
        # 处理异常情况
        fail_list[filename] = connection_speed
        print("Error while extracting text:", e)
    res_data = ''

print(fail_list)

print(connection_speed_list)
with open("OCR.txt","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Speed"])
    for item in connection_speed_list:
        writer.writerow([item])