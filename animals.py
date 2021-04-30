# Importation du module json qui permet a python d'intéragir correctement avec un fichier JSON, je m'en sert pour charger et sauvegarder la progression.
import json

animals = {}

# Localisation du fichier de sauvegarde des connaissances.
fichierSauvegarde = "arbre.json"

# Fonction principale qui démarre le jeu.
def main():
    animals = readFile(fichierSauvegarde)

    print("Bonjour, voulez vous jouer au jeu des animaux ? \n Mon but est de deviner a quel animal vous pensez, il est possible que je ne le connaisse pas mais dans ce cas vous pouvez me l'apprendre !")
    print("Je sauvegarde toute ma mémoire dans un fichier externe pour que si vous jouez en plusieurs fois, je me rappelle de la session précédente !")
    print("Je sauvegarderais la progression quand vous refuserez de lancer la partie")
    print("Merci de ne pas utiliser d'accents !!")
  
    while isYes(input("Voulez vous jouer ?\n O/N (N=Quitter et Sauvegarder)\n")):
        walkTree(animals)
    # Fin de partie = Fin de la boucle while et donc la sauvegarde de la progression dans le fichier JSON, noter que la sauvegarde n'est importante que si le jeu est quitté et relancé, une variable s'occupe
    # de la mémoire au cours de la session de jeu.
    updateFile(fichierSauvegarde, animals)

# Fonction qui sert a naviguer dans l'arbre, elle détecte aussi si la partie est sur le point d'être terminée
# Le premier argument est la partie actuellement explorée car les autres ont été écartées.
def walkTree(branche:dict):
    direction = askYesNo(branche["question"])
    nouvelbranche = descendre(branche, direction)

    if foundAnimal(nouvelbranche):
        endGame(nouvelbranche, branche, direction)
    else:
        # Récursivité pour explorer tout l'arbre.
        walkTree(nouvelbranche)

# Prends en premier argument une dicte qui correspond a la dicte à explorer.
# Prends en second argument un booléen qui correspond a la réponse de l'utilisateur.
# Si l'utilisateur a répondu positivement a la question, il renvoie la partie "yes" de la branche et la partie "non" si il a répondu autrement.
# la fonction renvoie la partie de la racine qui corresponds.
def descendre(branche:dict, direction:bool):
    if direction:
        return(branche["yes"])
    else:
        return(branche["no"])

# Vérifie si la branche est arrivée au bout en vérifiant si la branche est bien toujours de type dict, si ce n'est pas le cas, on peut terminer le jeu avec la question finale.
def foundAnimal(branche:dict):
    return(not isinstance(branche, dict))

# Fonction qui termine la partie.
# Elle prends en premier argument un dictionnaire qui est la branche actuelle
# En second argument un dictionnaire qui est l'ancienne branche sur laquelle nous étions afin de savoir ou stocker le nouvel animal en cas de victoire du joueur.
# En troisième et dernier argument un booléen qui indique la direction correspondant a la réponse du joueur (oui ou non).
def endGame(branche:dict, parent:dict, direction:bool):
    if askYesNo("Votre animal est-il " + branche + "?"):
        print("J'ai gagné.")
    else:
        stockernouvelAnimal(parent, whichSide(direction), branche)

# Fonction qui traduit un booléen en réponse pour naviguer sur l'arbre
# traduit True en "yes" (str) et False en "no" (str)
def whichSide(reponse:bool):
    if reponse:
        return("yes")
    else:
        return("no")

# Cette fonction n'est appellée qu'en cas de victoire du joueur, elle l'annonce, demande a quoi le joueur pensait,
# elle pose une question pour savoir comment identifier le nouvel animal et le différencier de celui proposé par l'ordinateur.
def stockernouvelAnimal(brancheaudessus:dict, side:str, ancienAnimal:str):
    print("Vous avez gagné, ", end="")
    print("à quoi pensiez vous ?")
    nouvelAnimal = input().lower()
        
    print("Quelle question pourrais-je poser pour faire la différence entre ", ancienAnimal, " et ", nouvelAnimal, " ?")
    nouvelQuestion = input()
        
    brancheaudessus[side] = {
        "question": MettreEnQuestion(nouvelQuestion),
        "yes": nouvelAnimal,
        "no": ancienAnimal
    }

# Prends un string en premier argument, s'assure qu'il y a bien " ?" a la fin de la question.
# Renvoie la question sous le format attendu, corrigé si besoin.
def MettreEnQuestion(words:str):
    if words.endswith("?"):
        return(words)
    else:
        return(words + "?")

# Prends en premier argument un string, cette fonction sert a comprendre la réponse du joueur, si la réponse commence par un "o", on assume qu'il veut dire "oui" et on l'interprète comme ceci,
# si on recoit n'importe quoi d'autre, on pense que le joueur a voulu dire "non".
# Renvoie un booléen True pour "oui" et False pour "Non"
def isYes(answer:str):
    if answer.lower().startswith("o"):
        return True
    else:
        return False

# Recoit un string en premier argument, sert a poser une question, elle se sert de la fonction juste au dessus (isYes()) pour interpréter la réponse.
def askYesNo(question:str):
    print(question, "\n", "O/N: ")
    return isYes(input())


# Fonction qui charge un fichier JSON et le renvoie interprété comme un dictionnaire.
# Le premier argument est un string et représente le chemin depuis le programme vers le fichier JSON a ouvrir
def readFile(path:str):
    file = open(path, "r")
    var = json.load(file)
    file.close()
    return(var)

# Fonction qui prends en premier argument l'adresse d'un fichier JSON sous forme de string et qui prends en deuxième argument un dictionnaire pour complètement ré-écrire le fichier de sauvegarde.
def updateFile(path:str, var:dict):
    file = open(path, "w")
    file.write(json.dumps(var, sort_keys=True, indent=4))
    file.close()


main()