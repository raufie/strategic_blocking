from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from QtObjects.MainWindow import Ui_MainWindow
from Stylesheets.stylesheets import main_stylesheet
from main_modules.ConfigurationManager import *
from main_modules.NotificationsManager import Notifications
import time
from DataManager import DataManager
# MPL

import numpy
import pyqtgraph as pg
from datetime import datetime, timedelta


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # vip
        self.setupUi(self)
        # self.pushButton.clicked.connect(self.add_stuff)
        # self.done = []
        # self.not_done = []
        self.current_timer = None
        self.tabWidget.setTabEnabled(3, False)

        self.dataManager = DataManager(app_paths.app_data_path)
        # self.pushButton_3.clicked.connect(self.do_task)
        # self.pushButton_2.clicked.connect(self.undo_task)
        self.setStyleSheet(main_stylesheet)

        # MAIN

        # TIME
        self.startTime = time.time()
        self.endTime = time.time()
        # load presets on start (if available...)
        self.load_table_from_presets()
        self.setup_listeners()
        self.accumulated = 0
        # threads
        self.thread = {}
        self.notifications = Notifications()

        # print(self.dataManager.get_data_from_file())
        self.update_plot1()
        self.update_plot2()

# PLOTS

    def get_daily_hours(self, _from=(20, 10, 1990), _to=(20, 12, 2022)):
        # returns minutes
        data = self.dataManager.data
        formatted_data = {}

        for item in data:
            tm = time.localtime(item['timestamp'])
            date = "%02d-%02d-%02d" % (tm.tm_mday, tm.tm_mon, tm.tm_year)
