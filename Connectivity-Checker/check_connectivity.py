import datetime
import sys
import urllib
import psycopg2

from ftplib import FTP
from threading import Thread
from time import sleep
from urllib import request
from urllib.parse import urlparse
from elasticsearch import Elasticsearch
from pymongo import MongoClient


def url_check(url):
    if not url.startswith("https://"):
        url = "https://" + url
    try:
        status_code = urllib.request.urlopen(url).getcode()
    except Exception:
        print(False)
        return
    website_is_up = status_code == 200.
    print(website_is_up)


def ftp_check(ftp_link):
    # 192.168.1.5:21
    # ftp.gnu.org
    try:
        ftp = FTP()
        if ':' in ftp_link:
            url, port = ftp_link.split(":")
            ftp.connect(url, int(port))
        else:
            ftp.connect(ftp_link)
        print(True)
    except Exception:
        print(False)


def check_postgres(uri):
    # hciifixvboxlvz:0341d5fa6a5b36572ab44c6107d42a971f33c9fb2d1a478173a80c88258d2fc2@ec2-54-74-95-84.eu-west-1.compute.amazonaws.com:5432/d6bs5ovruh4v6i
    if not uri.startswith("postgres://"):
        uri = "postgres://" + uri
    result = urlparse(uri)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    try:
        _ = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        print(True)
    except Exception:
        print(False)


def check_mongo(uri):
    # admin:admin@cluster0.avzid.mongodb.net/myFirstDatabase
    if not uri.startswith("mongodb+srv://"):
        uri = "mongodb+srv://" + uri
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=1000)
        client.server_info()
        print(True)
    except Exception:
        print(False)


def check_elastic(uri):
    # elastic:hMpN61lr3zVQBy30fwlByWmO@test-python.es.us-central1.gcp.cloud.es.io:9243
    if not uri.startswith("elastic://"):
        uri = "elastic://" + uri
    result = urlparse(uri)
    username = result.username
    password = result.password
    hostname = result.hostname
    port = result.port
    try:
        _ = Elasticsearch(hostname, sniff_on_start=True, sniff_on_connection_fail=True,
                          sniffer_timeout=5,
                          scheme="https",
                          http_auth=(username, password), port=port)
        print(True)
    except Exception:
        print(False)


def check_case():
    print("Checking connectivity for: " + sys.argv[2])
    if sys.argv[1] == '-url':
        url_check(sys.argv[2])
    elif sys.argv[1] == '-ftp':
        ftp_check(sys.argv[2])
    elif sys.argv[1] == '-mongodb':
        check_mongo(sys.argv[2])
    elif sys.argv[1] == '-postgresql':
        check_postgres(sys.argv[2])
    elif sys.argv[1] == '-elastic':
        check_elastic(sys.argv[2])
    else:
        print("Invalid domain for checking!")
        return


def translate_timeout(timeout):
    if timeout == "1m":
        return 60
    elif timeout == "1h":
        return 3600
    elif timeout == "10s":
        return 10
    elif timeout == "1d":
        return 24 * 3600
    else:
        return 0


def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments!")
        return
    timeout = translate_timeout(sys.argv[3])
    if timeout == 0:
        check_case()
    else:
        while True:
            print()
            print(datetime.datetime.now())
            _ = Thread(check_case())
            sleep(timeout)


if __name__ == '__main__':
    main()
