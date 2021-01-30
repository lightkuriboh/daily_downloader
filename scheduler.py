
import time
import datetime

import utils


class JobScheduler:
    def __init__(self, specific_time, job, first_time_run_params, future_run_params):
        self.seconds = utils.datetime_to_second(specific_time)
        if self.seconds == 0:
            self.seconds = 60 * 60 * 24
        self.job = job
        self.future_run_params = future_run_params

        self.job(**first_time_run_params)

        while True:
            self.__run()

    def __run(self):
        current_seconds = utils.datetime_to_second(datetime.datetime.now())
        if self.seconds > current_seconds:
            if self.seconds - current_seconds > 2:
                time.sleep(self.seconds - current_seconds - 2)
            else:
                self.job(**self.future_run_params)
        else:
            day_end = datetime.datetime.now().replace(hour=23, minute=23, second=59)
            # sleep to end of day
            time.sleep(
                utils.datetime_to_second(day_end) - current_seconds
            )
