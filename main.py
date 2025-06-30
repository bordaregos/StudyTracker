import csv
import time
from datetime import datetime


class StudySession:
    """Данные сессии и методы работы с ними."""
    def __init__(self):
        now = datetime.now()
        self.start_date = now.strftime('%d.%m.%y')
        self.start_time = now.strftime('%H:%M:%S')
        self.start_timestamp = time.time()
        self.pauses = []
        self.end_timestamp = None
        self.is_paused = False

    # Добавление паузы.
    def add_pause(self):
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def pause(self):
        self.pauses.append({
            'start': time.time(),
            'duration': 0
        })
        self.is_paused = True
        print('Session is paused')

    # Возобновление трекинга.
    def resume(self):
        if not self.pauses:
            return

        # Добавляем данные о паузе в словарь по ключу. В списке pauses у нас словарь если что!
        pause_duration = time.time() - self.pauses[-1]['start']
        self.pauses[-1]['duration'] += pause_duration
        self.is_paused = False
        print(f'Pause is finished. Pause time: {pause_duration:.0f} sec')

    # Подсчёт итоговых данных сессии.
    def calculate_stats(self):
        total_duration = self.end_timestamp - self.start_timestamp
        pause_duration = sum([p['duration'] for p in self.pauses])
        actual_study_time = total_duration - pause_duration

        return {
            'Дата': self.start_date,
            'Время': self.start_time,
            'Пр-ть': f"{total_duration // 60:.0f} min {total_duration % 60:.0f} sec",
            'Кол-во пауз': len(self.pauses),
            'Общ. вр. пауз': f"{pause_duration // 60:.0f} min {pause_duration % 60:.0f} sec",
            'Чистое вр. учёбы': f"{actual_study_time // 60:.0f} min {actual_study_time % 60:.0f} sec"
        }


class StudyTracker:
    """Логика трекера."""
    CSV_HEADERS = ['Дата', 'Время', 'Пр-ть', 'Кол-во пауз',
                   'Общ. вр. пауз', 'Чистое вр. учёбы']

    def __init__(self):
        self.sessions = []
        self.current_session = None

    def start_session(self):
        self.current_session = StudySession()
        print(f"\nSession started at: {self.current_session.start_date} "
              f"in {self.current_session.start_time}")

    def toggle_pause(self):
        if not self.current_session:
            print('No active sesion')
            return
        self.current_session.add_pause()

    def end_session(self):
        if not self.current_session:
            print('No active session')
            return

        self.current_session.end_timestamp = time.time()
        session_data = self.current_session.calculate_stats()

        self._print_session_stats(session_data)
        self._save_to_csv(session_data)
        self.current_session = None

    def _print_session_stats(self, stats):
        print('\n--- Session Stats ---')
        for key, value in stats.items():
            print(f"{key}: {value}")

    def _save_to_csv(self, session_data):
        with open('data_tracker.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.CSV_HEADERS,
                                    delimiter=';', quoting=csv.QUOTE_MINIMAL)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(session_data)

    def run(self):
        while True:
            print("\n=== Трекер учёбы ===")
            print("1. Начать сессию")
            print("2. Пауза/продолжить")
            print("3. Завершить сессию")
            print("0. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.start_session()
            elif choice == '2':
                self.toggle_pause()
            elif choice == '3':
                self.end_session()
            elif choice == '0':
                print("Программа завершена.")
                break
            else:
                print("Ошибка: введите число от 0 до 3")


if __name__ == "__main__":
    tracker = StudyTracker()
    tracker.run()
