from math import fabs


def material_yield(strains, stresses, limit_strain=0.2e-2):
    assert len(strains) == len(stresses)

    seen_strains = []
    seen_stresses = []
    E = 0
    sy = 0
    plastic_deformation = 0

    while fabs(last(seen_strains) - plastic_deformation) <= limit_strain:
        if len(strains) == 0:
            print("The material did not yield in the data range provided")
            break

        seen_strains.append(strains.pop(0))
        seen_stresses.append(stresses.pop(0))
        E = linear_reg(seen_strains, seen_stresses)
        plastic_deformation = last(seen_stresses) / E if E != 0 else 0
        sy = seen_stresses[-1]

    return (E, sy)


def linear_reg(xs, ys):
    assert len(xs) == len(ys)
    return sum([y/x for x,y in zip(xs, ys) if x !=0]) / len(xs)


def last(xs):
    return xs[-1] if len(xs) != 0 else 0


if __name__ == '__main__':
    import csv
    with open('data.csv') as data:
        reader = csv.reader(data, delimiter=' ')
        strains = []
        stresses = []
        for row in reader:
            strains.append(float(row[0]))
            stresses.append(float(row[1]))

    E, sy = material_yield(strains, stresses)
    print(f'The elastic constant of the material is {E:.0f} MPa')
    print(f'The yield stress of the material is {sy:.0f} MPa')