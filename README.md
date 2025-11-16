# Projet de compilation

## pour compiler

le code est lu par l'entrée standard et l'eembleur est sorti par la sortie standard de [main.py](main.py).

Toutefois c'est possible de changer les fichier in et out dans la fonction ```main()``` cd [main.py](main.py)

## les test
les fichier .c de test sont dans [tests](tests)

Ici on a utilisé pytest pour lancer le fichier qui contient tous les tests [test_compiler.py](test_compiler.py)

```sh
pytest
```

## Le code
### tokenizer->analyseur syntaxique

le tokenizer et analyseur syntaxique se trouve dans [lexer.py](lexer.py) 
