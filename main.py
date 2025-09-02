from typing import Optional, Tuple, List


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

class Token:
    def __init__(self, t_type:str, t_value:Optional[int]=None, t_string:Optional[str]=None, t_pos:Tuple[int,int]=None):
        """ 
        Classe représentant les objets Token utilisés par la suite

        @params
        Entrée : t_type,    type String, le type du token
                 t_value,   type Int,    la valeur du token lorsqu'il représente une constante numérique (optionnel)
                 t_string,  type String, la valeur du token lorsqu'il représente une contante alphabétique ou une variable (optionnel)
                 t_pos,     type Tuple(ligne:int, colonne:int), la position du token dans le code
        Sortie : None
        """
        self.token_type = t_type
        self.token_value = t_value
        self.token_string = t_string
        self.token_pos = t_pos

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


class Node:
     
    def __init__(self, node_type:str,node_pos: Tuple[int,int], node_value : Optional[int] = None, node_string: Optional[str] = None, children: List['Node'] = []):
        """ 
        Classe représentant les objets Noeud (Node) pour la construction d'arbre dans le but de gérer le code dans le bon ordre

        @params
        Entrée : node_type,     type String, type du noeud
                 node_pos,      type Tuple(ligne:int, colonne:int), position du noeud dans le code
                 node_value,    type Int, valeur du noeud quand c'est une constante numérique (optionnel)
                 node_string,   type String, valeur du noeud quand c'est une constante alphabétique (optionnel)
                 children,      type List(Node,Node...), liste des enfants du noeud
        """
        self.node_type = node_type
        self.node_pos = node_pos
        self.node_value = node_value
        self.node_string = node_string
        self.children = children


