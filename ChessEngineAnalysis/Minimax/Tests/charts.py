import matplotlib.pyplot as plt
import pandas as pd

def MMvsSF():
    df = pd.read_csv('MMvsSFDepth4.csv', sep=';')
    df_groupby = df.groupby('id').count()
    df1 = pd.DataFrame(df_groupby['is_won'])
    df1.insert(1, 'text', ['Przegrana', 'Remis', 'Wygrana'])
    df1.plot(x='text', y='is_won', kind='bar')
    plt.ylabel("Ilość wygranych pojedynków")
    plt.xticks(rotation=360)
    plt.legend().remove()
    plt.xlabel("")
    plt.title("Wyniki 50 partii")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMvsSF.png', dpi=100)


def SFvsMM():
    df = pd.read_csv('SFvsMMDepth4.csv', sep=';')
    df_groupby = df.groupby('id').count()
    df1 = pd.DataFrame(df_groupby['is_won'])
    df1.insert(1, 'text', ['Przegrana', 'Remis', 'Wygrana'])
    df1.plot(x='text', y='is_won', kind='bar')
    plt.ylabel("Ilość wygranych pojedynków")
    plt.xticks(rotation=360)
    plt.legend().remove()
    plt.xlabel("")
    plt.title("Wyniki 50 partii jako kolor czarny")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('SFvsMM.png', dpi=100)


def MMvsSFLimitedTime():
    df = pd.read_csv('MMvsSFLimitedTime.csv', sep=';')
    df_groupby = df.groupby('id').count()
    df1 = pd.DataFrame(df_groupby['is_won'])
    df1.insert(1, 'text', ['Przegrana', 'Remis', 'Wygrana'])
    df1.plot(x='text', y='is_won', kind='bar')
    plt.legend().remove()
    plt.xlabel("")
    plt.ylabel("Ilość wygranych pojedynków")
    plt.xticks(rotation=360)
    plt.title("Wyniki 50 partii przy ograniczeniu 1 sekundy na ruch")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMvsSFLimitedTime.png', dpi=100)


def MMAverageMoveTime():
    df = pd.read_csv('MMAverageMoveTime.csv', sep=';')
    df_groupby = df.groupby(['depth']).mean()

    df1 = pd.DataFrame(df_groupby['average_time']).reset_index()

    df1.plot(x='depth', y='average_time',linestyle='-', marker='o',)
    plt.legend(["Średni czas wykonywania ruchu"], loc=2)
    plt.xlim(0, 5)
    plt.xlabel("Głębokość")
    plt.ylabel("Średni czas (s)")
    plt.title("Średni czas na ruch w zależności od głębokości obliczeń")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMAverageMoveTime.png', dpi=100)

def MMAverageMoveTimeWithoutABP():
    df = pd.read_csv('MMAverageTimePerDepthNoABP.csv', sep=';')
    df_groupby = df.groupby(['depth']).mean()

    df1 = pd.DataFrame(df_groupby['average_time']).reset_index()

    df1.plot(x='depth', y='average_time',linestyle='-', marker='o',)
    plt.legend(["Średni czas wykonywania ruchu algorytmu Minimax"], loc=2)
    plt.xlabel("Głębokość")
    plt.ylabel("Średni czas (s)")
    plt.title("Średni czas na ruch w zależności od głębokości obliczeń")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMAverageTimePerDepthWithoutABP.png', dpi=100)

def MMAverageTimeTTABP():
    df = pd.read_csv('MMAverageTimeTTABP.csv', sep=';')
    df_groupby = df.groupby(['depth']).mean()

    df2 = pd.read_csv('MMAverageTimePerDepthABP.csv', sep=';')
    df_groupby2 = df2.groupby(['depth']).mean()

    df3 = pd.read_csv('MMAverageTimePerDepthNoABP.csv', sep=';')
    df_groupby3 = df3.groupby(['depth']).mean()

    df1 = pd.DataFrame(df_groupby['average_time']).reset_index()
    df2 = pd.DataFrame(df_groupby2['average_time']).reset_index()
    df3 = pd.DataFrame(df_groupby3['average_time']).reset_index()

    ax1 = df1.plot(x='depth', y='average_time',linestyle='-', marker='o',)
    ax2 = df2.plot(ax = ax1, x='depth', y='average_time',linestyle='-', marker='o',)
    df3.plot = df3.plot(ax = ax2, x='depth', y='average_time',linestyle='-', marker='o',)

    plt.legend(["Średni czas wykonywania ruchu\nz użyciem tabel transpozycji", "Średni czas wykonywania ruchu z przycinaniem gałęzi", "Średni czas wykonywania ruchu"], loc=2, prop={'size': 9})
    plt.xlabel("Głębokość")
    plt.ylabel("Średni czas (s)")
    plt.title("Średni czas na ruch w zależności od\n głębokości obliczeń algorytmu Minimax")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMvsSF.png', dpi=100)
    plt.show()