# is in between
            if self.is_date_greater(tm, _from[0], _from[1], _from[2]) and self.is_date_lesser(tm, _to[0], _to[1], _to[2]):

                if date not in formatted_data:
                    formatted_data[date] = 0

                formatted_data[date] += item['time_amount']/3600

        return (formatted_data.keys(), formatted_data.values())

    def update_plot2(self, _from=(10, 10, 1990), _to=(10, 11, 2022)):
        # _from = self.from_daily
        self.map_2_widget.clear()
        # if n is -1 from is from
        _from = (self.from_avg.date().day(),
                 self.from_avg.date().month(), self.from_avg.date().year())
        _to = (self.to_avg.date().day(),
               self.to_avg.date().month(), self.to_avg.date().year())
        try:
            n = int(self.n_days.text())
            if n > 0:
                currTime = time.localtime(time.time())
                currDate = f"{currTime.tm_mon}/{currTime.tm_mday}/{currTime.tm_year}"
                D = datetime.strptime(currDate, "%m/%d/%Y") - timedelta(n)
                dd = D.day
                dm = D.month
                dy = D.year
                _from = _to = (dd,
                               dm, dy)
                _to = (currTime.tm_mday, currTime.tm_mon, currTime.tm_year)

                self.to_avg.setDate(
                    QDate(currTime.tm_year, currTime.tm_mon, currTime.tm_mday+1))
                self.from_avg.setDate(
                    QDate(dy, dm, dd))
        except Exception as E:
            print(E)
        y = self.get_binned_hours(_from=_from, _to=_to)
        x = list(range(len(y)))
        x_str = [
            '12am',
            '1',
            '2',
            '3',
            '4am',
            '5',
            '6',
            '7',
            '8am',
            '9',
            '10',
            '11',
            '12pm',
            '1',
            "2",
            '3',
            '4pm',
            '5',
            '6',
            '7',
            '8pm',
            '9',
            '10',
            '11',
        ]

        self.map_2_widget.setBackground('w')

        # xdict = dict(enumerate(x))
        ticks = [list(zip(range(len(x_str)), x_str))]

        xax = self.map_2_widget.getAxis('bottom')
        xax.setTicks(ticks)

        self.map_2_widget.plot(x, y,
                               pen=pg.mkPen('#7733FF', width=3))
        # PLOT 1...get_binned_hours shit

    def get_interval(self, stamp, amount):
        return time.localtime(stamp+amount/2).tm_hour

    def get_binned_hours(self, _from, _to):
        data = self.dataManager.data
        work_bins = numpy.zeros(24)
        for i in range(24):
            work_bins[i] = 0
        for item in data:
            tm = time.localtime(item['timestamp'])
            if self.is_date_greater(tm, _from[0], _from[1], _from[2]) and self.is_date_lesser(tm, _to[0], _to[1], _to[2]):
                prev = work_bins[self.get_interval(
                    item['timestamp'], item['time_amount'])]

                work_bins[self.get_interval(
                    item['timestamp'], item['time_amount'])] = item['time_amount']+prev
        return work_bins

    def is_date_greater(self, tm, d, m, y):

        ty = tm.tm_year
        td = tm.tm_mday
        tm = tm.tm_mon
        if ty > y:
            return True
        elif ty == y:
            if tm > m:
                return True
            elif tm == m:
                if td >= d:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_date_lesser(self, tm, d, m, y):

        ty = tm.tm_year
        td = tm.tm_mday
        tm = tm.tm_mon
        if ty < y:
            return True
        elif ty == y:
            if tm < m:
                return True
            elif tm == m:
                if td < d:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def update_plot1(self, _from=(10, 10, 1990), _to=(10, 11, 2022)):
        # _from = self.from_daily
        self.map_1_widget.clear()
        _from = (self.from_daily.date().day(),
                 self.from_daily.date().month(), self.from_daily.date().year())
        _to = (self.to_daily.date().day(),
               self.to_daily.date().month(), self.to_daily.date().year())
        x, y = self.get_daily_hours(_from=_from, _to=_to)
        x = list(x)
        y = list(y)
        self.map_1_widget.setBackground('w')

        xdict = dict(enumerate(x))
        ticks = [list(zip(range(len(x)), x))]

        xax = self.map_1_widget.getAxis('bottom')
        xax.setTicks(ticks)

        self.map_1_widget.plot(list(xdict.keys()), y,
                               pen=pg.mkPen('#900C3F', width=3))
        # PLOT 1... daily shit

    def setup_listeners(self):
        self.add_block_btn.clicked.connect(self.add_block)
        self.delete_block_btn.clicked.connect(self.delete_block)
        self.startBtn.clicked.connect(self.initiate_timer)
        self.taskPositiveButton.clicked.connect(self.onTaskPositive)
        self.taskNegativeButton.clicked.connect(self.onTaskNegative)
        self.choose_file_btn.clicked.connect(self.openFileNameDialog)
        self.preset_btn.clicked.connect(self.save_preset)
        self.category_btn.clicked.connect(self.add_category)
        self.play_btn.clicked.connect(
            lambda: self.notifications.play_sound(get_music()))

        # dateChanged
        self.from_daily.dateChanged.connect(lambda: self.update_plot1())
        self.to_daily.dateChanged.connect(lambda: self.update_plot1())
        self.from_avg.dateChanged.connect(lambda: self.update_plot2())
        self.to_avg.dateChanged.connect(lambda: self.update_plot2())
        # n days
        self.n_days.textChanged.connect(lambda: self.update_plot2())

    def load_table_from_presets(self):
        blocks = load_blocks_preset()

        self.preset_label.setText(",".join([str(x) for x in blocks]))
        self.music_path_label.setText(get_music())
        self.categories_list.clear()
        self.categories_list.addItems(get_categories())
        self.categoryCombo.clear()
        self.categoryCombo.addItems(get_categories())
        # DATE EDIT INTI
        self.from_daily.setDate(QDate(2021, 12, 22))
        currTime = time.localtime(time.time())
        self.to_daily.setDate(
            QDate(currTime.tm_year, currTime.tm_mon, currTime.tm_mday))

        self.from_avg.setDate(QDate(2021, 12, 22))
        self.to_avg.setDate(
            QDate(currTime.tm_year, currTime.tm_mon, currTime.tm_mday))

        self.update_plot1()
        self.update_plot2()
        self.n_days.setText("-1")

        for i, block in enumerate(blocks):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(str(block//60))
            )
            self.tableWidget.setItem(
                i, 1, QTableWidgetItem(str(block % 60))
            )
        return blocks

    def add_block(self):
        row_to_add = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_to_add)
        self.tableWidget.setItem(
            row_to_add, 0, QTableWidgetItem(str(0))
        )
        self.tableWidget.setItem(
            row_to_add, 1, QTableWidgetItem(str(0))
        )

    def delete_block(self):
        rowToDelete = self.tableWidget.currentRow()
        if rowToDelete != -1:
            self.tableWidget.removeRow(rowToDelete)

        self.tableWidget.selectRow(-1)

    def add_category(self):
        if self.category_label.text().strip() != "":
            add_categories(self.category_label.text())
            self.categories_list.clear()
            self.categories_list.addItems(get_categories())

    def openFileNameDialog(self):

        dialog = QFileDialog()
        dialog.setNameFilter("Audio Files (*.mp3)")

        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            print(fileNames)
            self.music_path_label.setText(fileNames[0])
            save_music(fileNames[0])

    def save_preset(self):
        try:
            preset = [int(x) for x in self.preset_label.text().split(",")]
            save_preset(preset)
        except:
            self.show_error("PLEASE USE THE CORRECT SYNTAX ... e.g 5,25,35")

    def initiate_timer(self):
        blocks = self.get_blocks_from_table()
        if blocks == None:
            return
        isValidated = self.validate_form()

        if isValidated:
            self.accumulated = 0
            self.startTime = time.time()
            self.update_timer(0)
            self.tabWidget.setTabEnabled(3, True)
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setCurrentIndex(4)
            # SET DATE

            # set current timer
            self.current_timer = {
                "blocks": blocks,
                "title": self.title,
                "category": self.cat,
                "current": 1
            }
            self.set_task_status(0)

    def set_task_status(self, status):
        self.taskStatus = status
        if status == 0:
            self.taskNegativeButton.setText("End Session")
            self.taskPositiveButton.setText("Start Block")
            self.timer_task_label.setText(self.current_timer['title'])
            self.timer_category_label.setText(self.current_timer['category'])
            self.current_block_label.setText(
                str(f"{self.current_timer['current']}/{len(self.current_timer['blocks'])}"))
            formattedTime = self.current_timer['blocks'][self.current_timer['current']-1]
            formattedTime = get_formatted(formattedTime)
            self.block_time_label.setText(formattedTime)
            self.accumulated_label.setText(
                get_formatted_seconds(self.accumulated))

        elif status == 1:
            self.taskNegativeButton.setText("Cancel Block")
            self.taskPositiveButton.setText("Finish Block Early")
            self.accumulated_label.setText(
                get_formatted_seconds(self.accumulated))
        elif status == 2:
            # END>>>> CONFETTI>>> CELEBRATION>>>all that jazz
            print("ALL TASKS FINISHED")
            self.taskNegativeButton.setText("Task Finished")
            self.taskPositiveButton.setText("Main Menu")
            pass

    def onTaskPositive(self):
        if self.taskStatus == 0:
            # end task, ... save progress... move back to menu
            # START TIMER>>>>
            if self.current_timer['current'] <= len(self.current_timer['blocks']):
                self.startTime = time.time()
                self.startCounterWorker()
                self.set_task_status(1)
            else:
                self.set_task_status(2)

                # END THE TIMER>>>>
        elif self.taskStatus == 1:
            #
            # ADD PROGRESS< ADD BLOCK NUMBER, RESET TIMER
            print("Trying to stop thread...")
            self.stopCounterWorker()
            deltaTime = time.time() - self.startTime
            self.accumulated += deltaTime
            self.startTime = time.time()
            self.update_timer(0)
            self.current_timer['current'] += 1
            # SAVING TIME LOCALLY
            self.dataManager.add_data({
                "timestamp": time.time(),
                "time_amount": deltaTime,
                "category": self.current_timer["category"]
            })
            self.dataManager.save()

            if self.current_timer['current'] > len(self.current_timer['blocks']):
                self.set_task_status(2)
            else:
                self.set_task_status(0)
        elif self.taskStatus == 2:
            self.accumulated = 0

            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, True)
            self.tabWidget.setCurrentIndex(0)

    def onTaskNegative(self):
        if self.taskStatus == 0:
            # end task, ... save progress... move back to menu
            self.accumulated = 0

            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, True)
            self.tabWidget.setCurrentIndex(0)

        elif self.taskStatus == 1:
            #
            # cancel task progress... don't add the block number

            self.stopCounterWorker()
            self.startTime = time.time()
            self.update_timer(0)
            self.set_task_status(0)

        elif self.taskStatus == 2:
            self.accumulated = 0

            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, True)
            self.tabWidget.setCurrentIndex(0)

    def get_blocks_from_table(self):
        blocks = []
        for i in range(self.tableWidget.rowCount()):
            try:
                h = self.tableWidget.item(i, 0).text()
                h = int(h)
                m = self.tableWidget.item(i, 1).text()
                m = int(m)
                blocks.append(h*60 + m)

            except:
                self.show_error(
                    "Please make sure that only numbers are filled into the table")
                return None
        return blocks

    def validate_form(self):
        # make sure title is there
        title = self.titleInput.text()
        cat = self.categoryCombo.currentText()
        if title.strip() == "" or cat.strip() == "":
            self.show_error(
                "Please make sure that title and category are filled")
        # make sure category is there
        # make sure time is there...
            return False
        else:
            self.title = title
            self.cat = cat
            return True

    def show_error(self, text):
        dlg = QDialog()
        dlg.resize(500, 50)
        l1 = QLabel(text, dlg)

        dlg.setWindowModality(Qt.ApplicationModal)

        dlg.setWindowTitle("ERROR")
        dlg.exec_()

