from __future__ import annotations # imported to avoid forward references
from tabulate import tabulate

# Gene

class Gene:
    def __init__(self, gene: str) -> None:

        if len(gene) > 1:
            raise Exception("Gene must be a single character!")

        if not gene.isalpha():
            raise Exception("Gene must be a letter!")

        self.gene = gene

    def is_equal(self, other: Gene) -> bool:
        return self.gene == other.gene
    
    def is_allele(self, other: Gene) -> bool:
        return self.gene.lower() == other.gene.lower()

    @property
    def is_dominant(self) -> bool:
        return self.gene.isupper()


# Allele

class Allele:
    def __init__(self, genes: tuple[Gene, Gene]) -> None:
        if not genes[0].is_allele(genes[1]):
            raise Exception("Error! Cannot construct Allele class with non-allele genes!")
        self.genes = genes

    # Returns a dominant gene or recessive, if no dominant genes present.
    # Also can be thought of as getting a trait
    def get_dominant(self) -> Gene:
        if self.genes[0].is_dominant:
            return self.genes[0]
        return self.genes[1]
    
    def to_str(self) -> str:
        return self.genes[0].gene + self.genes[1].gene


class Chromosome:

    def __init__(self, alleles: list[Allele]) -> None:
        for i in range(len(alleles)):
            for j in range(i + 1, len(alleles)):
                if alleles[i].genes[0].is_allele(alleles[j].genes[0]):
                    raise Exception("Error! Chromosomes must be composed of unique traits!")
                
        self.alleles = alleles
    
    def from_str(sequence: str) -> 'Chromosome':
        if len(sequence) % 2 != 0:
            raise Exception("Error! Gene amount must be even!")

        alleles = []

        for i in range(int(len(sequence)/2)):
            alleles.append(Allele((Gene(sequence[2*i]), Gene(sequence[2*i + 1]))))
        
        return Chromosome(alleles)


    def get_traits(self) -> list[Gene]:
        return [allele.get_dominant() for allele in self.alleles]
    
    def is_compatible(self, other: Chromosome) -> bool:
        return self.get_traits() == other.get_traits()
    
    def to_str(self) -> str:
        return "".join([allele.to_str() for allele in self.alleles])

class Haploids:

    def __init__(self, parent: Chromosome) -> None:
        self.parent = parent

        def create_haploids(parent: Chromosome) -> list[list[Gene]]:
            alleles = parent.alleles

            current = alleles.pop(0).genes
            result = [[current[0]], [current[1]]]

            while len(alleles) != 0:
                first = alleles.pop(0)
                temp = []
                for gene in result:
                    for b in first.genes:
                        temp += [gene + [b]]
                result = temp
            
            return result

        self.haploids: list[list[Gene]] = create_haploids(parent)
    
    def as_str_list(self) -> list[str]:
        def haploid_to_str(genes: list[Gene]) -> str:
            return "".join([g.gene for g in genes])
        return [haploid_to_str(h) for h in self.haploids]

    # checks whether two haploids are a match
    # def is_fertilizible(mate: Haploids) -> bool:
    # Replaced by Chromosome.is_compatible




class OffSpring:

    def __init__(self, sperm: Haploids, eggs: Haploids) -> None:
        
        if not sperm.parent.is_compatible(eggs.parent):
            raise Exception("Genes of parents have different traits: cannot be fertilized.")
        
        self.sperm = sperm
        self.eggs = eggs

        def create_children(sperm: Haploids, eggs: Haploids) -> list[list[Chromosome]]:
            children: list[list[Chromosome]] = []
            for e in eggs.haploids:
                row = []
                for s in sperm.haploids:
                    child_alleles = []
                    for i in range(len(s)):
                        child_alleles.append(Allele((s[i], e[i])))
                    row.append(Chromosome(child_alleles))
                children += [row]
            
            return children

        self.children: list[list[Chromosome]] = create_children(sperm, eggs)

    # Genotype
    def get_genotypes(self) -> dict[str, int]:
        genotypes: dict[str, int] = {}

        for row in self.children:
            for child in row:
                genotypes[child.to_str()] = genotypes.get(child.to_str(), 0) + 1
    
        return genotypes

    # Phenotype (We can get it from fenotype, by purging come of its values)

    def get_phenotypes(self) -> dict[str, int]:

        def traits_to_str(genes: list[Gene]) -> str:
            return "".join([g.gene for g in genes])
        
        phenotypes: dict[str, int] = {}

        for key, value in self.get_genotypes().items():
            phenotype = traits_to_str(Chromosome.from_str(key).get_traits())
            phenotypes[phenotype] = phenotypes.get(phenotype, 0) + value

        return phenotypes
        


class PunnetSquare:
    def __init__(self, offspring: OffSpring) -> None:
        self.offspring = offspring
        
    # Display
    def display(self) -> None:
        body = []

        for row in self.offspring.children:
            temp_row = []
            for child in row:
                temp_row.append(child.to_str())
            body.append(temp_row)

        columns = self.offspring.eggs.as_str_list()
        rows = self.offspring.sperm.as_str_list()


        print(tabulate(body, headers=rows, tablefmt="fancy_grid", showindex=columns))