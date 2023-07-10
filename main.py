import PySimpleGUI as Sg


class GUI:
    def __init__(self):
        self.theme = 'DarkRed'
        self.font = 'Calibri'
        self.result = 0
        self.laps = 0
        self.layout = [
            [Sg.Text('Длительность гонки', font=self.font), Sg.Input(key='-RACE-', size=(10, 0))],
            [Sg.Text('Среднее время круга', font=self.font),
             Sg.Input(key='-MINLAP-', size=(3, 0), expand_x=True),
             Sg.Input(key='-SECLAP-', size=(3, 0), expand_x=True)],
            [Sg.Text('Расход топлива', font=self.font),
             Sg.Input(key='-FUEL-', size=(10, 0), expand_x=True)],
            [Sg.Text(f'Рекомендуется 0 литров', key='-FPR-', font=self.font, justification='center', expand_x=True)],
            [Sg.Text(f'Кол-во кругов 0', key='-LAPS-', font=self.font, justification='center', expand_x=True)],
            [Sg.Button('РАСЧЕТ', key='-RESULT-', font=self.font)]
        ]
        Sg.theme(self.theme)
        self.window = Sg.Window('Калькулятор топлива ACC', self.layout, self.theme)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == Sg.WIN_CLOSED:
                break
            if event == '-RESULT-':
                if self.validate_input(values):
                    self.result = self.fuel_per_race(values['-RACE-'], values['-MINLAP-'], values['-SECLAP-'],
                                                     values['-FUEL-'])
                    self.window['-FPR-'].update(
                        f'Рекомендуется {round(self.result, 2)} литров \n+ 10 литров на прогревочный \nкруг')
                    self.laps = self.all_laps(values['-RACE-'], values['-MINLAP-'], values['-SECLAP-'])
                    self.window['-LAPS-'].update(f'Кол-во кругов {round(self.laps, 1)}')
                else:
                    layout_ok = [[Sg.Text('Проверьте значения')],
                                 [Sg.Button('OK', expand_x=True)]]
                    ok_window = Sg.Window('Error', layout_ok)
                    ok_event, ok_values = ok_window.read()
                    while True:
                        if ok_event == 'OK':
                            break
                    ok_window.close()

    @staticmethod
    def validate_input(values):
        try:
            int(values['-RACE-'])
            int(values['-MINLAP-'])
            int(values['-SECLAP-'])
            float(values['-FUEL-'])
            return True
        except ValueError:
            return False

    @staticmethod
    def convert_time(race_time, lap_time_min, lap_time_sec):
        race_time = float(race_time) / 60
        lap_time = ((float(lap_time_sec) + (float(lap_time_min) * 60)) / 60) / 60
        return race_time, lap_time

    def fuel_per_race(self, race_time, lap_time_min, lap_time_sec, fuel_per_lap):
        race_time, lap_time = self.convert_time(race_time, lap_time_min, lap_time_sec)
        result = (race_time / lap_time) * float(fuel_per_lap)
        return result

    def all_laps(self, race_time, lap_time_min, lap_time_sec):
        race_time, lap_time = self.convert_time(race_time, lap_time_min, lap_time_sec)
        result = race_time / lap_time
        return result


if __name__ == '__main__':
    app = GUI()
    app.run()
