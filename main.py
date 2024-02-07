from tabulate import tabulate

if __name__ != '__main__':
  raise Exception("This program cannot be imported! Please run it directly!")

# ---------------------
# COLLECTING USER INPUT
# ---------------------

# Counts how many times a certain values appears in the array (for instance, how many times the value "1" appears in the array [1, 2, 3, 1, 2, 3]. In this case, the value "1" appears 3 times. Then occurence_count([1, 2, 3, 1, 2, 3], 1) is 3)
def occurence_count(arr: list[any], val: any) -> int:
  count = 0
  for i in arr:
    if i == val:
      count += 1
  return count

def verify_input(str: str) -> bool:
  if len(str) == 0:
    print("Error: Empty Input")
    return False

  # Check for x multiplication symbol
  if str.find("x") == -1:
    print("Error: x symbol not found")
    return False

  # Check that there are only two chromosomes, by making sure there is only one x
  if occurence_count(str, "x") != 1:
    print("Error: More than one x symbol found")
    return False

  chromosomes = str.split("x")
  # Check that the amount of genes is equal for both parents

  if len(chromosomes[0]) != len(chromosomes[1]):
    print("Error: Chromosomes have different amount of genes")
    return False
  
  # Check that genes pair up
  for i in range(int(len(chromosomes[0])/2)):
    if chromosomes[0][2*i].lower() != chromosomes[0][2*i + 1].lower():
      print("Error: Alleles in chromosome 1 do not pair up! Please check your input!")
      return False


  for i in range(int(len(chromosomes[1])/2)):
    if chromosomes[1][2*i].lower() != chromosomes[1][2*i + 1].lower():
      print("Error: Alleles in chromosome 2 do not pair up! Please check your input!")
      return False
    
  # Check that genes from both parents correspond to one another
  for i in range(len(chromosomes[0])):
    if chromosomes[0][i].lower() != chromosomes[1][i].lower():
      return False
  
  return True

while True:
  raw = input("Enter Gene Combination: ")
  if verify_input(raw):
    break
  else: 
    print("Invalid Gene Combination, please try again.")

# -------------------------
# CALCULATING CROSS DIAGRAM
# -------------------------

# Separating the input onto parent genes (AaxAA becomes Aa, AA)
chromosomes = raw.split("x")

# TODO: Rename to split_alleles
def pair_genes(chromosome):
  pairs = []
  for i in range(int(len(chromosome)/2)):
      pairs.append([chromosome[2*i], chromosome[2*i+1]])
  return pairs

father_genes = pair_genes(chromosomes[0])
mother_genes = pair_genes(chromosomes[1])

def create_haploids(genes):
  a = genes.pop(0)
  result = [[a[0]], [a[1]]]
  while len(genes) != 0:
      first = genes.pop(0)
  
      temp = []
  
      for gene in result:
          for b in first:
              temp += [gene + [b]]
  
      result = temp
  
  return result

father_haploids = create_haploids(father_genes)
mother_haploids = create_haploids(mother_genes)

def choose_dominant(gene1: str, gene2: str):
  if gene1.isupper():
    return gene1
  else:
    return gene2

def create_children(father, mother):
  children = []

  for mother_allele in mother:
    column = []
    for father_allele in father:
      child = []
      for i in range(len(father_allele)):
        child += choose_dominant(father_allele[i], mother_allele[i])
      column += [child]
      
    children += [column]

  return children

children = create_children(father_haploids, mother_haploids)

# ------------------------
# OUTPUTTING CROSS DIAGRAM
# ------------------------


def display(body: list[any], rows: list[str], columns: list[str]):
  print(tabulate(body, headers=columns, tablefmt="fancy_grid", showindex=rows))

def join_chars(chars: list[str]) -> str:
  s = ''
  for ch in chars:
    s += ch
  return s

body = []

for row in children:
  tmp_row = []
  for child in row:
    tmp_row += [join_chars(child)]
  body += [tmp_row]

rows = []

for haploid in mother_haploids:
  rows += [join_chars(haploid)]

columns = []

for haploid in father_haploids:
  columns += [join_chars(haploid)]

display(body, rows, columns)

# ------------------
# FINDING PHENOTYPES
# ------------------



# -----------------
# FINDING GENOTYPES
# -----------------

