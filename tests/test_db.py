from unittest.mock import patch

from sqlalchemy.pool import QueuePool

from src.db.session import get_engine, db_session


class TestSession:
    def test_get_engine(self):
        with patch('src.db.session.create_engine') as create_engine:
            get_engine('uri_db')
            assert all([create_engine.called,
                        list(create_engine.call_args_list[0]) == [('uri_db',),
                                                                  {'convert_unicode': True,
                                                                   'pool_size': 20,
                                                                   'poolclass': QueuePool}]])

    def test_db_session(self):
        with patch('src.db.session.get_engine') as get_engine:
            with patch('src.db.session.Base') as Base:
                with patch('src.db.session.sessionmaker') as sessionmaker:
                    with patch('src.db.session.scoped_session') as scoped_session:
                        with db_session(create_tables=True) as session:
                            pass
                        assert all([get_engine.called,
                                    get_engine.return_value.connect.called,
                                    Base.metadata.create_all.called,
                                    sessionmaker.called,
                                    list(sessionmaker.call_args_list[0]) ==[(), {'autocommit': False, 'autoflush': True, 'bind': get_engine.return_value}],
                                    scoped_session.called,
                                    scoped_session.return_value.close.called,
                                    get_engine.return_value.connect.return_value.close.called
                                    ])
