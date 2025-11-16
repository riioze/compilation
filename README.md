# Projet de compilation

## pour compiler

le code est lu par l'entrée standard et l'assembleur est sorti par la sortie standard de [main.py](main.py).

Toutefois c'est possible de changer les fichier in et out dans la fonction ```main()``` cd [main.py](main.py)

## les test
les fichier .c de test sont dans [tests](tests)

Ici on a utilisé pytest pour lancer le fichier qui contient tous les tests [test_compiler.py](test_compiler.py)

```sh
pytest
```

## Le code
### tokenizer->analyseur syntaxique

Le tokenizer et analyseur syntaxique se trouve dans [lexer.py](lexer.py) avec la classe ```Lexer``` qui s'occupe de récupérer les tokens un par un.

### parser
L'analyseur sémantique de trouve dans [parser.py](parser.py), il récupère les tokens un par un afin de créer des expressions instructions atoms ect

### optimiseur
l'optimiseur dans [optimizer.py](optimizer.py) ne fait rien et renvoie juste les noeud qu'il reçoit.

### gen_code
La génération du code se fait dans [code_gen.py](code_gen.py) et transforme les noeuds en code pour la machine msm

### Le main
[main.py](main.py) s'occupe de faire le chef d'orchestre.

### la std
[std.c](std.c) contient les quelques fontions de notre "librairie standard" (malloc print println) elle est automatiquement incluse par le main
