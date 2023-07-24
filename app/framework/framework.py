import pytest


@pytest.fixture
def setup():
    # 初始化SDK
    print("setup")


def test_action():
    # 1.读取测试用例
    # 2.基于用例类型执行对应的测试
    # 3.断言测试结果
    # 4.调用SDK上报数据
    print("test_action")
    assert True


@pytest.fixture
def teardown():
    # 清理工作
    print("teardown")
    assert True
