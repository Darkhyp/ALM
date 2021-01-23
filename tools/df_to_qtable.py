# Takes a df and writes it to a qtable provided. df headers become qtable headers
from PyQt5 import QtWidgets


# @staticmethod
def write_df_to_qtable(df, table):
    col_headers = list(map(str, list(df)))
    row_headers = df.index
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(col_headers)
    table.setVerticalHeaderLabels(row_headers)

    # getting data from df is computationally costly so convert it to array first
    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            table.setItem(row, col, QtWidgets.QTableWidgetItem("{0:.6f}".format(df_array[row, col])))

