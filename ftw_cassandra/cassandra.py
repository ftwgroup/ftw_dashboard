from pycassa import NotFoundException, InvalidRequestException

class Cassandra(object):
    """
    This is the base class for any Cassandra database access object
    """
    def __init__(self, acct):
        self.acct = acct

    def _get_records(self, col_family, start, limit = 10):
        """
        Gets a stream. A stream can be a mailbox, email thread, etc.
        """
        # First we need to retrieve a raw stream (in the form of email ids)

        # We get one more email than asked for, if we exceed the limit by doing
        # so, that email key (__) becomes what is returned as next for pagination
        start = start if start else ''
        nextKey = None
        try:
            stream = col_family.get(self.acct, column_start=start,
                            column_count=limit + 1, column_reversed=True)
        except NotFoundException:
            return [], nextKey

        if len(stream) > limit:
            # Find the minimum __ from our get (the oldest one), and convert it
            # to a non-floating value.
            oldest = min(stream.keys())

            # Present the string version of the oldest key (__)
            nextKey = str(oldest)

            # And then convert the pylong back to a bitpacked key so we can delete
            # it from the stream
            del stream[oldest]

        return nextKey, stream

    def _set_records(self, col_family, data):
        """
        :param cf: ColumnFamily
        :param data: a dict of dicts. Your dict keys becomes the cassandra key
        """
        insert_count = 0

        with col_family.batch() as b:

            try:
                for key, value in data.iter_items():
                    if isinstance(value, dict):
                        print "warn: dict expected"
                        insert_count += 1
                    else:
                        b.insert(key, value)

            except InvalidRequestException, e:
                print e
                insert_count = 0

        return insert_count
