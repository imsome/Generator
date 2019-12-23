# coding=utf-8

import config
import datetime


class Report:
    def __init__(self, error_path, response_path):
        self.log_errors = {}
        self.log_response = {}

    def add_error(self, function, error_text):
        key = datetime.datetime.now().strftime("%H:%M:%S.%f")
        if key in self.log_errors.keys():
            key = key + "0"
            while key in self.log_errors.keys():
                elem = int(key[-1])
                elem += 1
                key = str(key[:-1]) + str(elem)
        self.log_errors[key] = function + ": " + error_text
        self.print_error_while_working(key, function + ": " + error_text)

    def print_errors(self):
        with open(config.report_errors_path, 'w') as file_writer:
            for key, val in self.log_errors.items():
                file_writer.write('{0} - {1}\n'.format(key, val.encode('utf-8')))

    def add_log(self, function, log_text):
        var_text = self.parse_log(function, log_text)
        if var_text:
            log_text = var_text
        key = datetime.datetime.now().strftime("%H:%M:%S.%f")
        if str(key) in str(self.log_response.keys()):
            key = key + "0"
            while key in self.log_response.keys():
                elem = int(key[-1])
                elem += 1
                key = key[:-1] + str(elem)

        self.log_response[key] = function + ": " + str(log_text)
        self.print_log_while_working(key, function + ": " + str(log_text))

    def print_logs(self):
        with open (config.report_logs_path, 'w') as file_writer:
            for key, val in self.log_response.items():
                file_writer.write('{0} - {1}\n'.format(key, val))

    def print_log_while_working(self, key, val):
        with open(config.report_logs_path, 'a') as file_writer:
            try:
                if config.is_dump_logs_in_console:
                    print('{0} - {1}\n'.format(key, val))
                file_writer.write('{0} - {1}\n'.format(key, val))
            except UnicodeEncodeError:
                if config.is_dump_logs_in_console:
                    print(file_writer.write('{0} - {1}\n'.format(key, val.encode('utf-8'))))
                file_writer.write('{0} - {1}\n'.format(key, val.encode('utf-8')))

# TODO: проблема в енкодинге в utf-8, символы теряются. Над научиться работать с Польским как-то
    def print_error_while_working(self, key, val):
        with open(config.report_errors_path, 'a') as file_writer:
            try:
                if config.is_dump_logs_in_console:
                    print("ERROR:\n")
                    print(('{0} - {1}\n'.format(key, val)))
                file_writer.write('{0} - {1}\n'.format(key, val))
            except UnicodeEncodeError:
                if config.is_dump_logs_in_console:
                    print("ERROR:\n")
                    print('{0} - {1}\n'.format(key, val.encode('utf-8')))
                file_writer.write('{0} - {1}\n'.format(key, val.encode('utf-8')))

    def parse_log(self, function, response):
        if type(response) == dict:
            data = response.get("data")
            if str(function) in ("Registration", "Authorization"):
                id = data[0].get('id')
                email = data[0].get('email')
                token = data[0].get('token')
                return "id: " + str(id) + ", email: " + email + ", token: " + str(token)
            elif str(function) in "Creating add":
                id = data[0].get('id')
                name = data[0].get('name')
                description = data[0].get('description')
                return "id: " + str(id) + ", name: ", str(name), ", description: " + str(description)
            else:
                return False

    def report_it(self, function, response):
        if response.get('success'):
            self.add_log(function, response)
        else:
            self.add_log(function, "Failed")
            self.add_error(function, str(response))

    def response_token(self, function, data):
        if type(data) == dict:
            if not data.get('success'):
                if function:
                    self.add_log(function, "Failed to get right response\n__________________________")
                    self.add_error(function, "Could not get response:\n{0}".format(data))
                else:
                    self.add_log("Response", "Failed to get right response\n________________________")
                    self.add_error("Response", "Could not get response:\n{0}".format(data))
            else:
                if function:
                    self.add_log(function, data)
                else:
                    self.add_log("Response", data)
        else:
            self.add_error("Response", data)
            self.add_log("Response", "Failed")
