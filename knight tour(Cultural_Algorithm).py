import matplotlib.pyplot as plt
import random
from operator import index


def chessboard(n):  # The chess board representation
    counter = 1
    for i in range(n):
        for j in range(n):
            print(counter, end=" ")
            counter += 1
        print('\n')


n = int(input("Enter the size of the chessboard: "))


########## population #################

crossover_point = 4
random.seed(211)  # if needed
generation = 1
mutation_rate = 0.2
max_fitness = n * n
max_chromosomes = 2000  # termination condition
no_of_elite = 3

belief_space = {  # dictionary with key and value to store knowledge and patterns
    "best_path": None,        #situational knowledge store (the best path and fitness over all so far)
    "best_fitness": 0,
    "preferred_moves": {},    #domain knowledge store ( the moves That have high frequency)
}


########## population generation #################

moves = [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]


def generate_random_knight_path():  # a function that generates a path randomly
    x, y = 0, 0  # starting the knight position
    path = [(x, y)]  # a list to keep track the visited squares
    while True:
        valid_moves = []  # List shows the valid moves that the knight can make
        for dx, dy in moves:  # test which moves are valid
            nx = dx + x
            ny = dy + y
            if (n > nx >= 0 and n > ny >= 0 and (nx, ny) not in path):  # check bounds and visited
                valid_moves.append((nx, ny))
        if not valid_moves:  # no moves left → tour ended
            break
        x, y = random.choice(valid_moves)
        path.append((x, y))
    return path


population = []  # list of all paths
fitness_list = []
for i in range(10):
    path = generate_random_knight_path()
    population.append(path)
    fitness: int = len(path)

population_with_fitness = [(path, len(path)) for path in population]  # paths with fitness
population_with_fitness.sort(key=lambda x: x[1], reverse=True)  # sort descending


########## update belief space #################

def update_belief_space(elite, belief_space):  # updating belief space
    best_path, best_fit = elite[0]
    # Situational knowledge
    if best_fit > belief_space["best_fitness"]: # if the elite fitness greater than max fitness ever
        belief_space["best_fitness"] = best_fit  #replace max fitness by it is
        belief_space["best_path"] = best_path[:] # replace best path by it

    # Domain knowledge (move frequency)
    for path, _ in elite: # here we ignore fitness we only care about the path , each ieration took a single path
        for i in range(len(path) - 1): # split the path into pair of moves (jumb) if it appears frequantly in elite so it got appended by its number of frequancy
            move = (path[i], path[i + 1])
            belief_space["preferred_moves"][move] = \
                belief_space["preferred_moves"].get(move, 0) + 1

########## cross over Function ################# (single point)


def next_valid_moves(x, y, child):
    valid_moves = []
    for dx, dy in moves:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < n and 0 <= ny < n:  # inside board
            if (nx, ny) not in child:
                valid_moves.append((nx, ny))
    return valid_moves


def belief_guided_move(current_pos, valid_moves, belief_space):
    for move in valid_moves:
        key = (current_pos, move) # now key is a single jump
        if key in belief_space["preferred_moves"]:  # if this jump in the belief space
            return move
    return random.choice(valid_moves)


def crossover_at_point(parent1, parent2, crossover_point):
    child = parent1[:crossover_point]  # first section of p1
    current_position = parent1[crossover_point - 1]

    for i in range(crossover_point, len(parent2), 1):  # add positions
        valid_moves = next_valid_moves(current_position[0], current_position[1], child)
        if parent2[i] in valid_moves:
            child.append(parent2[i])
            current_position = parent2[i]
        else:
            # Choose repair move instead of stopping
            if valid_moves:
                alt = belief_guided_move(current_position, valid_moves, belief_space)
                child.append(alt)
                current_position = alt
            else:
                break  # dead end only if no moves
    return child


########## mutation Function ################# (single point)


def mutate(path, rate):
    new_path = path[:1]  # keep start

    for i in range(1, len(path)): # loop on all the path
        if random.random() < mutation_rate:
            x, y = new_path[-1]
            valid_moves = [(x + dx, y + dy) for dx, dy in moves
                           if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in new_path]  # all valid moves
            if not valid_moves:
                break
            new_path.append(
                belief_guided_move((x, y), valid_moves, belief_space)  # use belief space
            )
        else:
            if path[i] not in new_path:
                new_path.append(path[i])
            else:
                # repair
                x, y = new_path[-1]
                valid_moves = [(x + dx, y + dy) for dx, dy in moves
                               if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in new_path]
                if not valid_moves:
                    break
                new_path.append(random.choice(valid_moves))
    return new_path


########## main loop #################

count = 1
overall_fitness_list = []

while count < max_chromosomes and population_with_fitness[0][1] != n * n:

    Elite = population_with_fitness[:no_of_elite]  # copy elite
    update_belief_space(Elite, belief_space)

    children = [path for path, fit in Elite]
    for i in range(no_of_elite, 10, 1):  # fill the generation
        p1, p2 = random.sample([p for p, f in population_with_fitness], 2)
        child = crossover_at_point(p1, p2, crossover_point)  # crossover
        child = mutate(child, mutation_rate)  # mutation
        children.append(child)

    children_with_fitness = [(path, len(path)) for path in children]
    children_with_fitness.sort(key=lambda x: x[1], reverse=True)

    population = [path for path, fit in children_with_fitness]
    population_with_fitness = children_with_fitness

    fitness_list = []
    for chromosome, fitness in population_with_fitness:
        print(f"Chromosome {count} | Fitness: {fitness} ")
        fitness_list.append(fitness)
        count += 1
        if population_with_fitness[0][1] == n * n:
            print("optimal solution reached")
    generation += 1

print(f"maximum fitness reached is : {max(fitness_list)}")
print(f"we reached : {round((max(fitness_list) / (n * n)) * 100, 2)} % of the optimal solution")


fitness_values_for_plot = fitness_list
chromosome_labels = [f'{i + 1}' for i in range(len(fitness_list))]

# plt.figure(figsize=(20,6))
# plt.plot(chromosome_labels, fitness_values_for_plot, color='blue')
# plt.xlabel("Chromosome")
# plt.ylabel("Fitness (Number of Visited Squares)")
# plt.title("Fitness Progression Over Chromosomes")
# plt.ylim(0, max(fitness_values_for_plot)+5)
# plt.xlim(-1, len(chromosome_labels))
# plt.xticks(rotation=45)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()
