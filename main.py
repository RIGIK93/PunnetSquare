from lib import Chromosome, Haploids, PunnetSquare, OffSpring

if __name__ != '__main__':
  raise Exception("This program cannot be imported! Please run it directly!")

raw = input("Enter Gene Combination: ")

raw_chromosomes = raw.split("x")

father = Chromosome.from_str(raw_chromosomes[0])
mother = Chromosome.from_str(raw_chromosomes[1])

sperm = Haploids(father)
eggs = Haploids(mother)

children = OffSpring(sperm, eggs)

table = PunnetSquare(children)

print("\nPunnet Square:")
table.display()

children_total = len(children.children) * len(children.children[0])
print("\nGenotypes:")
for genotype, count in children.get_genotypes().items():
  print(f"{genotype} \t:\t {count} ({int(count/children_total * 100)}%)")

print("\nPhenotypes:")
for phenotype, count in children.get_genotypes().items():
  print(f"{phenotype} \t:\t {count} ({int(count/children_total * 100)}%)")