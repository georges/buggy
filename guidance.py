import time

class ObstacleAvoidance:    
    def __init__(self):
        self.last_surrounded_check = time.monotonic()
        self.obstacle_count = 0
        
    def perform(self, ui, robot, obstacle_range):
        if obstacle_range < 100:
            robot.stop()
            self.obstacle_count += 1
            ui.flash(50, 0, 0)
            robot.evade()
            ui.ok()
            robot.start()

        if self.obstacle_count > 5:
            self.obstacle_count = 0

            if time.monotonic() - self.last_surrounded_check < 30:
                robot.stop()
                ui.call_for_help()
            else:
                self.last_surrounded_check = time.monotonic()

class StuckEvasion:
    def __init__(self):
        self.last_obstacle_seen = time.monotonic()
        self.last_stuck_check = time.monotonic()
        self.stuck_count = 0
        
    def perform(self, ui, robot, obstacle_range):
        if obstacle_range < 100:
            self.last_obstacle_seen = time.monotonic()

        if (time.monotonic() - self.last_obstacle_seen > 30):
            self.stuck_count += 1
            robot.stop()
            ui.flash(0, 0, 50)
            robot.evade()
            ui.ok()
            robot.start()
            self.last_obstacle_seen = time.monotonic()

        if self.stuck_count > 3:
            self.stuck_count = 0

            if time.monotonic() - self.last_stuck_check < 130:
                robot.stop()
                ui.call_for_help()
            else:
                self.last_stuck_check = time.monotonic()