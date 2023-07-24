from sdk import MoloConsumer, MoloSDK

if __name__ == '__main__':
    consumer = MoloConsumer("http://127.0.0.1:8080/ping")
    molo = MoloSDK(consumer)

    molo.track("test", "test1234")
