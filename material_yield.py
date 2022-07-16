from math import fabs


def material_yield(strains, stresses, limit_strain=0.2e-2):
    assert len(strains) == len(stresses)

    for i, (strain, stress) in enumerate(zip(strains, stresses)):
        if i+1 >= len(strains):
            break
        
        E = linear_reg(strains[:i+1], stresses[:i+1])
        plastic_deformation = stress / E if E != 0 else 0

        if fabs(strain - plastic_deformation) >= limit_strain:
            break

    return (E, stress)


def linear_reg(xs, ys):
    assert len(xs) == len(ys)
    return sum([y/x for x,y in zip(xs, ys) if x !=0]) / len(xs) if len(xs) !=0 else 0


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