from EigerApi import EigerApi
from EigerMock.EigerMock import init_detector

if __name__ == "__main__":
    mock = init_detector()
    api = EigerApi(mock)
    api.run()