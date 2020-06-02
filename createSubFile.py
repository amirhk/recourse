import numpy as np

# SCM_CLASS_VALUES = ['sanity-3-lin', 'sanity-3-anm', 'sanity-3-gen']
# LAMBDA_LCB_VALUES = [1., 2.]
# OPTIMIZATION_APPROACHES = ['brute_force', 'grad_descent']
# CLASSIFIER_VALUES = ['lr']

# SCM_CLASS_VALUES = ['sanity-3-lin', 'sanity-3-anm', 'sanity-3-gen']
# SCM_CLASS_VALUES = ['sanity-3-gen']
SCM_CLASS_VALUES = ['sanity-3-lin', 'sanity-3-anm']
LAMBDA_LCB_VALUES = [2.]
OPTIMIZATION_APPROACHES = ['grad_descent']
CLASSIFIER_VALUES = ['lr']

# ==============================================================================
# ==============================================================================

# SCM_CLASS_VALUES = ['german-credit']
# LAMBDA_LCB_VALUES = np.linspace(0, 2.5, 6)
# OPTIMIZATION_APPROACHES = ['grad_descent']
# CLASSIFIER_VALUES = ['lr', 'mlp']

# ==============================================================================
# ==============================================================================

# SCM_CLASS_VALUES = ['german-credit']
# LAMBDA_LCB_VALUES =  np.linspace(0, 2.5, 6)
# OPTIMIZATION_APPROACHES = ['brute_force']
# CLASSIFIER_VALUES = ['tree']

# ==============================================================================
# ==============================================================================

NUM_BATCHES = 100
NUM_NEG_SAMPLES_PER_BATCH = 1
request_memory = 8192*8


sub_file = open('test.sub','w')
print('executable = /home/amir/dev/recourse/_venv/bin/python', file=sub_file)
print('error = _cluster_logs/test.$(Process).err', file=sub_file)
print('output = _cluster_logs/test.$(Process).out', file=sub_file)
print('log = _cluster_logs/test.$(Process).log', file=sub_file)
print(f'request_memory = {request_memory}', file=sub_file)
print('request_cpus = 4', file=sub_file)
print('\n' * 2, file=sub_file)

for scm_class in SCM_CLASS_VALUES:
  for classifier_class in CLASSIFIER_VALUES:
    for lambda_lcb in LAMBDA_LCB_VALUES:
      for optimization_approach in OPTIMIZATION_APPROACHES:
        for batch_number in range(NUM_BATCHES):
          command = \
            f'arguments = main.py' \
            f' --scm_class {scm_class}' \
            f' --classifier_class {classifier_class}' \
            f' --lambda_lcb {lambda_lcb}' \
            f' --optimization_approach {optimization_approach}'

          # run-specific options
          if optimization_approach == 'grad_descent':
            command += f' --grad_descent_epochs 1000'
          elif optimization_approach == 'brute_force':
            command += f' --grid_search_bins 20'

          if scm_class == 'german-credit':
            command += f' --grid_search_bins 10'
            command += f' --non_intervenable_nodes x1 x2 x5'

          # finally add batch, samples, and process id params
          command += f' --batch_number {batch_number}'
          command += f' --sample_count {NUM_NEG_SAMPLES_PER_BATCH}'
          command += f' -p $(Process)'
          print(command, file=sub_file)
          print('queue', file=sub_file)
          print('\n', file=sub_file)

