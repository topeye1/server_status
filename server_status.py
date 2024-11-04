import time
import psutil
from con_db import MariaDB


def server_status():
    try:
        # CPU 사용률 조회
        cpu_usage_percent = psutil.cpu_percent(interval=1)
        # CPU 코어 수 조회
        cpu_count = psutil.cpu_count(logical=False)
        # CPU freq
        cpu_freq_info = psutil.cpu_freq(percpu=True)
        cpu_freq = cpu_freq_info[0].current

        # 전체 메모리 정보
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total / (1024 * 1024 * 1024)
        memory_percent = memory_info.percent

        try:
            datas = {
                'cpu_count': cpu_count,
                'cpu_size': round(cpu_freq / 1024, 2),
                'cpu_rate': round(cpu_usage_percent),
                'ram_size': round(total_memory, 1),
                'ram_rate': round(memory_percent)
            }
            types = {
                'cpu_count': 'int',
                'cpu_size': 'str',
                'cpu_rate': 'str',
                'ram_size': 'str',
                'ram_rate': 'str'
            }
            where = f"server_name='maker'"
            mbd = MariaDB()
            mbd.updateServerStatus(datas, types, where)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        server_status()
        time.sleep(30)
