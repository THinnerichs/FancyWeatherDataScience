import numpy as np
import pandas as pd
import urllib.request



def get_description_tuples():
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

        elif line_number_str.strip() != "":
            start = int(line_number_str.strip())


        if start != -1 and end != -1:
            tuple_list.append((start,end,description,part_list))

    return tuple_list

def parse_children(description, line, index, index_child):
  beginn, end, string =  description
  return str(index)+"."+str(index_child) + "-" +  string, line[beginn-1:end].strip()

def parse_column(description, line, index):
  beginn, end, string, children =  description
  if len(children) < 1:
    return str(index)+"-"+string, line[beginn-1:end].strip()
  else:
    parsed_children = [parse_children(child, line, index, i_child) for (i_child,child) in enumerate(children)]
    parsed_children = list(filter(lambda x: x, parsed_children))
    labels, values = zip(*parsed_children)
    return str(index)+"-"+string, parsed_children

def parse_file(html_lines, tuple_list):
  series = []
  for line in html_lines[2:-4]:
    parsed_line = []
    for (i, t) in enumerate(tuple_list):
      label, value = parse_column(t, line, i)
      if type(value) is list:
        parsed_line.extend(value)
      else:
        parsed_line.append((label, value))

    labels, values = zip(*parsed_line)
    s = pd.Series(values, index=labels)
    series.append(s)
  return pd.DataFrame(series)

def main():
    tuple_list = get_description_tuples()
    years = range(2000, 2018, 1)
    months = range(1, 13)
    base_url = "https://www.dwd.de/EN/climate_environment/climatemonitoring/climatedatacenter/gsnmc/editorial/gsnmcdataset/gsn_{year}{month:02}_dat.dat?view=nasPublication&nn=359514"
    combinations = [{"year": year, "month": month} for year in years for month in months]
    dataframes = {}
    for combi in combinations:
        url = base_url.format(**combi)

        with urllib.request.urlopen(url) as response:
            html_lines = str(response.read()).split("\\n")
        dataframes[(combi["year"], combi["month"])] = parse_file(html_lines, tuple_list)
        dataframes[(combi["year"], combi["month"])].to_csv("{}-{}.csv".format(combi["year"], combi["month"]))
        print("Saved", "{}-{}.csv".format(combi["year"], combi["month"]))


if __name__ == '__main__':
    main()