import sys
import urllib
from urllib import request
from urllib import error


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


def main():
    if sys.argv[1] == '-url':
        url_check(sys.argv[2])
    elif sys.argv[1] == '-ftp':
        print("ftp")
    elif sys.argv[1] == '-mongodb':
        print("mongodb")
    elif sys.argv[1] == '-postgresql':
        print("postgres")
    elif sys.argv[1] == '-elastic':
        print("elastic")
    else:
        print("Invalid domain for checking!")
        return


if __name__ == '__main__':
    main()
