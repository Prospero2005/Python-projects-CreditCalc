import sys
import math
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

class ExampleApp(QMainWindow):

    def __init__(self, cli):
        super(ExampleApp, self).__init__()
        uic.loadUi('form.ui', self)
        self.btn_exit.clicked.connect(self.app_close)
        self.annuity.toggled.connect(self.type_check)
        self.classic.toggled.connect(self.type_check)
        self.slider_period.valueChanged.connect(self.change_period)
        self.slider_percent.valueChanged.connect(self.change_percent)
        self.slider_sum.valueChanged.connect(self.change_sum)
        self.slider_payment.valueChanged.connect(self.change_payment)
        self.ann_payment.toggled.connect(self.check_ann_type)
        self.ann_period.toggled.connect(self.check_ann_type)
        self.ann_sum.toggled.connect(self.check_ann_type)
        self.btn_calculate.clicked.connect(self.calculate)
        self.rb_ann_active = None
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Результат расчета")
        self.prepare()

    def calculate(self):
        type_ = self.classic if self.classic.isChecked() else self.annuity
        txt = f"Тип кредита: {type_.text()}.\n"
        percent_ = float(self.line_percent.text())
        period_ = self.progress_period.value()
        sum_ = self.progress_sum.value()
        payment_ = self.progress_payment.value()
        i = percent_ / 12 / 100
        if type_ == self.classic:
            total_ = 0
            for curr_period in range(1, period_ + 1):
                payment_ = (sum_ / period_) + i * (sum_ - (sum_ * (curr_period - 1) / period_))
                total_ += math.ceil(payment_)
            overpayment = total_ - sum_
            txt += f"Cтавка {percent_}% в год, период {period_} месяцев, сумма кредита {sum_} грн.\n"
            txt += f"Общая сумма выплаты: {total_} грн. Переплата = {overpayment} грн."
        else:
            if self.rb_ann_active == self.ann_payment:
                annuitet = math.ceil(sum_ * (i * pow(1 + i, period_)) / (pow(1 + i, period_) - 1))
                overpayment = (annuitet * period_) - sum_
                txt += f"Cтавка {percent_}% в год, период {period_} месяцев, сумма кредита {sum_} грн.\n"
                txt += f"Ваш платеж: {annuitet} грн. в месяц. Переплата = {overpayment} грн."
            elif self.rb_ann_active == self.ann_sum:
                sum_ = int(payment_ / (i * (pow(1 + i, period_) / (pow(1 + i, period_) - 1))))
                overpayment = (payment_ * period_) - sum_
                txt += f"Cтавка {percent_}% в год, период {period_} месяцев, платеж {payment_} грн.\n"
                txt += f"Доступная сумма кредита: {sum_} грн. Переплата = {overpayment} грн."
            elif self.rb_ann_active == self.ann_period:
                period_ = math.ceil(math.log((payment_ / (payment_ - i * sum_)), 1 + i))
                overpayment = payment_ * period_ - sum_
                txt += f"Cтавка {percent_}% в год, сумма кредита {sum_} грн., платеж {payment_} грн.\n"
                txt += f"Для погашения кредита потребуется {period_} месяцев. Переплата = {overpayment} грн."
        self.msg.setText(txt)
        self.msg.exec()

    def change_period(self):
        self.progress_period.setValue(self.slider_period.value())
        self.line_period.setText(str(self.progress_period.value()))

    def change_percent(self):
        p = self.slider_percent.value()
        self.progress_percent.setValue(p)
        self.line_percent.setText(str(float(p / 10)))

    def change_sum(self):
        self.progress_sum.setValue(self.slider_sum.value())
        self.line_sum.setText(str(self.progress_sum.value()))

    def change_payment(self):
        self.progress_payment.setValue(self.slider_payment.value())
        self.line_payment.setText(str(self.progress_payment.value()))

    def set_param(self, *args):
        self.period.setEnabled(args[0])
        self.line_period.setEnabled(args[0])
        self.progress_period.setEnabled(args[0])
        self.percent.setEnabled(args[1])
        self.line_percent.setEnabled(args[1])
        self.progress_percent.setEnabled(args[1])
        self.sum.setEnabled(args[2])
        self.line_sum.setEnabled(args[2])
        self.progress_sum.setEnabled(args[2])
        self.payment.setEnabled(args[3])
        self.line_payment.setEnabled(args[3])
        self.progress_payment.setEnabled(args[3])

    def check_ann_type(self):
        rb = self.sender()
        if rb.isChecked():
            self.rb_ann_active = rb
            if rb.objectName() == 'ann_payment':
                self.set_param(True, True, True, False)
            elif rb.objectName() == 'ann_sum':
                self.set_param(True, True, False, True)
            else:
                self.set_param(False, True, True, True)

    def annuity_enable(self, state):
        self.ann_payment.setEnabled(state)
        self.ann_period.setEnabled(state)
        self.ann_sum.setEnabled(state)

    def type_check(self):
        rb = self.sender()
        if rb.isChecked():
            if rb.objectName() == 'classic':
                if self.rb_ann_active:
                    self.rb_ann_active.setAutoExclusive(False)
                    self.rb_ann_active.setChecked(False)
                    self.rb_ann_active.setAutoExclusive(True)

                self.annuity_enable(False)
                self.set_param(True, True, True, False)
            else:
                self.annuity_enable(True)

    def app_close(self):
        sys.exit(0)

    def prepare(self):
        self.line_period.setText(str(self.progress_period.value()))
        self.line_sum.setText(str(self.progress_sum.value()))
        self.line_percent.setText(str(float(self.progress_percent.value() / 10)))
        self.line_payment.setText(str(self.progress_payment.value()))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp(False)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
