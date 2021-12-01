import sys


def main():
    if sys.argv[1] == '-url':
        print("url")
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
