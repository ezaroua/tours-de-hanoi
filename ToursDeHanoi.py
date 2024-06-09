# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 17:34:30 2024

@author: User
"""

import tkinter as tk
from os.path import abspath


class HanoiGUI:
    def __init__(self, master, num_disks):
        self.master = master
        self.num_disks = num_disks
        self.move_counter = 0

        # Créer une toile (canvas) pour dessiner les tours
        self.canvas = tk.Canvas(master, width=600, height=300)
        self.canvas.pack()

        # Initialiser les tours avec les disques
        self.towers = {
            'A': [i for i in range(num_disks, 0, -1)],
            'B': [],
            'C': []
        }

        # Dessiner les tours initiales
        self.draw_towers()

        # Déplacer les disques de la tour A à la tour C
        self.move_disks(num_disks, 'A', 'C', 'B')

    def draw_towers(self):
        self.canvas.delete("all")  # Effacer le contenu de la toile
        tower_width = 10  # Largeur des disques
        tower_spacing = 150  # Espacement entre les tours
        disk_height = 20  # Hauteur des disques
        tower_height = 200  # Hauteur des tours

        # Dessiner chaque tour et ses disques
        for tower, disks in self.towers.items():
            x = tower_spacing * (ord(tower) - ord('A') + 1)  # Position horizontale de la tour
            y_base = 300  # Position verticale de la base des tours

            # Dessiner la tour (rectangle)
            self.canvas.create_rectangle(x - tower_width, y_base, x + tower_width, y_base - tower_height,
                                         outline="black", fill="black")

            # Dessiner les disques sur la tour
            for i, disk in enumerate(disks):
                disk_width = disk * 20
                y = y_base - (i + 1) * disk_height  # Déplace les disques vers le haut
                self.canvas.create_rectangle(x - disk_width / 2, y, x + disk_width / 2, y + disk_height, fill="blue")

    def move_disks(self, n, source, target, auxiliary):
        if n > 0:
            # Déplacer n-1 disques de la source à l'auxiliaire, en utilisant la cible comme tour intermédiaire
            self.move_disks(n - 1, source, auxiliary, target)
            self.move_counter += 1  # Incrémenter le compteur de mouvements
            print(f"Move {self.move_counter}: Mouvement du disque depuis {source} vers {target}")

            disk = self.towers[source][-1]

            self.towers[source].pop()  # Suprime le disque du dessus de la tour source
            self.draw_towers()  # Redessine l'état actuel des tours avant le déplacement
            self.animate_move(source, target, disk)  # Anime le déplacement du disque entre les tours source et cible
            self.towers[target].append(disk)  # Place le disque sur la tour cible
            self.draw_towers()  # Redessine l'état actuel des tours après le déplacement
            self.move_disks(n - 1, auxiliary, target,
                            source)  # Déplace les disques restants de l'auxiliaire vers la cible
            self.master.update()  # Met à jour l'affichage graphique

    def animate_move(self, from_tower, to_tower, disk):
        start_x = 150 * (ord(from_tower) - ord(
            'A') + 1)  # Calcul de la position horizontale de départ en fonction de la tour source
        end_x = 150 * (ord(to_tower) - ord(
            'A') + 1)  # Calcul de la position horizontale d'arrivée en fonction de la tour cible

        # Calcul de la hauteur de déplacement vertical en fonction de la hauteur totale de la tour moins y_start
        y_start = 300 - 20 * (len(self.towers[from_tower]) + 1)

        totaldiskHeightFrom = (len(
            self.towers[from_tower])) * 20  # Calcul de la hauteur totale des disques sur la tour source
        totaldiskHeightTo = (len(
            self.towers[to_tower])) * 20  # Calcul de la hauteur totale des disques sur la tour cible

        # création du rectangle qui va se déplacer.
        disk_id = self.canvas.create_rectangle(start_x - (20 * disk) / 2, y_start, start_x + (20 * disk) / 2,
                                               y_start - 20,
                                               fill="red")

        # Déplacement vertical vers le haut
        for frame in range(0, 200 - totaldiskHeightFrom, 5):
            self.canvas.move(disk_id, 0, -5)
            self.canvas.update()
            self.master.after(25)

        # Déplacement horizontal
        for frame in range(40):
            self.canvas.move(disk_id, (end_x - start_x) / 40, 0)
            self.canvas.update()
            self.master.after(25)

        # Déplacement vertical vers le bas pour empiler sur la tour d'arrivée
        for frame in range(0, 200 - totaldiskHeightTo, 5):
            self.canvas.move(disk_id, 0, 5)
            self.canvas.update()
            self.master.after(25)

        self.canvas.delete(disk_id)


def main():
    num_disks = 3  # Nombre de disques défini

    root = tk.Tk()  # Créer la fenêtre principale
    root.title("Tours de Hanoï")  # Créer le titre de l'application
    hanoi_gui = HanoiGUI(root,
                         num_disks)  # Créer une instance de la classe HanoiGUI avec la fenêtre principale et le nombre de disques

    root.mainloop()  # Lance la boucle principale de l'interface graphique Tkinter pour afficher la fenêtre et gérer les événements


if __name__ == "__main__":
    main()