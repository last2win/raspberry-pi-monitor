
def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.title("time and cpu temperature", fontsize=25)
    plt.xlabel("time", fontsize=15)
    plt.ylabel("cpu temperature", fontsize=15)
    if len(x) > 10:
        plt.plot(x[::len(x)//10], temperature[::len(x)//10])
        plt.gcf().autofmt_xdate()
        plt.savefig('static/temperature.jpg')


if __name__ == '__main__':
    main()
