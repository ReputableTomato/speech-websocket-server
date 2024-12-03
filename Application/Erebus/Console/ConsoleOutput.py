import curses

from Erebus.Generic.Utilities.Date import Date

class ConsoleOutput:

    __instance = None

    def __init__(self):
        if __class__.__instance != None:
            self = __class__.__instance
        else:
            __class__.__instance = self

            self.__console_output = curses.initscr()
            self.__output_list = []

            self.__last_action = 0
            self.__total_connection_count = 0
            self.__unauthenticated_count = 0
            self.__user_count = 0
            self.__node_count = 0

            curses.noecho()
            curses.cbreak()
            curses.start_color()
            curses.use_default_colors()

            self.register_colours()

    @staticmethod
    def print(text) -> None:
        console_output = __class__.instance().console_output

        if len(__class__.instance().__output_list) == 5:
            __class__.instance().__output_list.pop(0)

        __class__.instance().__output_list.append("{} - {}".format(Date.timestring(), text))

        __class__.refresh_console()

    @staticmethod
    def connection_update(last_action = None, total_connection_count = None, unauthenticated_count = None, user_count = None, node_count = None) -> None:
        __class__.__last_action = last_action
        __class__.__total_connection_count = total_connection_count
        __class__.__unauthenticated_count = unauthenticated_count
        __class__.__user_count = user_count
        __class__.__node_count = node_count
    
    @staticmethod
    def refresh_console():
        last_action_string = "Last action: "
        total_connections_string = "Total Connections: "
        unauthenticated_string = "Unauthenticated: "
        users_string = "Users: "
        nodes_string = "Nodes: "
        connection_output_end = 5

        console_output = __class__.instance().console_output
        console_output.erase()

        console_output.addstr(0, 0, last_action_string)
        console_output.addstr(0, len(last_action_string), __class__.__last_action, curses.color_pair(161))

        console_output.addstr(1, 0, total_connections_string)
        console_output.addstr(1, len(total_connections_string), str(__class__.__total_connection_count), curses.color_pair(227))

        console_output.addstr(3, 0, unauthenticated_string)
        console_output.addstr(3, len(unauthenticated_string), str(__class__.__unauthenticated_count), curses.color_pair(227))

        console_output.addstr(4, 0, users_string)
        console_output.addstr(4, len(users_string), str(__class__.__user_count), curses.color_pair(227))

        console_output.addstr(connection_output_end, 0, nodes_string)
        console_output.addstr(connection_output_end, len(nodes_string), str(__class__.__node_count), curses.color_pair(227))

        if __class__.instance().__output_list:
            extra_output_start_index = connection_output_end + 2

            for output in __class__.instance().__output_list:
                console_output.addstr(extra_output_start_index, 0, str(output))

                extra_output_start_index += 1

        console_output.refresh()

    def register_colours(self):
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    @property
    def console_output(self):
        return self.__console_output

    @property
    def connection_output_end(self):
        return self.__connection_output_end

    @staticmethod
    def instance():
        if __class__.__instance == None:
            return __class__()

        return __class__.__instance