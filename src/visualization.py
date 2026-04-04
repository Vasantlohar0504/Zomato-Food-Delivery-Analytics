import matplotlib.pyplot as plt

def plot_bar(data, title):
    plt.figure()
    data.plot(kind='bar')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_scatter(df):
    plt.figure()
    plt.scatter(df['cost'], df['rate'])
    plt.title("Cost vs Rating")
    plt.xlabel("Cost")
    plt.ylabel("Rating")
    plt.show()