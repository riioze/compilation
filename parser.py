from lexer import *
from node import *

OP = {
    "tok_=" : { "prio" : 1, "parg" : 1, "node_type" : "nd_affect"},
    "tok_||" : { "prio" : 2, "parg" : 3, "node_type" : "nd_or"},
    "tok_&&" : { "prio" : 3, "parg" : 4, "node_type" : "nd_and"},
    "tok_==" : { "prio" : 4, "parg" : 5, "node_type" : "nd_iseq"},
    "tok_!=" : { "prio" : 4, "parg" : 5, "node_type" : "nd_isnoteq"},
    "tok_<=" : { "prio" : 4, "parg" : 5, "node_type" : "nd_isinfeq"},
    "tok_>=" : { "prio" : 4, "parg" : 5, "node_type" : "nd_issupeq"},
    "tok_<" : { "prio" : 4, "parg" : 5, "node_type" : "nd_isinf"},
    "tok_>" : { "prio" : 4, "parg" : 5, "node_type" : "nd_issup"},
    "tok_+" : { "prio" : 5, "parg" : 6, "node_type" : "nd_plus"},
    "tok_-" : { "prio" : 5, "parg" : 6, "node_type" : "nd_minus"},
    "tok_*" : { "prio" : 6, "parg" : 7, "node_type" : "nd_mult"},
    "tok_/" : { "prio" : 6, "parg" : 7, "node_type" : "nd_div"},
    "tok_%" : { "prio" : 6, "parg" : 7, "node_type" : "nd_mod"},
}

def check_op_prio(token_type : str,prio : int) -> bool:
    return token_type in OP.keys() and OP[token_type]["prio"] >= prio

class Symbol:
    def __init__(self, name:str):
        self.name = name
        self.index = -1
    
    def __repr__(self):
        return f"Symbol({self.name=} {self.index=})"

