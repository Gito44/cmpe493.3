data_path=r"D:\kod\cmpe493\ass3\data.txt"


def read_data(path):

    vertices={}
    edges=[]
    edge=False
    with open(path,"r") as d:
        lines= d.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('*Vertices'):
                vertice_count = int(line.split()[1])
            elif line.startswith('*Edges'):
                edge = True
            elif edge:
                vertex1, vertex2 = map(int, line.split())
                edges.append((vertex1, vertex2))
            else:
                vertex_id, vertex_label = line.split()
                vertices[int(vertex_id)] = vertex_label
        return vertice_count, vertices, edges


def find_reverse_edges(edges):
    reverse_edges = edges
    for (a,b) in edges:
        reverse_edges= reverse_edges + [(b,a)]
    return reverse_edges


def find_matrix(vertice_count,reverse_edges):
    matrix = []
    for i in range(vertice_count):
        matrix.append([0] * vertice_count)

    count = [0] * vertice_count
    for (u, v) in reverse_edges:
        count[u - 1] += 1

    for (u, v) in reverse_edges:
        matrix[v - 1][u - 1] = 1 / count[u - 1]
    return matrix


def matrix_vector_product(matrix, vector):
    result = [0] * len(vector)

    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]

    return result

def calculate_page_rank(matrix, teleportation_rate=0.10, max_iterations=100, convergence_threshold=1e-6):
    num_vertices = len(matrix)
    teleportation = [teleportation_rate / num_vertices] * num_vertices
    rank = [1 / num_vertices] * num_vertices

    for _ in range(max_iterations):
        new_rank = [(1 - teleportation_rate) * x for x in matrix_vector_product(matrix, rank)]
        new_rank = [x + y for x, y in zip(new_rank, teleportation)]

        if sum(abs(new_rank[i] - rank[i]) for i in range(num_vertices)) < convergence_threshold:
            break

        rank = new_rank

    return rank


def find_top_ranked_people(rank, vertices, no=20):
    sorted_list = sorted(range(len(rank)), key=lambda i: rank[i], reverse=True)[:no]
    top_people = [(vertices[i+1], rank[i]) for i in sorted_list]
    return top_people



vertice_count, vertices , edges = read_data(data_path)
reversed_edges= find_reverse_edges(edges)
matrixx= find_matrix(vertice_count,reversed_edges)
rank= calculate_page_rank(matrixx)
top_people=find_top_ranked_people(rank,vertices)
for person, rank in top_people:
    print(f"{person}: {rank}")

input("press enter to exit.")