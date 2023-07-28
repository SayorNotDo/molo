import base64
import datetime
import gzip
import io
import json
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Any


class MoloException(Exception):
    pass


class MoloIllegalDataException(MoloException):
    """
    在发送的数据格式有误时，SDK会抛出此异常，用户应当捕获并处理。
    """
    pass


class MoloNetworkException(MoloException):
    """
    在因为网络或者不可预知的问题导致数据无法发送时，SDK会抛出此异常，用户应当捕获并处理。
    """
    pass


class MoloSDK:
    class DatetimeSerializer(json.JSONEncoder):
        """ data 和 datetime 类型的 JSON 序列化"""

        def default(self, o: Any) -> Any:
            if isinstance(o, datetime.datetime):
                head_fmt = "%Y-%m-%d %H:%M:%S"
                return "{main_part}.{ms_part}".format(
                    main_part=o.strftime(head_fmt),
                    ms_part=int(o.microsecond / 1000))
            elif isinstance(o, datetime.date):
                fmt = '%Y-%m-%d'
                return o.strftime(fmt)
            return json.JSONEncoder.default(self, o)

    def __init__(self, consumer=None, task_name=None):
        """
        :param consumer:
        :param task_name:
        """
        self._consumer = consumer
        self._task_name = task_name

    @staticmethod
    def _now():
        return int(time.time() * 1000)

    @staticmethod
    def _json_dumps(data):
        custom_separators = (',', ':')
        return json.dumps(data, separators=custom_separators, cls=MoloSDK.DatetimeSerializer)

    @staticmethod
    def _assert_key(key):
        if not isinstance(key, str):
            raise MoloIllegalDataException("key must be a str. [key=%s]" % str(key))
        if len(key) > 255:
            raise MoloIllegalDataException("the max length of key is 256. [key=%s]" % str(key))

    @staticmethod
    def _assert_value(value, key=None):
        pass

    @staticmethod
    def _normalize_data(data):
        # 检查 execute_id
        if data["execute_id"] is None or len(str(data['execute_id'])) == 0:
            raise MoloIllegalDataException("property [execute_id] must not be empty")
        if len(str(data['execute_id'])) > 255:
            raise MoloIllegalDataException("the max length of property [execute_id] is 255")
        data['execute_id'] = str(data['execute_id'])

        # 检查 time
        if isinstance(data['time'], datetime.datetime):
            data['time'] = time.mktime(data['time'].timetuple()) * 1000 + data['time'].microsecond / 1000

        ts = int(data['time'])
        ts_num = len(str(ts))
        if ts_num < 10 or ts_num > 13:
            raise MoloIllegalDataException("property [time] must be a timestamp in microseconds")

        if ts_num == 10:
            ts *= 1000
        data['time'] = ts

        # 检查 properties
        MoloSDK._normalize_properties(data)
        return data

    @staticmethod
    def _normalize_properties(data):
        if "properties" in data and data["properties"] is not None:
            for key, value in data["properties"].items():
                MoloSDK._assert_key(key)
                MoloSDK._assert_value(value, key)

    def _track(self, track_type, task_name, execute_id, properties):
        """
        :param track_type:
        :param execute_id:
        :param properties
        :return:
        """
        track_time = self._now()
        data = {
            'type': track_type,
            'time': track_time,
            'execute_id': execute_id,
            'properties': properties,
        }
        if self._task_name is not None:
            data['task'] = self._task_name
        data = self._normalize_data(data)
        self._consumer.report(self._json_dumps(data))

    def track(self, properties=None, task_name=None, execute_id=None, track_type=None):
        """
        跟踪一个用户的行为。

        :param track_type:
        :param task_name:
        :param execute_id: 执行的唯一标识
        :param properties: 上报属性集合
        """
        self._track(track_type, task_name, execute_id, properties)


class MoloConsumer:
    def __init__(self, url: str = None, request_timeout: int = None):
        """
        :param url: 后台URL地址
        :param request_timeout: 请求的超时时间，单位：秒
        """
        self.url = url
        self.request_timeout = request_timeout

    @staticmethod
    def _gzip_string(data):
        try:
            return gzip.compress(data)
        except AttributeError:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="w") as fd:
                fd.write(data)
            return buf.getvalue()

    def _do_request(self, data):
        encoded_data = urllib.parse.urlencode(data).encode('utf8')
        try:
            request = urllib.request.Request(self.url, encoded_data)
            if self.request_timeout is not None:
                urllib.request.urlopen(request, timeout=self.request_timeout)
            else:
                urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            raise MoloNetworkException(e)
        return True

    def report(self, msg):
        return self._do_request({
            'data': self._encode_msg(msg)
        })

    def _encode_msg(self, msg):
        return base64.b64encode(self._gzip_string(msg.encode('utf8')))
