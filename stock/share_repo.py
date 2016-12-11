import share


class ShareRepository(object):
    repo = {}

    def _factory(self, share_name, s_type='common', par_val=0,
                 dividend_par_val=0):
        """

        :param share_name: Name of a share
        :param s_type: Type of a share (Common, Preferred)
        :param par_val: Nominal price of a preferred share
        :param dividend_par_val: Dividend percents for preferred share
        :return:
        """
        if share_name not in self.repo:
            if s_type == 'common':
                s = share.Share(share_name)
            elif s_type == 'preferred':
                s = share.PreferredShare(share_name, par_val, dividend_par_val)
            else:
                raise ShareRepositoryException('''Share can be only of type
                preferred or common.''')
            self.repo[share_name] = s
        return self.repo[share_name]

    def get_share(self, name, *args):
        return self._factory(name, *args)

    def __iter__(self):
        return self.repo.itervalues()

    def __len__(self):
        return len(self.repo)


class ShareRepositoryException(Exception):
    pass