import unittest
from ChangeDupInSQL import getNeedModifyRow,getRowByID,mysqlConnect
from config import config
import mysql
from mysql.connector import errorcode
import pandas as pd


class MyTestCase(unittest.TestCase):
    def test_conection(self):
        print("---------- Testing Connection ----------")
        try:
            cnx = mysqlConnect(config)
        except mysql.connctor.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.assertIsNotNone(cnx,"test_connection:")
        print("---------- Testing Connection: OK ----------")
    def test_getNeedModifyRow(self):
        # Case of all true
        df1 = pd.DataFrame(data={
            'id': [0, 1, 2], 'bank_request': [1, 1, 1]
        })
        rs1 = [1, 1, 0]
        print("---------- Testing getNeedModifyRow: All True ----------")
        self.assertEqual(getNeedModifyRow([0, 1, 2], df1, 'id', 'bank_request'), rs1, "test_getNeedModifyRow: All true")
        print("---------- Testing getNeedModifyRow: All True : OK ----------")

        # Case of All false
        df2 = pd.DataFrame(data={
            'id': [0, 1, 2], 'bank_request': [0, 0, 0]
        })
        rs2 = [0, 0, 0]
        print("---------- Testing getNeedModifyRow: All False ----------")
        self.assertEqual(getNeedModifyRow([0, 1, 2], df2, 'id', 'bank_request'), rs2, "test_getNeedModifyRow: All False")
        print("---------- Testing getNeedModifyRow: All False : OK ----------")

        # Case of mix
        df3 = pd.DataFrame(data={
            'id': [0, 1, 2, 3], 'bank_request': [1, 0, 1, 0]
        })
        rs3 = [1, 0, 0, 0]
        print("---------- Testing getNeedModifyRow: Mix ----------")
        self.assertEqual(getNeedModifyRow([0, 1, 2, 3], df3, 'id', 'bank_request'), rs3, "test_getNeedModifyRow: Mix")
        print("---------- Testing getNeedModifyRow: Mix : OK ----------")

if __name__ == '__main__':
    unittest.main()
