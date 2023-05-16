class Command:
    def __init__(self, name, arguments, author):
        self.name = name
        self.arguments = arguments
        self.author = author
        self.next_command = None
        self.prev_command = None

class CommandHistory:
    def __init__(self):
        self.commands = []

    def add_command(self, command_name, arguments):
        self.commands.append({"command_name": command_name, "arguments": arguments})

    def get_previous_command(self):
        # Implementation for getting the previous command goes here
        pass

    def get_next_command(self):
        # Implementation for getting the next command goes here
        pass

    def get_commands_by_user(self, user_id):
        user_commands = []
        for command in self.commands:
            # Assuming the user_id is stored in the "arguments" field of the command
            if command["arguments"] == user_id:
                user_commands.append(command)
        return user_commands

    def clear(self):
        self.commands = []
