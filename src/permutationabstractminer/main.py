import sys
import PermutationSearch


def main():
    keywords1 = ['Monocular', '"Mono camera*"', 'Vision']
    keywords2 = ['Safe', 'Safety', 'Robust*']
    keywords3 = ['Collision* Avoidance', 'Obstacle* Detection*']
    # keywords1 = ['Monocular', '"Mono camera$"', 'Vision']    
    # keywords2 = ['Validat*', 'Simulat*', 'Testing', 'Verif*']
    # keywords3 = ['Collision$ Avoidance', 'Obstacle$ Detection$']

    miner = PermutationSearch.ScopusMiner()
    miner.run(keywords1, keywords2, keywords3)

if __name__ == "__main__":
    main()