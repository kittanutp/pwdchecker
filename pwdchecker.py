import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_char)
    res = requests.get(url)
    if res.status_code != 200:
        print(
            f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes_list, hash_to_check):
    for line in hashes_list.text.splitlines():
        hashes = line.split(':')
        if hashes[0] == hash_to_check:  # hashes[0] is tail
            return int(hashes[1])  # hashes[1] is count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        print(f'{password} was found {count} times')

    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