class Parser:

    def __init__(self,lexer:Lexer):
        """ 
        Classe récupérant les tokens un par un et les transforme en noeud pour créer l'arbre représentant le code

        @params:
        Entrée : lexer, type Lexer, objet d'analyse du code pour la transformation en token
        Sortie : None
        """
        self.lexer = lexer

        self.sym_table : List[Symbol] = []
        self.sym_indices_table : List[int] = []
        self.nb_var = 0
        
    
    def next_tree(self) -> Node:
        """ 
        Méthode renvoyant un noeud représentant la prochaine expression

        @params:
        Entrée : None
        Sortie : Node
        """
        tree = self.get_instruction()
        self.nb_var = 0
        self.sem_node(tree)
        return tree
    
    def sem_node(self,node:Node) -> None:
        """
        Analyse sémantique d'un noeud et de ses enfants

        @params:
        Entrée : node, type Node, Noeud dont l'analyse sémantique est faite
        Sortie : None 
        """

        # Vérification du type de noeud, la suite de l'analyse en dépend
        match node.node_type:

            # Type "noeud bloc"
            case "nd_block":
                # Appel à la méthode gérant le commencement d'un nouveau bloc
                self.begin()

                # Analyse des noeuds contenus dans le bloc
                for child in node.children:
                    self.sem_node(child)

                # Appel à la méthode gérant la fin d'un nouveau bloc
                self.end()
            
            # Type "noeud déclaration"
            case "nd_decl":
                # Déclaration d'une variable 
                s = self.declare(node.node_string)

                # Sauvegarde de son indice dans la pile globale
                s.index = self.nb_var

                # Augmentation du nombre de variable
                self.nb_var+=1
            
            # Type "noeud référence"
            case "nd_ref":
                s = self.find(node.node_string)
                assert s.index!=-1
                node.index = s.index
            
            # Type "noeud affection"
            case "nd_affect":
                if node.children[0].node_type != "nd_ref":
                    raise ValueError(f"Waiting identifier at {node.node_pos} before affectation")
                for child in node.children:
                    self.sem_node(child)

            # Cas par défaut, dans le cas d'un noeud loop par exemple
            case default:
                for child in node.children:
                    self.sem_node(child)
    
    def begin(self) -> None:
        """
        Méthode démarrant un contexte quant une '{' est rencontrée
        La table des indices permet de savoir où commence chaque bloc pour délmiter dans la pile de symbole
        quel symbole est dans quel scope

        @params:
        Entrée : None
        Sortie : None
        """

        # Si la table des indices est vide, on ajoute 0 (indice de la fin du scope)
        if self.sym_indices_table == []:
            self.sym_indices_table.append(0)
        else:
            # Si la table des indices des symboles contient quelque chose, duplication de ce nombre
            # pour pouvoir l'augmenter sans le modifier (définition de la fin du scope)
            self.sym_indices_table.append(self.sym_indices_table[-1])
    
    def end(self) -> None:
        """
        Méthode rencontrée à la fin d'un bloc d'instruction pour en sortir

        @params:
        Entrée : None
        Sortie : None
        """

        # Sortie du scope, récupération et suppression de l'indice de la fin de ce dernier
        new_end = self.sym_indices_table.pop()
        
        # Redéfinition de la table des symboles pour enlever les symboles du contexte qui se termine
        # TODO : VERIFIER CETTE LIGNE
        self.sym_table = self.sym_table[:new_end]
    
    def declare(self,name:str) -> Symbol:
        """
        Déclarition d'une variable

        @params:
        Entrée : name, type String, nom de la variable
        Sortie : new_symbol, type Symbol, symbole de la variable
        """
        assert type(name)==str, "L'argument name n'a pas le type attendu (String)."
        
        # Si la table des indices des symboles est vide, il y a une erreur
        if len(self.sym_indices_table) == 0:
            raise ValueError(f"Not in a scope at pos{self.lexer.current_token.token_pos}")
        
        # -----

        # Récupération / Définition des bottom et top pour parcourir la table des symboles du contexte actuel
        # pour vérifier que le nom de la variable qui est définie n'est pas en conflit avec un autre nom (déjà pris)

        # --

        # Dans le cas du contexte général, il n'y a que l'indice de fin dans la liste, attribution du bottom à 0
        elif len(self.sym_indices_table) == 1:
            bottom = 0
            # Récupération de l'indice du haut du contexte
            top = self.sym_indices_table[0]
        
        # Dans le cas d'un contexte aléatoire dans un code, récupération du bottom et du top
        else:
            bottom = self.sym_indices_table[-2]
            top = self.sym_indices_table[-1]
        
        # Regarde dans le contexte courant si on a déjà une variable avec ce nom
        for i in range(bottom,top):
            # Cas problématique
            if self.sym_table[i].name == name:
                # Renvoi d'erreur
                raise ValueError(f"Name {name} at pos {self.lexer.current_token.token_pos} already declared in current scope")
        
        # Création d'un nouveau symbole
        new_symbol = Symbol(name)

        # Ajout dans la table des symboles
        self.sym_table.append(new_symbol)

        # Augmentation de 1 la fin de la pile des indices des symboles
        self.sym_indices_table[-1]+=1

        # Renvoi du symbole tout juste créé représentant la variable
        return new_symbol
    
    
    def find(self,name:str) -> Symbol:
        """
        Méthode renvoyant le symbole recherché s'il est trouvé dans la table des symboles

        @params
        Entrée : name, type String, le nom du symbole à trouver 
        Sortie : self.sym_table[i], type Symbol, le symbole recherché s'il est trouvé
        """

        assert type(name)==str, "L'argument name n'a pas le type attendu (String)."

        top = self.sym_indices_table[-1]-1
        for i in range(top,-1,-1):
            if self.sym_table[i].name == name:
                return self.sym_table[i]
            
        raise ValueError(f"Name {name} at {self.lexer.current_token.token_pos} not declared in current or bigger scope.")
    
    def get_instruction(self) -> Node:
        """
        Méthode permettant de récupérer

        @params:
        Entrée : 
        Sortie :
        """

        if self.lexer.check("tok_debug"):
            intern_expression = self.get_expression()
            self.lexer.accept("tok_;")
            return Node("nd_debug",node_pos=intern_expression.node_pos,node_children=[intern_expression])
        
        elif self.lexer.check("tok_{"):
            block = Node("nd_block",node_pos=self.lexer.last_token.token_pos)
            while(not self.lexer.check("tok_}")):
                block.children.append(self.get_instruction())
            return block
        
        elif self.lexer.check("tok_int"):
            token = self.lexer.current_token
            self.lexer.accept("tok_ident")
            self.lexer.accept("tok_;")
            return Node("nd_decl",token.token_pos,node_string=token.token_string)
        
        elif self.lexer.check("tok_if"):
            if_token = self.lexer.last_token
            self.lexer.accept("tok_(")
            condition_expression = self.get_expression()
            self.lexer.accept("tok_)")
            instruction1 = self.get_instruction()
            cond_node = Node("nd_cond", node_pos=if_token.token_pos,node_children=[condition_expression,instruction1])
            if self.lexer.check("tok_else"):
                instruction2 = self.get_instruction()
                cond_node.children.append(instruction2)
            return cond_node
        
        elif self.lexer.check("tok_while"):
            while_token = self.lexer.last_token
            self.lexer.accept("tok_(")
            condition = self.get_expression()
            self.lexer.accept("tok_)")
            instruction = self.get_instruction()

            loop_node = Node("nd_loop",node_pos=while_token.token_pos)
            target_node = Node("nd_target",node_pos=while_token.token_pos)
            cond_node = Node("nd_cond",node_pos=while_token.token_pos)
            break_node = Node("nd_break",node_pos=while_token.token_pos)
           
            loop_node.children.append(target_node)
            loop_node.children.append(cond_node)

            cond_node.children.append(condition)
            cond_node.children.append(instruction)
            cond_node.children.append(break_node)
            return loop_node
        
        elif self.lexer.check("tok_do"):
            instruction = self.get_instruction()
            self.lexer.accept("tok_while")
            while_token = self.lexer.last_token
            self.lexer.accept("tok_(")
            condition = self.get_expression()
            self.lexer.accept("tok_)")
            self.lexer.accept("tok_;")

            loop_node = Node("nd_loop",node_pos=while_token.token_pos)
            target_node = Node("nd_target",node_pos=while_token.token_pos)
            cond_node = Node("nd_cond",node_pos=while_token.token_pos)
            break_node = Node("nd_break",node_pos=while_token.token_pos)
            continue_node = Node("nd_continue",node_pos=while_token.token_pos)

            loop_node.children.append(target_node)
            loop_node.children.append(instruction)
            loop_node.children.append(cond_node)

            cond_node.children.append(condition)
            cond_node.children.append(continue_node)
            cond_node.children.append(break_node)
            return loop_node

        elif self.lexer.check("tok_for"):

            for_tok = self.lexer.last_token

            self.lexer.accept("tok_(")
            init_expression = self.get_expression()
            self.lexer.accept("tok_;")
            cond_expression = self.get_expression()
            self.lexer.accept("tok_;")
            step_expression = self.get_expression()
            self.lexer.accept("tok_)")

            instruction = self.get_instruction()

            global_seq_node = Node("nd_seq",node_pos=for_tok.token_pos)

            init_instruction = Node("nd_drop",node_pos=init_expression.node_pos,node_children=[init_expression])

            loop_node = Node("nd_loop",node_pos=for_tok.token_pos)

            restart_seq = Node("nd_seq",node_pos=for_tok.token_pos)

            target_instruction = Node("nd_target",node_pos=for_tok.token_pos)
            step_instruction = Node("nd_drop",step_expression.node_pos,node_children=[step_expression])

            break_instruction = Node("nd_break",node_pos=for_tok.token_pos)

            cond_instruction = Node("nd_cond",node_pos=for_tok.token_pos)

            restart_seq.children.append(instruction)
            restart_seq.children.append(target_instruction)
            restart_seq.children.append(step_instruction)

            cond_instruction.children.append(cond_expression)
            cond_instruction.children.append(restart_seq)
            cond_instruction.children.append(break_instruction)

            loop_node.children.append(cond_instruction)

            global_seq_node.children.append(init_instruction)
            global_seq_node.children.append(loop_node)

            return global_seq_node

        else:
            intern_expression = self.get_expression()
            self.lexer.accept("tok_;")
            return Node("nd_drop",node_pos=intern_expression.node_pos,node_children=[intern_expression])


    def get_expression(self, prio: int = 0) -> Node:
        """ 
        Méthode renvoyant un noeud représentant une expression complète

        @params:
        Entrée : None
        Sortie : Node
        """
        assert type(prio)==int, "Mauvais type de priorité (int attendu)"

        first_part = self.get_prefix()

        while check_op_prio(self.lexer.current_token.token_type, prio):
            op_token = self.lexer.current_token
            self.lexer.next_token()
            second_part = self.get_expression(OP[op_token.token_type]["parg"])
            first_part = Node(OP[op_token.token_type]["node_type"],node_pos=op_token.token_pos,node_children=[first_part,second_part])
        return first_part

    def get_suffix(self) -> Node:
        """ 
        Méthode renvoyant un noeud opérateur suffixe (appel de fonction, indexation) avec comme enfant le reste de l'expression

        @params
        Entrée : None
        Sortie : Node
        """

        return self.get_atom()

    def get_prefix(self) -> Node:
        """ 
        Méthode renvoyant un noeud opérateur préfixe (!, -, +, *, &) avec comme enfant le reste de l'expression

        @params
        Entrée : None
        Sortie : Node
        """

        # Parcours en fonction du préfixe
        if self.lexer.check("tok_!"):

            # Récupération du dernier token rencontré ( tok_! )
            token_not = self.lexer.last_token
            
            # Récupération du reste de l'expression en se rappelant elle-même
            intern_prefix = self.get_prefix()

            # Création d'un noeud correspondant au token
            node_not = Node("nd_not",node_pos=token_not.token_pos,node_children=[intern_prefix])

            # Renvoi du noeud
            return node_not
        
        elif self.lexer.check("tok_-"):

            # Récupération du dernier token rencontré ( tok_- )
            token_neg = self.lexer.last_token

            # Récupération du reste de l'expression en se rappelant elle-même
            intern_prefix = self.get_prefix()

            # Création d'un noeud correspondant au token
            node_neg = Node("nd_neg",node_pos=token_neg.token_pos,node_children=[intern_prefix])

            # Renvoi du noeud
            return node_neg
        
        elif self.lexer.check("tok_+"):
            # Préfix + inutile (comme dans "+5", suppression du "+" inutile)
            return self.get_prefix()
        
        else:
            # Lorsqu'on rencontre quelque chose de différent des préfixes définis, renvoi en tant que suffixe
            return self.get_suffix()

    def get_atom(self) -> Node:
        """ 
        Méthode renvoyant un noeud atome (constante numérique ou une expression entre parenthèse) 

        @params
        Entrée : None
        Sortie : Node
        """

        # Parcours en fonction du token rencontré
        if self.lexer.check("tok_const"):

            # Récupération du dernier token ( tok_const )
            token = self.lexer.last_token

            # Renvoi du noeud correspondant au token
            return Node("nd_const",node_pos=token.token_pos,node_value=token.token_value,node_children=[])

        elif self.lexer.check("tok_("):

            # Récupération de l'expression parenthésée
            expression = self.get_expression()

            # Vérification de la fermeture de l'expression par une parenthèse fermante
            self.lexer.accept("tok_)")

            # Renvoi de l'expression
            return expression

        elif self.lexer.check("tok_ident"):

            token = self.lexer.last_token

            return Node("nd_ref",node_pos=token.token_pos,node_string=token.token_string)
        
        else:
            # Token non accepté dans la grammaire régissant ce modèle atome, renvoi d'une erreur
            raise ValueError(f"error at pos {self.lexer.current_token.token_pos}, expected const or expression")

    
