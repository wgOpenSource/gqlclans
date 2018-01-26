from promise import Promise
from promise.dataloader import DataLoader

from gqlclans import logic


class ClanLoader(DataLoader):
    def batch_load_fn(self, ids):
        return Promise.resolve([logic.get_clan_info(id) for id in ids])


class AccountLoader(DataLoader):
    def batch_load_fn(self, ids):
        return Promise.resolve([logic.get_account_info(id) for id in ids])


class DataLoaders:
    clan_loader = ClanLoader()
    account_loader = AccountLoader()
