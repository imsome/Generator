import psycopg2
import config
import api_requests
from config import ReportHandler


class DBConnector:

    __connection = False

    def __init__(self):
        ReportHandler.add_log("Connect to DB", "Starting")
        self.login = "board"
        self.password = "board"
        self.url = config.db_url
        self.host = "192.168.2.3"
        self.__cursor = ""
        try:
            self.__connection = psycopg2.connect(dbname=self.url, user=self.login, password=self.password, host=self.host)
            ReportHandler.add_log("Connect to DB", "Connection established")
            self.__cursor = self.__connection.cursor()
        except psycopg2.OperationalError:
            ReportHandler.add_error("Wrong DB setted up")
        except:
            ReportHandler.add_error("Connect to DB", "Failed")

    def approve_adds_with_status_2(self):
        ReportHandler.add_log("Approving ads with DB", "Starting")
        try:
            with self.__connection:
                self.__cursor.execute(api_requests.query_set_status_confirmed)
            ReportHandler.add_log("Approving ads with DB", "Finished successfully")
        except:
            ReportHandler.add_error("Approving ads with DB", "Failed")

    def get_min_and_max_ad_id(self):
        try:
            with self.__connection:
                self.__cursor.execute(api_requests.query_get_ads_min_and_max)
                result = self.__cursor.fetchone()
                config.min_ad_id = result[0]
                config.max_ad_id = result[1]
                print(config.max_ad_id)
        except:
            ReportHandler.add_error("Getting min and max ad ids", "Failed")

    def get_filter_groups(self):
        try:
            with self.__connection:
                self.__cursor.execute("SELECT * FROM filter_groups")
                to_parse = self.__cursor.fetchall()
                return to_parse
        except:
            return None

    def get_filters(self):
        try:
            with self.__connection:
                self.__cursor.execute("SELECT * FROM filters")
                to_parse = self.__cursor.fetchall()
                return to_parse
        except:
            ReportHandler.add_error("Getting filters", "Failed")


# config.db_url = "ip-2441.board"
# connect = DBConnector()
# connect.approve_adds_with_status_2()
# connect.get_min_and_max_ad_id()
# connect.get_parsed_filters()
# connect.get_1st_lvl_filters()
