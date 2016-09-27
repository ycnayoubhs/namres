import pymssql


class MsSQL(object):
    def __init__(self, host, db, user, psw):
        self.host = host
        self.db = db
        self.user = user
        self.psw = psw

    def __get_connect(self):
        if not self.db:
            raise (NameError, "No database configuration.")
        self.conn = pymssql.connect(self.host, self.user, self.psw, self.db)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, 'Connect database failed.')
        else:
            return cur

    def get_col_name(self, table_name):
        sql = "SELECT NAME FROM SYSCOLUMNS WHERE ID = OBJECT_ID(N'{table_name}') ORDER BY COLORDER".format(table_name=table_name)
        return tuple(item[0] for item in self.exec_query(sql))

    def get_col_property(self, table_name):
        sql = '''SELECT C.NAME, C.ISNULLABLE, T.NAME AS TYPE, C.LENGTH FROM SYSCOLUMNS C LEFT JOIN SYS.TYPES T on C.XUSERTYPE = T.USER_TYPE_ID 
                 WHERE C.ID = OBJECT_ID(N'{table_name}') ORDER BY C.COLORDER'''.format(table_name=table_name)
        return {
            item[0]: {
                'isnullable': item[1],
                'type': item[2],
                'length': item[3],
            }
            for item in self.exec_query(sql)
        }

    def exec_query(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        res = cur.fetchall()
        self.conn.close()
        return res

    def exec_non_query(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


# Decorator which reading config information in request to create
# a database helper object, and pass it to the decorated function.
# If no config information in request, use the default configuration.
def dbconn_required(db_auth_list):
    def _dbconn_required(func):
        def _get_dbconn(request, *args, **kwargs):
            auth = {
                'host': request.GET.get('host'),
                'user': request.GET.get('user'),
                'psw': request.GET.get('psw'),
                'db': request.GET.get('db'),
            }

            def _has_none():
                for k, v in auth.items():
                    if v is None:
                        return True

            if _has_none():
                db = request.GET.get('db')
                if db in db_auth_list:
                    auth = db_auth_list[db]
                else:
                    auth = db_auth_list['.']
            
            kwargs['db'] = MsSQL(host=auth['host'], user=auth['user'], psw=auth['psw'], db=auth['db'])
            return func(request, *args, **kwargs)
        return _get_dbconn
    return _dbconn_required