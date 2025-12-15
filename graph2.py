import xml.etree.ElementTree as ET
from graphviz import Digraph
import sys

# Test for filepath argument
try:
    XML_FILE = sys.argv[1]
except:
    XML_FILE = input("Bestandsnaam configuratie: ")

# Parse XML
tree = ET.parse(XML_FILE)
root = tree.getroot()

# Number of sources (inputs)
sources = root.find("Sources")
num_sources = len(sources.findall("Source"))

# Queue lengths
queues_xml = root.find("Queues").findall("Queue")
queue_lengths = [int(q.find("Length").text) for q in queues_xml]

# Queues connected to destinations
servers_xml = root.find("Servers").findall("Server")
destinations = [(int(s.find("Destination").text), int(
    s.find("Queue").text)) for s in servers_xml]

# Routing matrix
routing_xml = root.find("Routing").findall("Element")
routing_matrix = {}
for e in routing_xml:
    i = int(e.attrib["i"])
    j = int(e.attrib["j"])
    routing_matrix[(i, j)] = float(e.text)

# Build diagram
dot = Digraph("RouterDiagram", format="png")
dot.attr(rankdir='LR', fontsize='12', splines="polyline",
         ranksep="3.0", nodesep="0.2")

# Add inputs
for i in range(num_sources):
    dot.node(f"IN{i}", f"Source {i}", shape="box")


# Add queues
for i in range(len(queue_lengths)):
    buf_name = f"BUF{i}"
    dot.node(buf_name, f"C = {queue_lengths[i]}", shape="box",
             style="filled", fillcolor="#C1FFC1")
    for j in range(num_sources):
        # Connect inputs to queues
        dot.edge(f"IN{j}", buf_name)

# Add destinations
unique_destinations = sorted(set(destinations))
for (d, b) in unique_destinations:
    dot.node(f"DEST{d}", f"Destination {d}", shape="box")

    # Connect queues to destinations
    count = destinations.count((d, b))
    for _ in range(count):
        dot.edge(f"BUF{b}", f"DEST{d}")

# Save and render
dot.render("router_diagram", cleanup=True)
print("Diagram generated as router_diagram.png")
