import networkx as nx
import json
from itertools import combinations
import random
from random import uniform
from .utils import SCHEMA_VERSION
from typing import TextIO, Optional

def save_graph(graph: nx.Graph, filename: str):
    """Saves a NetworkX graph object to JSON file.

    Args:
        graph (networks.Graph): the input graph object
        filename (string): name of the output file
    """
    f = open(filename, "w")
    graph_dict = nx.readwrite.json_graph.node_link_data(graph)
    graph_dict["schema"] = SCHEMA_VERSION + "-graph"
    json.dump(graph_dict, f, indent=2)
    f.close()


def load_graph(file: TextIO) -> nx.Graph:
    """Reads a JSON file for extracting the NetworkX graph object.

    Args:
        file (str or file-like object): the file to load
    
    Returns:
        networkx.Graph: the graph
    """

    if isinstance(file, str):
        with open(file, "r") as f:
            data = json.load(f)
    else:
        data = json.load(file)

    return nx.readwrite.json_graph.node_link_graph(data)


def compare_graphs(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    """Compares two NetworkX graph objects to see if they are identical.
    NOTE: this is *not* solving isomorphism problem.
    """

    for n1, n2 in zip(graph1.nodes, graph2.nodes):
        if n1 != n2:
            return False
    for e1, e2 in zip(graph1.edges, graph2.edges):
        if e1 != e2:
            return False
    return True


def generate_graph_node_dict(graph: nx.Graph) -> dict:
    """Generates a dictionary containing key:value pairs in the form of
                    nx.Graph node : integer index of the node
    
    Args:
        graph: nx.Graph object
    
    Returns:
        A dictionary as described
    """
    nodes_int_map = []
    for node_index, node in enumerate(graph.nodes):
        nodes_int_map.append((node, node_index))
    nodes_dict = dict(nodes_int_map)
    return nodes_dict


def generate_random_graph_erdos_renyi(
    num_nodes: int, probability: float, random_weights: bool = False, min_weight:Optional[int]=0, max_weight:Optional[int]=1, seed: Optional[int] = None
) -> nx.Graph:
    """Randomly generate a graph from Erdos-Renyi ensemble. 
    A graph is constructed by connecting nodes randomly. 
    Each edge is included in the graph with probability p independent from 
    every other edge. Equivalently, all graphs with n nodes and M edges have 
    equal probability.

    Args:
        num_nodes: integer
            Number of nodes.
        probability: float
            Probability of two nodes connecting.
        random_weights: bool
            Flag indicating whether the weights should be random or constant.
    
    Returns:
        A networkx.Graph object
    """
    output_graph = nx.erdos_renyi_graph(n = num_nodes, p = probability, seed = seed)
    output_graph = weight_graph_edges(output_graph, random_weights, min_weight, max_weight, seed)
     
    return output_graph

def generate_random_regular_graph(
    num_nodes: int, degree: int, random_weights: bool = False, seed: Optional[int] = None
) -> nx.Graph:
    """Randomly generate a d-regular graph. 
    A graph is generated by picking uniformly a graph among the set of graphs 
    with the desired number of nodes and degre.

    Args:
        num_nodes: integer
            Number of nodes.
        degre: int
            Degre of each edge.
        random_weights: bool
            Flag indicating whether the weights should be random or constant.
    
    Returns:
        A networkx.Graph object
    """
    output_graph = nx.random_regular_graph(d = degree, n = num_nodes, seed = seed)
    output_graph = weight_graph_edges(output_graph, random_weights, seed)

    return output_graph

def weight_graph_edges(
    graph: nx.Graph, random_weights: bool = False, min_weight:Optional[int]=0, max_weight:Optional[int]=1, seed: Optional[int] = None
) -> nx.Graph:
    """Update the weights of all the edges of a graph. 

    Args:
        graph: nx.Graph
            The input graph.
        random_weights: bool
            Flag indicating whether the weights should be random or constant (1.).
    
    Returns:
        A networkx.Graph object
    """
    assert not(graph.is_multigraph()), "Cannot deal with multigraphs"
    
    random.seed(seed)
    if random_weights:
        weighted_edges = [(e[0], e[1], uniform(min_weight, max_weight)) for e in graph.edges]
    else:
        weighted_edges = [(e[0], e[1], 1.0) for e in graph.edges]
    
    # If edges already present, it will effectively update them (except for multigraph)
    graph.add_weighted_edges_from(weighted_edges)
    return graph

def generate_graph_from_specs(graph_specs:dict) -> nx.Graph:
    """Generate a graph from a specs dictionary

    Args:
        graph_specs: dictionnary
            Specifications of the graph to generate. It should contain at 
            least an entry with key 'type' and one with num_nodes
    
    Returns:
        A networkx.Graph object
    """
    type_graph = graph_specs['type_graph']
    num_nodes = graph_specs['num_nodes']
    random_weights = graph_specs.get('random_weights', False)
    seed = graph_specs.get('seed', None)
    
    if type_graph == 'erdos_renyi':
        probability = graph_specs['probability']
        graph = generate_random_graph_erdos_renyi(num_nodes, probability, random_weights, seed)
    
    elif type_graph == 'regular':
        degree = graph_specs['degree']
        graph = generate_random_regular_graph(num_nodes, degree, random_weights, seed)
    
    elif type_graph == 'complete':
        graph = generate_random_graph_erdos_renyi(num_nodes, 1., random_weights, seed)
        
    else:
        raise(NotImplementedError("This type of graph is not supported: ", type_graph))

    return graph
