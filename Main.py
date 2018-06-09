

def main():
    #open file and read values into list

    raw_list = []
    with open(file= "data_description", mode='r') as file:
        for line in file:
            if line.strip() != "":
                raw_list.append(line)

    #3 tuple: first element is the starting line of the field, second is the ending line of the field, third is list of tuples of values below in tree structure, fourth is description
    tuple_list = []
    for line in raw_list:
        line_number_str = line[:8].strip()
        description = line[8:].strip()
        part_list = []

        start, end = -1, -1
        if '-' in line_number_str:
            start, end = [int(x) for x in line_number_str.split('-')]
            print("Start:", start, "End:", end)
            for line in raw_list:
                part_line_number_str = line.strip()[:8].strip()
                part_description = line.strip()[8:].strip()

                part_start, part_end = -1,-1
                if '-' in part_line_number_str:
                    part_start, part_end = [int(x) for x  in part_line_number_str.split('-')]
                elif part_line_number_str != "":
                    part_start = int(part_line_number_str)
                    part_end = part_start

                if start <= part_start and part_end <= end and line[:8].strip() == "":
                    part_list.append((part_start,part_end,part_description))
                    print("Tuple:",(part_start,part_end,part_description))
        elif line_number_str.strip() != "":
            start = int(line_number_str.strip())
            print("Start:", start, "End:", start)

        if start != -1 and end != -1:
            tuple_list.append((start,end,description,part_list))

    print(tuple_list)


if __name__ == '__main__':
    main()