class Lexer:
    def __init__(self, text:str):
        """ 
        Méthode d'initialisation de la classe

        @params
        Entrée : text, type String, code à compiler
        Sortie : None
        """
        self.pointer_pos : int = 0
        self.current_line : int = 0
        self.current_col : int = 0

        self.current_token = Token("tok_start",(-1,-1))
        self.last_token = Token("tok_start",(-1,-1))

        self.spacing_chars = [' ', '\t', '\n']

        self.keywords = [
            "int",
            "void",
            "return",
            "if",
            "else",
            "for",
            "do",
            "while",
            "break",
            "continue",
            "debug",
            "send",
            "rec"
        ]

        self.text = text
    
    # -----
    # Vérification de position du curseur
    # -----
    def test_eof(self):
        """ 
        Renvoi de l'égalité entre la position du pointeur parcourant le code 
        et la longueur du code

        S'ils sont égaux, alors le code a fini d'être parcouru

        @params
        Entrée : None
        Sortie : None
        """
        return self.pointer_pos == len(self.text)
            
    def eof_tok(self):
        """ 
        Création du token 'End Of File', signifiant que le curseur est après le 
        dernier caratère du code, il a donc fini d'être parcouru

        @params
        Entrée : None
        Sortie : Token, le token eof
        """
        return Token("tok_eof",(self.current_line,self.current_col))
    
    # -----
    # Vérification du type de caratère rencontré
    # -----
    def is_number(self, character:str):
        """
        Renvoie si le caractère étudié est un chiffre ou non en utilisant la table ASCII
        
        @params
        Entrée : character, type string, caractère du code rencontré
        Sortie : Boolean, résultat de la comparaison
        """
        return ord('0' ) <= ord(character) <= ord('9')
    
    def is_letter(self,character:str):
        """
        Renvoie si le caractère étudié est une lettre ou non en utilisant la table ASCII
        
        @params
        Entrée : character, type string, caractère du code rencontré
        Sortie : Boolean, résultat de la comparaison
        """
        return (ord('A') <= ord(character) <= ord('Z')) or (ord('a') <= ord(character) <= ord('z'))
    
    def is_alpha_num(self,character:str):
        """
        Renvoie si le caractère étudié est alphanumérique la méthode is_number et is_letter
        
        @params
        Entrée : character, type string, caractère du code rencontré
        Sortie : Boolean, résultat de la comparaison
        """
        return self.is_number(character) or self.is_letter(character)
    
    # -----
    # Parcours du code dans le but de trouver le token suivant
    # -----

    def next_token(self):
        """
        La fonction next_token recherche dans le code à compiler le prochain token en faisant
        avancer le pointeur le parcourant.

        La fonction commence par mettre à jour les token, passe les différents espace puis
        convertit les caratères rencontrés en token.

        @params
        Entrée : None
        Sortie : None
        """
        
        # Actualisation des tokens
        self.last_token = self.current_token

        # Vérification de la position du curseur par rapport à la fin du code
        if self.test_eof():
            # Si le code a été entièrement parcouru, le token passe en end of file
            self.current_token = self.eof_tok()
            # Arret de la méthode
            return

        # ---
        # Gestion des espaces et retour à la ligne
        # ---

        # TODO: ajouter la gestion des commentaires

        while (self.text[self.pointer_pos] in self.spacing_chars): # skipping spaces
            
            # Augmentation de l'indice à regarder
            self.pointer_pos += 1

            # S'il a dépassé la fin du code, token end of file et arret
            if self.test_eof():
                self.current_token = self.eof_tok()

                # Une fois le token eof créé, on sort de la fonction
                return

            # Mise à jour de la position du curseur
            self.current_col += 1
            if self.text[self.pointer_pos] == '\n':
                self.current_col = 0
                self.current_line+=1
        
        # ---
        # Le pointeur rencontre des caractères, attribution de token
        # ---

        # Rencontre de chiffre/nombre
        if self.is_number(self.text[self.pointer_pos]): # parse full number

            # Création du nombre
            current_number = ''

            # Ajout de chaque chiffre du nombre caractère par caractère          
            while not self.test_eof() and self.is_number(self.text[self.pointer_pos]):
                current_number += self.text[self.pointer_pos]
                self.pointer_pos+=1
                
            # Le nombre est complet, création de token
            self.current_token = Token("tok_const",(self.current_line,self.current_col),token_value=int(current_number))
            
            # Le token a été trouvé, arret de la méthode
            return

        # Rencontre de lettre/mot
        if self.is_letter(self.text[self.pointer_pos]):

            # Création du mot
            current_word = ''

            # Tant que le pointeur n'est pas à la fin du code et qu'il rencontre des caratères
            while not self.test_eof() and self.is_alpha_num(self.text[self.pointer_pos]): # ici on utilise is_alpha_num car un identifiant ne peut pas commencer par une lettre mais il peut en avoir ensuite
                # Ajout de la lettre ou du chiffre au mot
                current_word += self.text[self.pointer_pos]

                self.pointer_pos+=1

            # Vérification de la présence du mot dans les mots clefs réservés
            if current_word in self.keywords:
                # Création du token particulier réservé au mot-clef
                self.current_token = Token("tok_"+current_word,(self.current_line,self.current_col),token_string=current_word)
            else:
                # Création d'un token d'identification
                self.current_token = Token("tok_ident",(self.current_line,self.current_col),token_string=current_word)
            
            # Token trouvé, arret de la méthode
            return
        
        # ---
        # Si le caractère rencontré est un token en lui-même, renvoi du token correspondant
        # ---
        match self.text[self.pointer_pos]:
            case '+':
                self.current_token = Token("tok_+",(self.current_line,self.current_col))

            case '-':
                self.current_token = Token("tok_-",(self.current_line,self.current_col))

            case '*':
                self.current_token = Token("tok_*",(self.current_line,self.current_col))

            case '/':
                self.current_token = Token("tok_/",(self.current_line,self.current_col))

            case '%':
                self.current_token = Token("tok_%",(self.current_line,self.current_col))
            
            case '&':
                # Distinction entre '&' et '&&'
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '&':
                    self.current_token = Token("tok_&&",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_&",(self.current_line,self.current_col))
            
            case '|':
                # Le token '|' n'existe pas, vérification de la présence de '||'
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '|':
                    self.current_token = Token("tok_||",(self.current_line,self.current_col))
                else:
                    raise ValueError(f"Token | unkown at pos (line = {self.current_line} col = {self.current_col}) did you mean \"||\" ?")
            
            case '!':
                # Distinction entre '!' et '!='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_!=",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_!",(self.current_line,self.current_col))
            
            case '=':
                # Distinction entre '=' et '=='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_==",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_=",(self.current_line,self.current_col))

            case '<':
                # Distinction entre '<' et '<='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_<=",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_<",(self.current_line,self.current_col))

            case '>':
                # Distinction entre '>' et '>='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_>=",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_<",(self.current_line,self.current_col))

            case '(':
                self.current_token = Token("tok_(",(self.current_line,self.current_col))

            case ')':
                self.current_token = Token("tok_)",(self.current_line,self.current_col))

            case '[':
                self.current_token = Token("tok_[",(self.current_line,self.current_col))

            case ']':
                self.current_token = Token("tok_]",(self.current_line,self.current_col))

            case '{':
                self.current_token = Token("tok_{",(self.current_line,self.current_col))

            case '}':
                self.current_token = Token("tok_}",(self.current_line,self.current_col))

            case ';':
                self.current_token = Token("tok_;",(self.current_line,self.current_col))

            case ',':
                self.current_token = Token("tok_,",(self.current_line,self.current_col))

            case other: # si token inconnue, on envoie une erreur
                raise ValueError(f"Token {other} unkown at pos (line = {self.current_line} col = {self.current_col})")
        self.pointer_pos+=1
    
    def accept(self,token_type:str):
        """
        Vérification du type du current_token par rapport au type fourni en argument.
        Si le type du current_token n'est pas le bon, un message d'erreur est envoyé

        @params
        Entrée : token_type, type string, type du token 
        Sortie : None
        """
        if not self.check(token_type):
            line, col = self.current_token.token_pos
            raise ValueError(f"wrong token at pos ({line = } {col = }) expected a token of type {token_type}")

    def check(self,token_type:str):
        """
        Vérification du type du current_token par rapport au type fourni en argument.
        Si le type est le bon, appel à next_token() pour trouver la token d'avant,
        renvoi de 'True'
        Si le type du current_token n'est pas le bon, 'False' est renvoyé

        @params
        Entrée : token_type, type string, type du token 
        Sortie : Boolean, résultat de la comparaison
        """
        if self.current_token.token_type == token_type:
            self.next_token()
            return True
        return False
                
class Parser:

    def __init__(self,lexer:Lexer):
        """ 
        Classe récupérant les tokens un par un et les transforme en noeud pour créer l'arbre représentant le code

        @params:
        Entrée : lexer, type Lexer, objet d'analyse du code pour la transformation en token
        Sortie : None
        """
        self.lexer = lexer
        
    
    def next_tree(self):
        """ 
        Méthode renvoyant un noeud représentant la prochaine expression

        @params:
        Entrée : None
        Sortie : Node
        """
        return self.get_expression()


# Node *E(int prio = 0) {
#     N = P(); # première partie de l'expression
#     while (OP_BIN[T.Type] != NULL) and  (OP[T.Type].prio >= prio) { # Test si c'est op binaire qui respecte la priorité
#         op = T.type;
#         next();
#         M = E(tbl[op].parg); # suite : aller manger ce qui est de priorité supérieur a l'op courant
#         N = node2(op, N, M);
#     }
#     return N;
# }

    def get_expression(self, prio: int = 0) -> Node:
        """ 
        Méthode renvoyant un noeud représentant une expression complète

        @params:
        Entrée : None
        Sortie : Node
        """
        first_part = self.get_prefix()

        while check_op_prio(self.lexer.current_token.token_type, prio):
            op_token = self.lexer.current_token
            self.lexer.next_token()
            second_part = self.get_expression(OP[op_token.token_type]["parg"])
            first_part = Node(OP[op_token.token_type]["node_type"],node_pos=op_token.token_pos,children=[first_part,second_part])
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
            node_not = Node("nd_not",node_pos=token_not.token_pos,children=[intern_prefix])

            # Renvoi du noeud
            return node_not
        
        elif self.lexer.check("tok_-"):

            # Récupération du dernier token rencontré ( tok_- )
            token_neg = self.lexer.last_token

            # Récupération du reste de l'expression en se rappelant elle-même
            intern_prefix = self.get_prefix()

            # Création d'un noeud correspondant au token
            node_neg = Node("nd_neg",node_pos=token_neg.token_pos,children=[intern_prefix])

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
            return Node("nd_const",node_pos=token.token_pos,node_value=token.token_value)

        elif self.lexer.check("tok_("):

            # Récupération de l'expression parenthésée
            expression = self.get_expression()

            # Vérification de la fermeture de l'expression par une parenthèse fermante
            self.lexer.accept("tok_)")

            # Renvoi de l'expression
            return expression
        
        else:
            # Token non accepté dans la grammaire régissant ce modèle atome, renvoi d'une erreur
            raise ValueError(f"error at pos {self.lexer.current_token.token_pos}, expected const of expression")

    

class Optimizer:
    def __init__(self,parser:Parser):
        self.parser = parser
    
    def next_tree(self):
        return self.parser.next_tree()

def gencode(optimizer:Optimizer,file):
    tree = optimizer.next_tree()
    gennode(tree,file)

def gennode(node:Node,file):
    
    match node.node_type:
        case "nd_const":
            print(f"push {node.node_value}",file=file)

        case "nd_not":
            assert len(node.children) == 1, f"node nd_not at pos {node.node_pos} has not the required number of children (1)"
            gennode(node.children[0],file)
            print("not",file=file)
        
        case "nd_neg":
           assert len(node.children) == 1, f"node nd_not at pos {node.node_pos} has not the required number of children (1)"
           print("push 0",file=file)
           gennode(node.children[0],file)
           print("sub", file=file)
        
        case other:
            raise ValueError(f"node_type {other} at pos {node.node_pos} unknown")



        
def main():
    with open("code.c", 'r') as f:
        code = f.read()
    
    lexer = Lexer(code)
    lexer.next_token()
    parser = Parser(lexer)
    optimizer = Optimizer(parser)

    with open("msm/prg.asm",'w') as file:

        

        print(".start",file=file)

        while(lexer.current_token.token_type != "tok_eof"):
            gencode(optimizer,file=file)

        print("dbg",file=file)
        print("halt",file=file)





if __name__ == "__main__":
    main()