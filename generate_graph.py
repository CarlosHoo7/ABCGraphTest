import networkx as nx
import matplotlib.pyplot as plt
import random

def ABC_Method (products=[]):
    """Classify types of products using the ABC method. This function uses a nested structure where each product has a name, usage, and average price. For Example:
    products = [
        {'name': 'Product A', 'usage': 100, 'avg_price': 50},
        {'name': 'Product B', 'usage': 200, 'avg_price': 30},
        {'name': 'Product C', 'usage': 300, 'avg_price': 20},
        ...
    ]

    Args:
        products (dict): List of product types (More than 3 product types). This is a nested structure where each product has a name, usage, and average price.
    Returns:
        rating (dict) : The A-B-C rated products, each rate includes types of product stored as a nested structure with name and value.
    """
    
    product_count = len(products)
    if product_count < 3: raise ValueError("At least 3 products are required for classification.")
    rating_limits = {'A' : int(product_count * 0.20) if int(product_count * 0.20) > 0 else 1,
                       'B' : int(product_count * 0.30) if int(product_count * 0.30) > 0 else 1,
                       'C' : int(product_count * 0.50)}
    limit_total_count = rating_limits['C'] + rating_limits['B'] + rating_limits['A']

    # Adjust in case the total is less than the number of products
    if limit_total_count < product_count: rating_limits['C'] += 1
    rating = {'A':[], 'B':[], 'C':[]}
    #Get product usage value => avg product usage * avg product price
    unrated_products_value = {}
    for product in products:
        value = int(product['usage']) * int(product['avg_price'])
        unrated_products_value[product['name']] = value
    for rate in rating:
        #do these steps until reaching the limit for each rating
        for i in range(rating_limits[rate]):
            suitable_product = max(unrated_products_value, key=unrated_products_value.get)
            suitable_product_value = max(unrated_products_value.values()) 
            unrated_products_value.pop(suitable_product)
            rating[rate].append({'name': suitable_product, 'value' : suitable_product_value})
    return rating

def Get_Adjacency(products):
    """Get the adjacency matrix for the ABC method. This function uses a nested structure where each product has a name, usage, and average price. For Example:
    products = [
        {'name': 'Product A', 'usage': 100, 'avg_price': 50},
        {'name': 'Product B', 'usage': 200, 'avg_price': 30},
        {'name': 'Product C', 'usage': 300, 'avg_price': 20},
        ...
    ]
    Args:
        products (dict): List of product types (More than 3 product types). This is a nested structure where each product has a name, usage, and average price.
    Returns:
        adjacency (dict) : The adjacency matrix for the ABC method, where each product is connected to its rating with the value of the product.
    """
    adjacency = {}
    rated_vertices = ABC_Method(products)
    for rate in rated_vertices:
        for edge in rated_vertices[rate]:
            adjacency [edge['name']] = {rate : edge['value']} 
    return adjacency

def Get_Edges(products):
    """Get the edges for the ABC method. This function uses a nested structure where each product has a name, usage, and average price. For Example:
    products = [
        {'name': 'Product A', 'usage': 100, 'avg_price': 50},
        {'name': 'Product B', 'usage': 200, 'avg_price': 30},
        {'name': 'Product C', 'usage': 300, 'avg_price': 20},
        ...
    ]
    Args:
        products (dict): List of product types (More than 3 product types). This is a nested structure where each product has a name, usage, and average price.
    Returns:
        edges (list) : The edges for the ABC method, where each edge is a dictionary with the product name and its rating.
    """
    edges = []
    rated_vertices = ABC_Method(products)
    for rate in rated_vertices:
        for product in rated_vertices[rate]:
            edges.append({'name' : product['name'], 'rate' : rate})
    return edges

def Organize_Positions (pos: dict, organized_vertices):
    """Organize the positions of the vertices in the graph from highest to lowest according to a list order.
    Args:
        pos (dict): The positions of the vertices in the graph.
        organized_vertices (list): An organized list of vertices, from highest to lowest
    Returns:
        dict: A dictionary with the positions of the vertices in the graph, organized from highest to lowest.
    """
    filtered_positions = [pos[vertex] for vertex in organized_vertices]
    sorted_positions = sorted(filtered_positions, key=lambda p: p[1], reverse=True)
    return {vertex: sorted_positions[i] for i, vertex in enumerate(organized_vertices)}
        
