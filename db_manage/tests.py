from django.test import TestCase

# Create your tests here.


class Test_DB_Manage(TestCase):
    def setUp(self):
        print("测试 获取数据库信息相关配置")

    def test_conf_info(self):
        from libs.config import Config
        conf = Config()
        db_type_list = conf.items('db_type')
        mysql_version_list = conf.items('mysql_version')
        oracle_version = conf.items('oracle_version')
        print(db_type_list)
        print(mysql_version_list)
        print(oracle_version)
        self.assertEqual(len(db_type_list)>0,True)
        self.assertEqual(len(mysql_version_list)>0,True)
        self.assertEqual(len(oracle_version)>0,True)

    def tearDown(self):
        print('测试完成')

