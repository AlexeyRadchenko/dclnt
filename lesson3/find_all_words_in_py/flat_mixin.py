class FlatMixin:
    @staticmethod
    def flat(_list):
        """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
        return sum([list(item) for item in _list], [])

