class Person:
    def __init__(self, employee_number, capabilities=None):
        """
        Initialize a Person object.

        :param employee_number: Unique identifier for the employee.
        :param capabilities: Dictionary mapping each capability to its proficiency level.
        """
        self.employee_number = employee_number
        self.capabilities = capabilities if capabilities else {}

    def add_capability(self, capability, proficiency):
        """
        Add a new capability with its proficiency level.

        :param capability: The capability to add.
        :param proficiency: Proficiency level for the capability.
        """
        self.capabilities[capability] = proficiency

    def update_proficiency(self, capability, proficiency):
        """
        Update the proficiency level for an existing capability.

        :param capability: The capability to update.
        :param proficiency: New proficiency level.
        """
        if capability in self.capabilities:
            self.capabilities[capability] = proficiency
        else:
            raise ValueError(f"Capability '{capability}' not found.")

    def get_proficiency(self, capability):
        """
        Get the proficiency level for a specific capability.

        :param capability: The capability to check.
        :return: Proficiency level.
        """
        return self.capabilities.get(capability, None)


class Organization:
    def __init__(self, name):
        """
        Initialize an Organization object.

        :param name: Name of the organization.
        """
        self.name = name
        self.employees = []
        self.requests = []

    def add_employee(self, person):
        """
        Add an employee to the organization.

        :param person: Person object representing the employee.
        """
        self.employees.append(person)

    def add_request(self, request):
        """
        Add a request to the organization.

        :param request: Dictionary with 'id' and 'required_capabilities' keys.
        """
        self.requests.append(request)

    def allocate_requests(self):
        """
        Allocate requests to employees based on their capabilities.

        :return: Dictionary mapping request IDs to employee numbers.
        """
        allocation = {}
        for request in self.requests:
            for employee in self.employees:
                if all(
                    employee.get_proficiency(cap) is not None and
                    employee.get_proficiency(cap) >= level
                    for cap, level in request['required_capabilities'].items()
                ):
                    allocation[request['id']] = employee.employee_number
                    break
            else:
                allocation[request['id']] = None  # No suitable employee found
        return allocation
    


# Example usage
if __name__ == "__main__":
    org = Organization("Tech Corp")

    # Adding employees
    emp1 = Person(101, {"Python": 5, "Java": 3})
    emp2 = Person(102, {"Python": 2, "Java": 4})
    emp3 = Person(103, {"Python": 4, "Java": 5})

    org.add_employee(emp1)
    org.add_employee(emp2)
    org.add_employee(emp3)

    # Adding requests
    org.add_request({"id": "R1", "required_capabilities": {"Python": 4}})
    org.add_request({"id": "R2", "required_capabilities": {"Java": 5}})
    org.add_request({"id": "R3", "required_capabilities": {"Python": 6}})

    # Allocating requests
    allocation = org.allocate_requests()
    print(allocation)  # Output: {'R1': 101, 'R2': 103, 'R3': None}