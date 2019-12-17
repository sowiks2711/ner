import morfeusz2
morf = morfeusz2.Morfeusz()
with open("../result_step_001.csv") as f:
    for line in f.readlines():
        columns=line.strip().split(';')
        person_name = columns[1]
        analysis = morf.analyse(person_name)
        indices = set(el[0] for el in analysis)
        result = []

        for index in indices:
            filtered_analysis = [el for el in analysis if el[0] == index]
            result.append(filtered_analysis[0][2][1].split(':')[0])
        columns[1] = " ".join(result).replace(" - ","-")
        print(";".join(columns))




