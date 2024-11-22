import json
import os
from rce.rce_network import RceNetwork
from data.input_data import InputData, Point
from rce.rce_trainer import RceTrainer

def load_test_data(file_name):
    with open(file_name, 'r') as f:
        parsed_data = json.loads(f.read())
        input = InputData(parsed_data)
    return input

def main():
    # Načítanie testovacích dát
    script_dir = os.path.dirname(__file__)
    training_data :InputData = load_test_data(script_dir + '/test_data.json')

    # Vytvorenie RCE siete
    rce_trainer = RceTrainer()

    # Trénovanie RCE siete
    print("Training RCE Network with test data...")
    rce_trainer.Train(list(training_data.data.values()))

    # Print every network
    for rce_network in rce_trainer.rce_networks:
        print(rce_network)

if __name__ == "__main__":
    main()
