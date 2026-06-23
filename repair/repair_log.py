class RepairLog:

    def __init__(self):
        self.repairs = []

    def add(self, issue, fix):

        self.repairs.append(
            {
                "issue": issue,
                "fix": fix
            }
        )

    def get_repairs(self):
        return self.repairs