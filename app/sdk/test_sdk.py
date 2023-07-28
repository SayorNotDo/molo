from sdk import MoloConsumer, MoloSDK
from pkg.utils.network.wifi import get_wifi_info

if __name__ == '__main__':
    consumer = MoloConsumer("http://127.0.0.1:8080/ping")
    molo = MoloSDK(consumer)

    get_wifi_info(molo.track, task_name="test", execute_id="test1234", track_type="monitor")
