class RepairLog:

    def __init__(self):
        self.repairs = []

    def add(self, issue, fix, section="ir"):

        self.repairs.append(
            {
                "section": section,
                "issue": issue,
                "fix": fix
            }
        )

    def get_repairs(self):
        return self.repairs