def MMWithTaperedEvalVsSF():
    df = pd.read_csv('MMWithTaperedEvalvsSF.csv', sep=';')
    df_groupby = df.groupby('id').count()
    df1 = pd.DataFrame(df_groupby['is_won'])
    df1.insert(1, 'text', ['Przegrana', 'Remis', 'Wygrana'])
    df1.plot(x='text', y='is_won', kind='bar')
    plt.ylabel("Ilość wygranych pojedynków")
    plt.xticks(rotation=360)
    plt.legend().remove()
    plt.xlabel("")
    plt.title("Wyniki 50 partii")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMWithTaperedEvalvsSF.png', dpi=100)

def MMWithoutTaperedEvalVsSF():
    df = pd.read_csv('MMWithoutTaperedEvalvsSF.csv', sep=';')
    df_groupby = df.groupby('id').count()
    df1 = pd.DataFrame(df_groupby['is_won'])
    df1.insert(1, 'text', ['Przegrana', 'Remis', 'Wygrana'])
    df1.plot(x='text', y='is_won', kind='bar')
    plt.ylabel("Ilość wygranych pojedynków")
    plt.xticks(rotation=360)
    plt.legend().remove()
    plt.xlabel("")
    plt.title("Wyniki 50 partii")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMWithoutTaperedEvalvsSF.png', dpi=100)

def MMABPvsNoABP():
    df = pd.read_csv('MMAverageTimePerDepthNoABP.csv', sep=';')
    df_groupby = df.groupby(['depth']).mean()

    df2 = pd.read_csv('MMAverageTimePerDepthABP.csv', sep=';')
    df_groupby2 = df2.groupby(['depth']).mean()

    df1 = pd.DataFrame(df_groupby['average_time']).reset_index()
    df2 = pd.DataFrame(df_groupby2['average_time']).reset_index()

    ax = df1.plot(x='depth', y='average_time',linestyle='-', marker='o',)
    df2.plot(ax=ax, x='depth', y='average_time',linestyle='-', marker='o',)

    plt.legend(["Średni czas wykonywania ruchu\n bez przycinania gałęzi", "Średni czas wykonywania ruchu\nz przycinaniem gałęzi"], loc=2, prop={'size': 9})
    plt.xlabel("Głębokość")
    plt.ylabel("Średni czas (s)")
    plt.title("Średni czas na ruch w zależności od\n głębokości obliczeń algorytmu Minimax")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMABPvsNoABP.png', dpi=100)

def NNvsSF():
    df = pd.read_csv('NNvsSF.csv', sep=';')
    df_groupby = df.groupby('id').count()
    df1 = pd.DataFrame(df_groupby['is_won'])
    df1.insert(1, 'text', ['Przegrana', 'Remis', 'Wygrana'])
    df1.plot(x='text', y='is_won', kind='bar')
    plt.ylabel("Ilość wygranych pojedynków")
    plt.xticks(rotation=360)
    plt.legend().remove()
    plt.xlabel("")
    plt.title("Wyniki 50 partii")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('NNvsSF.png', dpi=100)

def MMABPvsSFAll():
    df = pd.read_csv('MMAverageTimeAll.csv', sep=';')
    df_groupby = df.groupby(['depth']).mean()

    df2 = pd.read_csv('MMAverageTimePerDepthABP.csv', sep=';')
    df_groupby2 = df2.groupby(['depth']).mean()

    df1 = pd.DataFrame(df_groupby['average_time']).reset_index()
    df2 = pd.DataFrame(df_groupby2['average_time']).reset_index()

    ax = df1.plot(x='depth', y='average_time',linestyle='-', marker='o',)
    df2.plot(ax=ax, x='depth', y='average_time',linestyle='-', marker='o',)

    plt.legend(["Średni czas wykonywania ruchu\n z przeszukiwaniem spoczynkowym", "Średni czas wykonywania ruchu\nz przycinaniem gałęzi\noraz tabelami transpozycji"], loc=2, prop={'size': 9})
    plt.xlabel("Głębokość")
    plt.ylabel("Średni czas (s)")
    plt.title("Średni czas na ruch w zależności od\n głębokości obliczeń algorytmu Minimax")
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig('MMABPvsNoABP.png', dpi=100)




if __name__ == "__main__":
    MMvsSF()
    # SFvsMM()
    # MMvsSFLimitedTime()
    # MMAverageMoveTime()
    # MMAverageMoveTimeWithoutABP()
    # MMWithTaperedEvalVsSF()
    # MMWithoutTaperedEvalVsSF()
    # MMABPvsNoABP()
    # MMAverageTimeTTABP()
    # MMABPvsSFAll()
    # NNvsSF()
