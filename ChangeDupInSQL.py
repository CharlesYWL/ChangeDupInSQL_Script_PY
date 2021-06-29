
import mysql.connector
from mysql.connector import errorcode
import pandas
from collections import defaultdict
from config import config
import json
import logging

# Logging setting
root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(asctime)s; %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")) # or whatever
root_logger.addHandler(handler)


# return row(list) that id matches.
# df: Dataframe, id: value if "id"
def getRowByID(df,id):
    return df.loc[df[0] == id].iloc[0]


# pass ids: list of id, df: dataFrame, pos: search column(which is column is bank_request)
# get bank_request of all ids, we only keep 1, return list that need to be changed or not
# the return value is list of id that NEED TO BE CHANGED
def getNeedModifyRow(ids,df, query_column,value_column):
    bank_requests = [df.loc[df[query_column] == id].iloc[0][value_column] for id in ids]
    bank_requests_need_to_change = [0 for _ in range(len(ids))]

    # now we have id:bank_request
    # check sum(bank_requests) == 1
    # True: good, return []
    # False: bad, modfiy them to only 1 true bank_request
    sum_of_one = sum(bank_requests)

    if sum_of_one > 1:
        for (idx, val) in enumerate(bank_requests):
            if val == 1 and sum_of_one > 1:
                bank_requests_need_to_change[idx] = 1
                sum_of_one -= 1
    elif sum_of_one == 0:  # sum_of_one = 0
        bank_requests_need_to_change[-1] = 1

    return bank_requests_need_to_change


def modifyDB(cnx,cursor, id, target_value):
    # print(f"We change id:{id} to target_value:{target_value}")
    query = "UPDATE t_problem SET bank_request = " + str(target_value) + " WHERE id = " + str(id) + ";"
    # print(query)
    logging.info(query)
    cursor.execute(query)
    cnx.commit()


def saveDictToJson(dic, file_name):
    with open(file_name, "w") as outfile:
        json.dump(dic, outfile)


def mysqlConnect(config):
    return mysql.connector.connect(**config)

if __name__ == '__main__':
    # identity_col is the col we used for identify duplication
    # target_col is the col we gonna make change
    identity_col = 0
    target_col = 37
    try:
        cnx = mysqlConnect(config)
        # cnx = mysql.connector.connect(user='mobile', password='M0bil3',host='beacondev.coverq.com',database='thinkmobile')
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            logging.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            logging.error("Database does not exist")
        else:
            print(err)
            logging.error(err)
    else:
        print("connection success");
        logging.debug("connection success")
        # query here
        query = "SELECT * FROM t_problem AS A WHERE (title IN (SELECT title FROM t_problem AS B WHERE A.id<>B.id)) AND " \
                "create_by = 10384 "
        cursor.execute(query)
        query_df = pandas.DataFrame(cursor) # save to dataframe
        # print(query_df)
        # dict: sort duplicated problems together
        # dict {title:[id1,id2,id3],title2:[id4,id5}
        dup_map = defaultdict(lambda :[])
        for index, row in query_df.iterrows():
            id = row[0]
            title = row[1]
            create_by = row[30]
            dup_map[title+str(create_by)].append(id)
        saveDictToJson(dup_map, "dup_map.json")

        # now we export them to csv
        csv_df = pandas.DataFrame(columns=['id','title','create_by','bank_request','bank_request_changed'])

        for dup_title, ids in dup_map.items():
            '''
            we have groups of dup [id1,id2,id3], we only keep "bank_request=1" 1 of them
            '''
            bank_requests_need_to_change = getNeedModifyRow(ids, query_df, identity_col, target_col);
            for (idx , id) in enumerate(ids):
                select_row = getRowByID(query_df, id)
                csv_df = csv_df.append({'id': id, 'title':select_row[1], 'create_by':select_row[30], 'bank_request': select_row[target_col], 'bank_request_changed':bank_requests_need_to_change[idx] }, ignore_index=True)

            # Modify DB here
            for id in [x for i, x in enumerate(ids) if bank_requests_need_to_change[i]]:
                # Chance 0 -> 1 and 1-> 0
                modifyDB(cnx,cursor, id, [1, 0][getRowByID(query_df, id)[target_col]])

        csv_df.to_csv('DupProblems.csv', sep=',', encoding='utf-8')


        cursor.close()
        cnx.close()
        logging.info("Python End")
