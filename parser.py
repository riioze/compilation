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
    def __init__(self, name:str,sym_type="int"):
        self.name = name
        self.index = -1
        self.type_ = sym_type
    
    def __repr__(self):
        return f"Symbol({self.name=} {self.type_} {self.index=})"

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
        
    
    def next_tree(self):
        """ 
        Méthode renvoyant un noeud représentant la prochaine expression

        @params:
        Entrée : None
        Sortie : Node
        """
        tree = self.get_function()
        self.nb_var = 0
        self.sem_node(tree)
        return tree
    
    def sem_nodes_children(self,node:Node):
        for child in node.children:
            self.sem_node(child)

    def sem_node(self,node:Node):

        match node.node_type:
            case "nd_block":
                self.begin()
                self.sem_nodes_children(node)
                self.end()
            
            case "nd_decl":
                s = self.declare(node.node_string)
                s.index = self.nb_var
                node.index = s.index
                self.nb_var+=1
            
            case "nd_ref":
                s = self.find(node.node_string)
                if (s.type_ != "func"):
                    assert s.index!=-1
                node.index = s.index
            
            case "nd_affect":
                if node.children[0].node_type not in ["nd_ref","nd_ind"]:
                    raise ValueError(f"Waiting identifier at {node.node_pos} before affectation")
                self.sem_nodes_children(node)

            case "nd_call":
                self.sem_nodes_children(node)
                func_node = node.children[0]
                if (func_node.node_type != "nd_ref" or self.find(func_node.node_string).type_ != "func"):
                    raise ValueError(f"Can't call ({node.node_type} {node.node_string}) as a func")

            case "nd_func" :
                self.declare(node.node_string,sym_type="func")
                
                self.nb_var = 0
                self.begin()
                self.sem_nodes_children(node)
                self.end()
                node.node_value = self.nb_var

            case default:
                self.sem_nodes_children(node)

    
    def begin(self):
        if self.sym_indices_table == []:
            self.sym_indices_table.append(0)
        else:
            self.sym_indices_table.append(self.sym_indices_table[-1])
    
    def end(self):
        previous_end = self.sym_indices_table.pop()
        if self.sym_indices_table != []:
            new_end = self.sym_indices_table[-1]
            self.sym_table = self.sym_table[:new_end]
    
    def declare(self,name:str,sym_type = "int"):
        assert type(name)==str, "L'argument name n'a pas le type attendu (String)."
        if len(self.sym_indices_table) == 0:
            raise ValueError(f"Not in a scope at pos{self.lexer.current_token.token_pos}")
        elif len(self.sym_indices_table) == 1:
            bottom = 0
            top = self.sym_indices_table[0]
        else:
            bottom = self.sym_indices_table[-2]
            top = self.sym_indices_table[-1]
        
        for i in range(bottom,top):
            if self.sym_table[i].name == name:
                raise ValueError(f"Name {name} at pos {self.lexer.current_token.token_pos} already declared in current scope")
        
        new_symbol = Symbol(name,sym_type)
        self.sym_table.append(new_symbol)
        self.sym_indices_table[-1]+=1
        return new_symbol
    
    def find(self,name:str):
        assert type(name)==str, "L'argument name n'a pas le type attendu (String)."
        top = self.sym_indices_table[-1]-1
        for i in range(top,-1,-1):
            if self.sym_table[i].name == name:
                return self.sym_table[i]
        print(self.sym_table)
        raise ValueError(f"Name {name} at {self.lexer.current_token.token_pos} not declared in current or bigger scope.")
    
    def get_function(self) -> Node:

        self.lexer.accept("tok_int")
        while self.lexer.check("tok_*"):pass # retire les * "inutiles"
        self.lexer.accept("tok_ident")
        identifier_tok = self.lexer.last_token
        self.lexer.accept("tok_(")

        function_node = Node("nd_func",node_pos=identifier_tok.token_pos,node_string=identifier_tok.token_string)

        if not self.lexer.check("tok_)"):
            while True: # Do

                self.lexer.accept("tok_int")
                self.lexer.accept("tok_ident")
                arg_tok = self.lexer.last_token
                function_node.children.append(Node("nd_decl",node_pos=arg_tok.token_pos,node_string=arg_tok.token_string))

                if not self.lexer.check("tok_,"): # while
                    break
            self.lexer.accept("tok_)")
        function_body = self.get_instruction()

        assert function_body.node_type == "nd_block", f"Must have a block, got {function_body.node_type}"

        function_node.children.append(function_body)

        return function_node

    def get_instruction(self) -> Node:

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
            

            while(self.lexer.check("tok_*")):pass

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

        if self.lexer.check("tok_return"):
            pos = self.lexer.last_token.token_pos
            expression = self.get_expression()
            self.lexer.accept("tok_;")
            return Node("nd_return",node_pos = pos,node_children=[expression])

        if self.lexer.check("tok_send"):
            intern_expression = self.get_expression()
            self.lexer.accept("tok_;")
            return Node("nd_send",node_pos=self.lexer.last_token.token_pos,node_children=[intern_expression])

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
        print(self.lexer.last_token)
        atom = self.get_atom()

        if self.lexer.check("tok_("):
            call_node = Node("nd_call",node_pos=atom.node_pos,node_children=[atom])

            if not self.lexer.check("tok_)"):
                while True: #do
                    call_node.children.append(self.get_expression())
                    if not self.lexer.check("tok_,"):
                        break
                self.lexer.accept("tok_)")
            
            return call_node
        
        else:
            return atom



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
        
        elif self.lexer.check("tok_*"):
            return Node("nd_ind",node_pos=self.lexer.last_token.token_pos,node_children=[self.get_prefix()])
        
        elif self.lexer.check("tok_&"):
            return Node("nd_adr",node_pos=self.lexer.last_token.token_pos,node_children=[self.get_prefix()])

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
        
        elif self.lexer.check("tok_recv"):

            return Node("nd_recv",node_pos=self.lexer.last_token.token_pos)

        else:
            # Token non accepté dans la grammaire régissant ce modèle atome, renvoi d'une erreur
            raise ValueError(f"error at pos {self.lexer.current_token.token_pos}, expected const or expression")

    
