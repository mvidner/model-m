import timeit
import time
import click
import random
import matplotlib.pyplot as plt
import numpy as np
import copy 

from config_utils import ConfigFile
from graph_gen import GraphGenerator
from load_model import create_graph, matrix,  load_graph
from policy import bound_policy

from model_zoo import model_zoo


from model_m import ModelM, load_model_from_config

from multiprocessing import Pool


def evaluate_model(setup):

    model, test_id, cf, args = setup
    ndays, print_interval, verbose = args
    model.run(ndays, print_interval=print_interval, verbose=verbose)

    # save history
    suffix = "" if not test_id else "_" + test_id
    file_name = f"history{suffix}.csv"
    cf.save(file_name)
    cfg_string = ""
    with open(file_name, "r") as f:
        cfg_string = "#" + "#".join(f.readlines())
    with open(file_name, "w") as f:
        f.write(cfg_string)
        f.write(f"# RANDOM_SEED = {model.random_seed}\n")
        model.save_history(f)
    


def demo(filename, test_id=None, model_random_seed=42, use_policy=None, print_interval=1, n_repeat=1, n_jobs=1):

    cf = ConfigFile()
    cf.load(filename)

    # create model
    model = load_model_from_config(cf, use_policy, model_random_seed)
    print("model loaded", flush=True) 

    # run parameters
    ndays = cf.section_as_dict("TASK").get("duration_in_days", 60)
    print_interval = cf.section_as_dict("TASK").get("print_interval", 1)
    verbose = cf.section_as_dict("TASK").get("verbose", "Yes") == "Yes"

    if test_id is None:
        test_id = ""

    models = [ model ] 
    for i in range(1, n_repeat):
        print(f"{i} copy", flush=True) 
        models.append(model.duplicate()) 
    
    setups = zip(models, [f"{test_id}_{i}" for i in  range(0, n_repeat)], [cf]*n_repeat, 
                 [(ndays, print_interval, verbose)]*n_repeat)


    with Pool(n_jobs) as pool: 
        print("READY")
        pool.map(evaluate_model, setups)
        
    print("finished")



@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--policy', '-p', default=None)
@click.option('--print_interval',  default=1)
@click.option('--n_repeat',  default=1)
@click.option('--n_jobs', default=1) 
@click.argument('filename', default="example.ini")
@click.argument('test_id', default="")
def test(set_random_seed, policy, print_interval, n_repeat, n_jobs, filename, test_id):
    """ Run the demo test inside the timeit """

    random_seed = 42 if set_random_seed else random.randint(0, 10000)
    def demo_fce(): return demo(filename, test_id,
                                model_random_seed=random_seed, use_policy=policy, print_interval=print_interval, 
                                n_repeat=n_repeat, n_jobs=n_jobs)
    print(timeit.timeit(demo_fce, number=1))


if __name__ == "__main__":
    test()