def Create_Graph(products):
    """Create a bipartite graph using the ABC method to classify the nodes. Every node (product) is connected with a rating node (A,B or C).
    This function uses a nested structure where each product has a name, usage, and average price. For Example:
    products = [
        {'name': 'Product A', 'usage': 100, 'avg_price': 50},
        {'name': 'Product B', 'usage': 200, 'avg_price': 30},
        {'name': 'Product C', 'usage': 300, 'avg_price': 20},
        ...
    ]
    Args:
        products (dict): List of product types (More than 3 product types). This is a nested structure where each product has a name, usage, and average price.
    Returns:
        dict: A dictionary that stores the graph, left vertices, right vertices, position, edges, and rating data."""
    graph = nx.Graph()
    left_vertices = [product['name'] for product in products]
    graph.add_nodes_from(left_vertices, bipartite = 0)
    #Right vertices will always be 'A', 'B', 'C' for the ABC method
    right_vertices = ['A', 'B', 'C']
    graph.add_nodes_from(right_vertices, bipartite = 1)
    edges = Get_Edges(products)
    adjacency = Get_Adjacency(products)
    edges_list = [(edge['name'], edge['rate']) for edge in edges]
    graph.add_edges_from(edges_list)
    for edge in edges:
        start = edge['name']
        end = edge['rate']
        graph[start][end]['weight'] = int(adjacency[start][end])
    pos = Organize_Positions(nx.drawing.layout.bipartite_layout(graph,left_vertices,'vertical'),left_vertices)
    pos.update(Organize_Positions(nx.drawing.layout.bipartite_layout(graph,left_vertices,'vertical'),right_vertices))
    return {'graph' : graph,
            'left_vertices' : left_vertices,
            'right_vertices' : right_vertices,
            'position' : pos,
            'edges' : edges,
            'rating' : ABC_Method(products)}

def Position_Labels(pos):
    """Position the labels inside the edges of the graph.
    Args:
        pos (dict): The positions of the vertices in the graph.
    Returns:
        dict: A dictionary with the positions of the labels of the edges in the graph."""
    edge_labels_positions = {}
    for label, coordinates in pos.items():
        x_pos = coordinates[0]
        y_pos = coordinates[1]
        #this threshold is used to avoid overlapping labels
        threshold = 0.04
        edge_labels_positions[label] = (x_pos, y_pos + threshold)
    return edge_labels_positions

def Draw_Graph (graph, size_x=6, size_y=8.5, node_colors={'A': '#40e0d0', 'B': '#eda11f', 'C': '#f62536'},node_size=100, font_size=8):
    """Draw the ABC method graph using matplotlib and networkx. The ABC nodes recibe a different color from green, yellow to red.
    The most adequate value for each category is highlighted in the graph with that given color (higher value for A and B, lowest for C).
    Args:
        graph (dict): The graph to be drawn, which includes the graph structure, positions, edges, and ratings.
        size_x (int): The width of the graph.
        size_y (int): The height of the graph.
        node_colors (dict): A dictionary with the colors for each rating node (A, B, C).
        node_size (int): The size of the nodes in the graph.
        font_size (int): The font size for the labels in the graph.
    """
    edge_labels = nx.get_edge_attributes(graph['graph'],'weight')
    #Find the highest value for A-B categories, and lowest for C
    highest_values = {'A' : 0, 'B' : 0, 'C' : 0}
    for rate in graph['rating']:
        for product in graph['rating'][rate]:
            if rate != 'C':
                highest_values[rate] = max(highest_values[rate], product['value'])
            else:
                highest_values[rate] = min(highest_values[rate], product['value']) if highest_values[rate] != 0 else product['value']

    size = (size_x, size_y)
    fig = plt.figure (0, figsize=size,dpi=200)

    nx.draw_networkx_nodes(graph['graph'],pos=graph['position'],nodelist=graph['left_vertices'],node_size=node_size)
    
    #Color each node according to its rating
    for rate in graph['right_vertices']:
        nx.draw_networkx_nodes(graph['graph'],pos=graph['position'],nodelist=rate, node_size=100,node_color=node_colors[rate])
    nx.draw_networkx_labels(graph['graph'],pos=Position_Labels(graph['position']),font_size=font_size)

    #Color the edge if the its the most adequate product for the category
    for edge in graph['edges']:
        rating = edge['rate']
        value = graph['graph'][edge['name']][rating]['weight']

        if value == highest_values[rating]:
            nx.draw_networkx_edges(graph['graph'],pos=graph['position'], edgelist=[(edge['name'], rating)], edge_color=node_colors[rating])
        else:
            nx.draw_networkx_edges(graph['graph'],pos=graph['position'], edgelist=[(edge['name'], rating)])
    #lable position sorting to avoid overlapping
    previous_position = 0
    label_position = random.uniform(0.3, 0.9)
    for edge in edge_labels:
        while abs(label_position - previous_position) < 0.21:
            label_position = random.uniform(0.3, 0.9)
        previous_position = label_position
        edge_label = {edge: edge_labels[edge]}
        nx.draw_networkx_edge_labels(graph['graph'], pos=graph['position'], edge_labels=edge_label, label_pos=label_position, font_size=font_size-3, node_size=50)
