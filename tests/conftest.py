def pytest_configure(config):
    from gqlclans.contrib.session import PapiRequestSession
    from tests.requestsnapshot import FileSnapshotStore, SnapshotAdapter
    s_adaptor = SnapshotAdapter(FileSnapshotStore('tests/testsnapshots'))

    PapiRequestSession.adapters['https://'] = s_adaptor


def pytest_unconfigure(config):
    from gqlclans.contrib.session import PapiRequestSession
    del PapiRequestSession.adapters['https://']
