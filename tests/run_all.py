import timeit
import time
import click
import random
import matplotlib.pyplot as plt
import numpy as np
import copy 

from config_utils import ConfigFile
from graph_gen import GraphGenerator

from model_zoo import model_zoo


from model_m import ModelM, load_model_from_config, load_graph

from pool import Pool


def evaluate_model(model, setup):

    my_model = model

    idx, random_seed, test_id, config, args = setup 
    ndays, print_interval, verbose = args

    if random_seed is not None:
        my_model.reset(random_seed=random_seed)
    
    my_model.run(ndays, print_interval=print_interval, verbose=verbose)

    # save history
    suffix = "" if not test_id else "_" + test_id
    file_name = f"history{suffix}.csv"
    config.save(file_name)
    cfg_string = ""
    with open(file_name, "r") as f:
        cfg_string = "#" + "#".join(f.readlines())
    with open(file_name, "w") as f:
        f.write(cfg_string)
        f.write(f"# RANDOM_SEED = {my_model.random_seed}\n")
        my_model.save_history(f)

#    with open(f"durations{suffix}.csv", "w") as f:
#        my_model.model.save_durations(f)

    return idx
#    del my_model 



def demo(filename, test_id=None, model_random_seed=42, use_policy=None, print_interval=1, n_repeat=1, n_jobs=1):

    cf = ConfigFile()
    cf.load(filename)
    graph = load_graph(cf) 

    ndays = cf.section_as_dict("TASK").get("duration_in_days", 60)
    print_interval = cf.section_as_dict("TASK").get("print_interval", 1)
    verbose = cf.section_as_dict("TASK").get("verbose", "Yes") == "Yes"


    # create model
    model = load_model_from_config(cf, use_policy, model_random_seed, preloaded_graph=graph)
    print("model loaded", flush=True) 

    # run parameters

    if test_id is None:
        test_id = ""

    models = [ model ]  
    random_seed = model.random_seed
    for i in range(1, n_jobs):
        print(f"{i} copy", flush=True) 
        models.append(model.duplicate(random_seed=random_seed + i)) 
    #random_seeds = [ model_random_seed + i for i in range(0, n_repeat)]


    pool = Pool(processors=n_jobs, evalfunc=evaluate_model, models=models)    
    for i in range(n_jobs):
        pool.putQuerry((i, None, f"{test_id}_{i}", cf, (ndays, print_interval, verbose)))
        
    i = n_jobs
    answers = 0
    rseed = models[-1].random_seed 
    while i < n_repeat:
        idx = pool.getAnswer()
        answers += 1 
        rseed += 1 
        pool.putQuerry((idx, rseed, 
                        f"{test_id}_{i}", cf, (ndays, print_interval, verbose)))
        i += 1

    for i in range(answers, n_repeat):
        pool.getAnswer()

    pool.close()
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
