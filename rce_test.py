import json
import os
from data.input_data import InputData
from rce.rce_trainer import RceTrainer

def load_test_data(file_name):
    with open(file_name, 'r') as f:
        parsed_data = json.loads(f.read())
        input = InputData(parsed_data)
    return input

def main():
    script_dir = os.path.dirname(__file__)
    training_data :InputData = load_test_data(script_dir + '/test_data_4_v4.json')

    rce_trainer = RceTrainer()

    print("Training RCE Network...")
    rce_trainer.Train(list(training_data.data.values()))

    # Print every progress of training - last step is the final network
    for rce_network in rce_trainer.rce_networks:
        print(rce_network)

if __name__ == "__main__":
    main()
