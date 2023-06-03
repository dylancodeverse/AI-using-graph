class graph_access_file:

    @staticmethod
    def get_all_lines(path: str) -> list[str]:
        with open(path, 'r') as file:
            lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.strip() for line in lines]
        # Remove unnecessary spaces in each line
        lines = [''.join(line.split()) for line in lines]
        return lines

    @staticmethod
    def get_elements(all_lines: list[str], index: int) -> list[str]:
        first_line = all_lines[index]
        # Check if the first line has the desired format
        if not (first_line.startswith('[') and first_line.endswith(']')):
            raise ValueError("First line is not in the expected format.")

        # Remove unnecessary spaces and create a list from the format
        formatted_line = first_line.strip('[]')
        elements = [elem.strip() for elem in formatted_line.split(',')]

        return elements

    @staticmethod
    def get_bool(all_lines: list[str], index: int) -> bool:
        line = all_lines[index]
        line = line.strip().lower()  # Convert to lowercase and remove leading/trailing spaces

        if line == 'true':
            return True
        elif line == 'false':
            return False
        else:
            raise ValueError("Line does not represent a boolean value.")

    @staticmethod
    def get_adjancy_list(all_lines: list[str], index: int = 2, is_weighted: bool = True) -> dict:
        adjancy_list = {}
        for line in all_lines[index:]:
            graph_access_file.process_line(line, adjancy_list, is_weighted)
        return adjancy_list
    
    @staticmethod
    def process_line(line: str, adjancy_list: dict, is_weighted: bool):
        line_parts = line.split('->')
        if len(line_parts) != 2:
            raise ValueError("Line is not in the expected format.")
        source_index = line_parts[0]
        destinations = line_parts[1]
        dest_list = []
        dest_items = destinations.split(',')
        if is_weighted:
            for dest in dest_items:
                if not dest.startswith('(') or not dest.endswith(')'):
                    raise ValueError("Line is not in the expected format.")
                dest = tuple(dest[1:-1].split(';'))
                dest_list.append(dest)
            adjancy_list[source_index] = dest_list
        else:
            for dest in destinations.split(','):
                dest_list.append(dest)
            adjancy_list[source_index] = dest_list

