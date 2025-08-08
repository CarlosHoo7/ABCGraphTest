from generate_graph import Create_Graph, Draw_Graph
import matplotlib.pyplot as plt
from PIL import Image

#sample data, you can use many products with different values
products = [
    {'name': 'Product A', 'usage': 120, 'avg_price': 50},
    {'name': 'Product B', 'usage': 80, 'avg_price': 30},
    {'name': 'Product C', 'usage': 200, 'avg_price': 20},
    {'name': 'Product D', 'usage': 60, 'avg_price': 40},
    {'name': 'Product E', 'usage': 150, 'avg_price': 25}
]

# Create the graph using the sample data
graph = Create_Graph(products=products)
# Draw the graph with specified parameters
Draw_Graph(graph)
# Save the graph to a file and display it
plt.axis('off')
plt.savefig("graph.png")
plt.clf()
image = Image.open('graph.png')
image.show()

