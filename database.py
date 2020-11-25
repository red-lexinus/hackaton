import pickle
import os


def main():
    # os.system('clear')
    # os.system('cls')

    a = {'1': 1, '2': 2}
    print(a)

    pickle.dump(a, open('a.dat', 'wb'))

    a['1'] = 2
    print(a)

    a = pickle.load(open('a.dat', 'rb'))
    print(a)


if __name__ == '__main__':
    main()

