from typing import Optional, Tuple, List


class Token:
    def __init__(self, token_type:str, token_pos:Tuple[int,int], token_value:Optional[int]=None, token_string:Optional[str]=None):
        """ 
        Classe représentant les objets Token utilisés par la suite

        @params
        Entrée : t_type,    type String, le type du token
                 t_value,   type Int,    la valeur du token lorsqu'il représente une constante numérique (optionnel)
                 t_string,  type String, la valeur du token lorsqu'il représente une contante alphabétique ou une variable (optionnel)
                 t_pos,     type Tuple(ligne:int, colonne:int), la position du token dans le code
        Sortie : None
        """
        assert type(token_type)==str, "Mauvais type d'argument node_type (str attendu)"
        assert type(token_pos)==tuple, "Mauvais type d'argument node_pos (tuple attendu)"
        for e in token_pos:
            assert type(e)==int, f"Mauvais type d'argument node_pose à l'indice pour {e} (int attendu)"
        if token_value:
            assert type(token_value)==int, "Mauvais type d'argument node_value (int attendu)"
        if token_string:
            assert type(token_string)==str, "Mauvais type d'argument node_string (str attendu)"
        
        self.token_type = token_type
        self.token_value = token_value
        self.token_string = token_string
        self.token_pos = token_pos

    def __str__(self):
        """
        Méthode d'affichage de l'object

        @params:
        Entrée : None
        Sortie :None
        """
        string = self.token_type + f" at ({self.token_pos})"

        if self.token_value:
            string += f" with value : {self.token_value}"
        if self.token_string:
            string += f" with string : {self.token_string}"
    
        return string