from tokens import *

class Lexer:
    def __init__(self, text:str):
        """ 
        Méthode d'initialisation de la classe

        @params
        Entrée : text, type String, code à compiler
        Sortie : None
        """
        assert type(text)==str, "Mauvais type d'argument text (str attendu)"

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
            "recv"
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
        assert type(character)==str, "Mauvais type d'argument character (str attendu)"

        return ord('0' ) <= ord(character) <= ord('9')
    
    def is_letter(self,character:str):
        """
        Renvoie si le caractère étudié est une lettre ou non en utilisant la table ASCII
        
        @params
        Entrée : character, type string, caractère du code rencontré
        Sortie : Boolean, résultat de la comparaison
        """
        assert type(character)==str, "Mauvais type d'argument character (str attendu)"

        return (ord('A') <= ord(character) <= ord('Z')) or (ord('a') <= ord(character) <= ord('z'))
    
    def is_alpha_num(self,character:str):
        """
        Renvoie si le caractère étudié est alphanumérique la méthode is_number et is_letter
        
        @params
        Entrée : character, type string, caractère du code rencontré
        Sortie : Boolean, résultat de la comparaison
        """
        assert type(character)==str, "Mauvais type d'argument character (str attendu)"

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
                    self.pointer_pos+=1
                    self.current_col+=1
                else:
                    self.current_token = Token("tok_&",(self.current_line,self.current_col))
            
            case '|':
                # Le token '|' n'existe pas, vérification de la présence de '||'
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '|':
                    self.current_token = Token("tok_||",(self.current_line,self.current_col))
                    self.pointer_pos+=1
                    self.current_col+=1
                else:
                    raise ValueError(f"Token | unkown at pos (line = {self.current_line} col = {self.current_col}) did you mean \"||\" ?")
            
            case '!':
                # Distinction entre '!' et '!='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_!=",(self.current_line,self.current_col))
                    self.pointer_pos+=1
                    self.current_col+=1
                else:
                    self.current_token = Token("tok_!",(self.current_line,self.current_col))
            
            case '=':
                # Distinction entre '=' et '=='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_==",(self.current_line,self.current_col))
                    self.pointer_pos+=1
                    self.current_col+=1
                else:
                    self.current_token = Token("tok_=",(self.current_line,self.current_col))

            case '<':
                # Distinction entre '<' et '<='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_<=",(self.current_line,self.current_col))
                    self.pointer_pos+=1
                    self.current_col+=1
                else:
                    self.current_token = Token("tok_<",(self.current_line,self.current_col))

            case '>':
                # Distinction entre '>' et '>='
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_>=",(self.current_line,self.current_col))
                    self.pointer_pos+=1
                    self.current_col+=1
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
        assert type(token_type)==str, "Mauvais type d'argument token_type (str attendu)"

        if not self.check(token_type):
            line, col = self.current_token.token_pos
            raise ValueError(f"wrong token at pos ({line = } {col = }) expected a token of type {token_type}, got {self.current_token}")

    def check(self, token_type:str):
        """
        Vérification du type du current_token par rapport au type fourni en argument.
        Si le type est le bon, appel à next_token() pour trouver le token d'avant,
        renvoi de 'True'
        Si le type du current_token n'est pas le bon, 'False' est renvoyé

        @params
        Entrée : token_type, type string, type du token 
        Sortie : Boolean, résultat de la comparaison
        """
        assert type(token_type)==str, "Mauvais type d'argument token_type (str attendu)"

        if self.current_token.token_type == token_type:
            self.next_token()
            return True
        return False