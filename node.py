from typing import Optional, Tuple, List

all_nodes = []

class Node:
     
    def __init__(self, node_type:str,node_pos: Tuple[int,int], node_value : Optional[int] = None, node_string: Optional[str] = None, node_children: List['Node'] = None):
        """ 
        Classe représentant les objets Noeud (Node) pour la construction d'arbre dans le but de gérer le code dans le bon ordre

        @params
        Entrée : node_type,     type String, type du noeud, liste d'argument : nd_const (constante num), nd_ref (identifiant str)
                 node_pos,      type Tuple(ligne:int, colonne:int), position du noeud dans le code
                 node_value,    type Int, valeur du noeud quand c'est une constante numérique (optionnel)
                 node_string,   type String, valeur du noeud quand c'est une constante alphabétique (optionnel)
                 node_children,      type List(Node,Node...), liste des enfants du noeud
        """
        assert type(node_type)==str, "Mauvais type d'argument node_type (str attendu)"
        assert node_type[:3]=="nd_", f"Le node_type n'est pas valide. Il doit commencer par \"nd_\". node_type donné : {node_type} "
        if node_type == "nd_const":
            assert node_value!=None, "L'argument node_value doit avoir une valeur quand node_type == nd_const."
        else:
            assert node_value==None, "L'argument node_value n'est pas censé avoir de valeur en dehors d'un node_type == nd_const."

        if (node_type == "nd_ref" or node_type == "nd_decl"):
            assert node_string!=None, "L'argument node_string doit avoir une valeur quand node_type == nd_ref ou nd_decl."
        else:
            assert node_string==None, f"L'argument node_string n'est pas censé avoir de valeur en dehors d'un node_type == nd_ref ou nd_decl, ici c'est {node_type}."

        assert type(node_pos)==tuple, "Mauvais type d'argument node_pos (tuple attendu)"
        assert len(node_pos)==2, "Argument node_pos pas acceptable. Il doit être en deux dimensions."
        for e in node_pos:
            assert type(e)==int, f"Mauvais type d'argument node_pose à l'indice pour {e} (int attendu)"
            assert e >-1, f"La position ne peut pas être négative. Position donnée : {node_pos}"

        if node_value:
            assert type(node_value)==int, "Mauvais type d'argument node_value (int attendu)"
        if node_string:
            assert type(node_string)==str, "Mauvais type d'argument node_string (str attendu)"
        assert type(node_children)==list or node_children == None, "Mauvais type d'argument children (list attendu)"
        if node_children:
            for c in node_children:
                assert type(c)==Node, f"Mauvais type d'argument children. Type donné : {type(c)}"
        

        self.node_type = node_type
        self.node_pos = node_pos
        self.node_value = node_value
        self.node_string = node_string
        if node_children:
            self.children = node_children
        else:
            self.children = []
        self.index = -1

        all_nodes.append(self)
    
    def __str__(self):
        return f"Node( {self.node_type=} {self.node_pos} {self.node_string=} {self.node_value} {self.index=} )"

    def __repr__(self):
        return self.__str__()