# CONUTER THREADS
    def startCounterWorker(self):
        self.thread[0] = ThreadClass(parent=None, index=0)
        self.thread[0].start()
        self.thread[0].any_signal.connect(self.update_timer)
        pass

    def stopCounterWorker(self):
        self.thread[0].stop()
        # self.

    def update_timer(self, i):
        # print("COUNTING = " + str(i))
        t_s = (time.time()-self.startTime)  # minutes
        t_m = t_s//60
        t_h = t_m//60
        self.hours_label.display(int(t_h))
        self.minutes_label.display(int(t_m))
        self.seconds_label.display(int(t_s % 60))
        # print()
        if self.current_timer != None:
            blocks = self.current_timer['blocks']
            block = blocks[self.current_timer['current']-1]
            block *= 60
            print(f"dt={t_s%60}")
            print(f"block={block}")
            if (t_s >= float(block)):
                # self.stopCounterWorker()
                print("TRYING TO STOP THREAD")
                self.onTaskPositive()
                self.notifications.show_notification(t_s)
# STATS
    # def update_graphs(self):


class ThreadClass(QThread):
    any_signal = pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        print("STARTING THREAD")
        i = 1
        while True:
            time.sleep(1)
            self.any_signal.emit(i)

    def stop(self):
        self.is_running = False
        print("stopping thread")
        self.terminate()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
