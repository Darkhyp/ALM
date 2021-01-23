from PyQt5 import QtCore, QtGui, QtWidgets, uic

class parameter_Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None,ALM=None):
        super(parameter_Dialog, self).__init__(parent)

        self.ALM = ALM

        uic.loadUi('dialog_window.ui', self)
        self.setWindowTitle("Input parameters")

        self.load_parameters()

        # connect the two functions
        self.cancelButton.clicked.connect(self.cancel)
        self.defaultButton.clicked.connect(self.default)
        self.validateButton.clicked.connect(self.validate)

    def load_parameters(self):
        if self.ALM is not None:
            self.textEdit_insured_number.setText(str(self.ALM.insured_number))
            self.textEdit_insured_premium.setText(str(self.ALM.insured_premium))
            self.textEdit_average_age.setText(str(self.ALM.average_age))
            self.textEdit_contracts_maturity.setText(str(self.ALM.contracts_maturity))

            self.textEdit_charges_rate.setText(str(self.ALM.charges_rate))
            self.textEdit_fee_pct_premium.setText(str(self.ALM.fee_pct_premium))
            self.textEdit_fixed_fee.setText(str(self.ALM.fixed_fee))
            self.textEdit_fixed_cost_inflation.setText(str(self.ALM.fixed_cost_inflation))
            self.textEdit_redemption_rates.setText(str(self.ALM.redemption_rates))

    def default(self):
        self.ALM.set_default()
        self.load_parameters()


    def validate(self):
        if self.ALM is not None:
            self.ALM.insured_number = int(self.textEdit_insured_number.toPlainText())
            self.ALM.insured_premium = int(self.textEdit_insured_premium.toPlainText())
            self.ALM.average_age = int(self.textEdit_average_age.toPlainText())
            self.ALM.contracts_maturity = int(self.textEdit_contracts_maturity.toPlainText())

            self.ALM.charges_rate = float(self.textEdit_charges_rate.toPlainText())
            self.ALM.fee_pct_premium = float(self.textEdit_fee_pct_premium.toPlainText())
            self.ALM.fixed_fee = float(self.textEdit_fixed_fee.toPlainText())
            self.ALM.fixed_cost_inflation = float(self.textEdit_fixed_cost_inflation.toPlainText())
            self.ALM.redemption_rates = float(self.textEdit_redemption_rates.toPlainText())

        self.close()

    def cancel(self):
        self.close()