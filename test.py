from main import *

# ----- TEST CLASS NODE -----

# Renvoi d'erreur de définition : 

# Erreur de formatage pour node_type
# Node(node_type="bonjour", node_pos=(-5,-5), node_value=56, node_string=20, children=[5, "Café"])

# Erreur d'argument node_value - il doit être à None pour node_type == "nd_*"
# Node(node_type="nd_*", node_pos=(0,0), node_value=56, node_string="Baboum Chakal", children=[5, "Café"])

# Erreur d'argument node_value - il doit avoir une valeur pour node_type == "nd_const"
# Node(node_type="nd_const", node_pos=(0,0), node_string="Baboum Chakal", children=[5, "Café"])

# Erreur d'argument node_value - il doit être à None pour node_type == "nd_*"
# Node(node_type="nd_*", node_pos=(0,0), node_value=56, node_string="Baboum Chakal", children=[5, "Café"])

# Erreur d'argument node_string - il doit avoir une valeur pour node_type == "nd_ident"
# Node(node_type="nd_ident", node_pos=(0,0), node_string="Baboum Chakal", children=[5, "Café"])

# Erreur d'argument node_string - il doit être à None pour node_type != "nd_ident"
# Node(node_type="nd_*", node_pos=(0,0), node_string="Baboum Chakal", children=[5, "Café"])

# Erreur de position négative
# Node(node_type="nd_*", node_pos=(-5,-5), node_value=56, node_string="Baboum Chakal", children=[5, "Café"])

# Erreur de dimension de la position
# Node(node_type="nd_*", node_pos=(0,0,0), node_value=None, node_string="Baboum Chakal", children=[5, "Café"])


# Erreur de type pour le premier enfant
# Node(node_type="nd_*", node_pos=(0,0), children=[5, "Café"])

op1=Node(node_type="nd_const", node_pos=(0,0),node_value=1)
op2=Node(node_type="nd_const", node_pos=(0,2),node_value=2)
assert Node(node_type="nd_*", node_pos=(0,1), children=[op1, op2]), "Impossible de créer un noeud multiplication avec deux enfants."

