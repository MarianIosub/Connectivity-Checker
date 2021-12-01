import sys
import urllib
from urllib import request
from urllib import error

import psycopg2
from urllib.parse import urlparse


def url_check(url):
    if url[0:3] == "www":
        url = "https://" + url
    try:
        status_code = urllib.request.urlopen(url).getcode()
    except urllib.error.HTTPError:
        print("False")
        return
    except urllib.error.URLError:
        print(False)
        return
    website_is_up = status_code == 200.
    print(website_is_up)


def ftp_check(ftp_link):
    pass


def check_postgres(uri):
    # postgres: // mdtdoxetgisriv: e980d8c00263e2fb362485c68e4933987f3df27c8daeaabfd3dc2b167984dcd7 @ ec2 - 176 - 34 - 105 - 15.eu - west - 1.compute.amazonaws.com: 5432 / d1qujjivcif155
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
        print("True")
    except Exception as e:
        print("False: " + str(e))


def main():
    if len(sys.argv) != 3:
        print("Invalid number of arguments!")
        return
    if sys.argv[1] == '-url':
        url_check(sys.argv[2])
    elif sys.argv[1] == '-ftp':
        ftp_check(sys.argv[2])
    elif sys.argv[1] == '-mongodb':
        print("mongodb")
    elif sys.argv[1] == '-postgresql':
        check_postgres(sys.argv[2])
    elif sys.argv[1] == '-elastic':
        print("elastic")
    else:
        print("Invalid domain for checking!")
        return


if __name__ == '__main__':
    main()
