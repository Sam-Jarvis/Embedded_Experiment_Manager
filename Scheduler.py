class Scheduler:
    """Responsible for all cron job and time related tasks"""

    def __init__(self):
        pass

    def minutesToHours(self, minutes):
        hours = int(minutes / 60)
        minutes = minutes % 60
        return (hours, minutes)

    