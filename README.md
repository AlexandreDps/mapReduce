# mapReduce
#Polytech - Map Reduce project

#Variables utiles :

<code>sometext</code> correspond à la variable ou sera stocké le texte d'origine. Dans cette exemple le texte est la page "python" de wikipedia qui est scrappée.

<code>nbpaquet</code> est une variable correspondant au nombre de paquets qui vont diviser le texte initial. Exemple {"Ceci est", "une phrase", "divisée en", "quatre paquets"}

<code>nombredefred</code> est une vraiable correspondant au nombre de threads à lancer.

#Déroulement du programme

Voici les différentes étapes du déroulement du programme.
* On créé une boucle ligne 116 pour créer tous nos Threads avec pour attribut 'mapper'

* Ensuite on créé une boucle <code>ligne 119</code> pour démarrer tous les Threads. Au départ tous les Threads sont mapper et s'occupent de mapper. Si un Thread à fini de mapper un paquet, il peut continuer à mapper d'autres paquets restants.

* Si un Thread à fini de mapper et qu'il ne reste plus rien à mapper, ce dernier se met en attente de l'évenement 'mapped' et passe en reducer.

* Une fois que le dernier Thread à terminé de mapper, il déclenche l'évenement 'mapped' avec <code>'mapped.set()'</code> qui permettra aux threads de continuer.

* Tous les threads qui étaient mapper à la base deviennent alors reducer et commencent à réduire.

Ils parcourent la liste 'aftermap' en cherchant un mot bien précis pour réunir toutes les occurences de ce mot (déjà précompté par paquet).
Une fois que les threads ont terminé leur phase reduce, ils 'meurent'. On attends que tous les threads meurent avec la fonction <code>.join()</code> puis on affiche les resultats.
