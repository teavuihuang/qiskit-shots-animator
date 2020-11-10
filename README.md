
## Quantum-Computer Microwave-Pulse Animator


**Qiskit** is an open-source framework for working with noisy quantum computers at the level of pulses, circuits, and algorithms. Tea Vui Huang's **Qiskit-Shots-Animator** animates microwave-pulse shots in a quantum circuit execution as microwave flashes either on a gate map, or x-ray photo of the quantum computer chip. Microwave measurement pulses interact with qubits via readout resonators and are reflected back, the animation illustrates readout microwave (MW) pulses at the corresponding Rx read-out resonators.


## Usage

```python
from IPython.core.display import display, Image
from qiskit_shots_animator.visualization import save_quantum_animation, 
	get_supported_samples, get_sample
```


Import the `qiskit-shots-animator` functions and call **save_quantum_animation()** with the following parameters:
- filename (str): file name to save as
- type (str): 'gate' or 'xray'
- fps (int): shots per second
- counts (dict): job result counts, e.g. for 1024 shots: {'000': 510, '111': 514}
- sample (str): sample name, e.g. 'albatross'                
- labelled (boolean): True or False, only for type='xray'
- microwave_color (str): Python colors, e.g. 'white', 'lightblue' etc
- microwave_intensity (int): 0.1 to 1.0 (weakest to strongest)


## Examples


### 1a. Animate quantum circuit execution on gate map at 3 shots/sec on Qiskit-Aer backend with **get_sample()** to auto-select quantum device


```python
import qiskit.tools.jupyter
from qiskit import IBMQ, QuantumCircuit, Aer, execute
from qiskit.circuit.random import random_circuit
from IPython.core.display import display, Image
from qiskit_shots_animator.visualization import save_quantum_animation, 
	get_supported_samples, get_sample

# Generate and execute a 5-qubit random-circuit on Qiskit-Aer backend
backend = Aer.get_backend('qasm_simulator')
while(1):
    circ = random_circuit(5, 2, max_operands=3, measure=True)
    counts = execute(circ, backend, shots=1000).result().get_counts()
    if len(counts)>4: break    
        
# Save & display animation of quantum circuit execution
filename = "quantum-shots_5q.gif"
save_quantum_animation(filename, "gate", 3, counts, get_sample(backend, circ))
img = Image(filename); img.reload(); display(img)
print(circ.draw())
```

'Sparrow' quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_sparrow.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_sparrow.gif)


### 1b. Animate quantum circuit execution on gate map at 3 shots/sec with 'giraffe' device


```python
filename = "quantum-shots_5q_giraffe.gif"
save_quantum_animation(filename, "gate", 3, counts, "giraffe") 
img = Image(filename); img.reload(); display(img)
```

'Giraffe' quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_giraffe.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_giraffe.gif)


### 1c. Animate quantum circuit execution on a labelled x-ray photo at 3 shots/sec, with microwave color 'lightblue' & microwave intensity 0.6


```python
filename = "quantum-shots_5q_sparrow_xray-labelled.gif"
save_quantum_animation(filename, "xray", 3, counts,
	get_sample(backend, circ), labelled=True,
	microwave_color="lightblue", microwave_intensity=0.6)
img = Image(filename); img.reload(); display(img)
```

'Sparrow' quantum device:   
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_sparrow_xray-labelled.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_sparrow_xray-labelled.gif)


### 1d. Animate quantum circuit execution on an unlabelled x-ray photo at 3 shots/sec, with microwave color 'white' & microwave intensity 0.5


```python
filename = "quantum-shots_5q_sparrow_xray-unlabelled.gif"
save_quantum_animation(filename, "xray", 3, counts,
	get_sample(backend, circ), labelled=False,
	microwave_color="white", microwave_intensity=0.5)
img = Image(filename); img.reload(); display(img)
```

'Sparrow' quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_sparrow_xray-unlabelled.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_circuit/quantum-shots_5q_sparrow_xray-unlabelled.gif)


### 1e. Animate quantum circuit execution on all supported devices at 3 shots/sec using **get_supported_samples()**


```python
for sample in get_supported_samples():
    print(sample); filename = "quantum-shots_5q_" + sample + ".gif"
    if (save_quantum_animation(filename, "gate", 3, counts, sample)==True):
        img = Image(filename); img.reload(); display(img)  
```


### 2. Animate 15-qubits random-number-generator quantum circuit execution on IBMQ provider


```python
import qiskit.tools.jupyter
from qiskit import IBMQ, QuantumCircuit, Aer, execute
from qiskit.circuit.random import random_circuit
from IPython.core.display import display, Image
from qiskit_shots_animator.visualization import save_quantum_animation, 
	get_sample, get_supported_samples

# Generate and execute random circuit remotely on ibmq_qasm_simulator
provider = IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
# Use 'ibmq_16_melbourne' if don't mind waiting in the queue
backend = provider.get_backend('ibmq_qasm_simulator')

# Build a random-number-generator quantum circuit
rng_size = 15; circ = QuantumCircuit(rng_size, rng_size)
circ.h(range(rng_size)) # Applies hadamard gate to all qubits
circ.measure(range(rng_size), range(rng_size)) # Measures all qubits
counts = execute(circ, backend, shots=1000).result().get_counts()

# Save & display animation of quantum circuit execution 
filename = "quantum-shots_15q.gif"
save_quantum_animation(filename, "gate", 3, counts, get_sample(backend, circ))
img = Image(filename); img.reload(); display(img)
print(circ.draw())
```

15-qubits 'Albatross' quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_15q_albatross_rng.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_15q_albatross_rng.gif)




### 3. Animate 20-qubits random-number-generator quantum circuit execution on IBMQ provider


```python
import qiskit.tools.jupyter
from qiskit import IBMQ, QuantumCircuit, Aer, execute
from qiskit.circuit.random import random_circuit
from IPython.core.display import display, Image
from qiskit_shots_animator.visualization import save_quantum_animation, 
	get_sample, get_supported_samples

# Generate and execute random circuit remotely on ibmq_qasm_simulator
provider = IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_qasm_simulator')

# Build a random-number-generator quantum circuit
rng_size = 20; circ = QuantumCircuit(rng_size, rng_size)
circ.h(range(rng_size)) # Applies hadamard gate to all qubits
circ.measure(range(rng_size), range(rng_size)) # Measures all qubits
counts = execute(circ, backend, shots=1000).result().get_counts()

# Save & display animation of quantum circuit execution 
filename = "quantum-shots_20q_unknown20a.gif"
save_quantum_animation(filename, "gate", 3, counts, "unknown20a")
img = Image(filename); img.reload(); display(img)
filename = "quantum-shots_20q_unknown20b.gif"
save_quantum_animation(filename, "gate", 3, counts, "unknown20b")
img = Image(filename); img.reload(); display(img)
print(circ.draw())
```

20-qubits quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_20q_unknown20a_rng.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_20q_unknown20a_rng.gif)

20-qubits quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_20q_unknown20b_rng.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_20q_unknown20b_rng.gif)



### 4. Animate 53-qubits random-number-generator quantum circuit execution on Qiskit-Aer backend


```python
import qiskit.tools.jupyter
from qiskit import IBMQ, QuantumCircuit, Aer, execute
from qiskit.circuit.random import random_circuit
from IPython.core.display import display, Image
from qiskit_shots_animator.visualization import save_quantum_animation, 
	get_sample, get_supported_samples

# Generate and execute random circuit locally on Aer qasm_simulator
backend = Aer.get_backend('qasm_simulator')

# Build a quantum circuit - random number generator
rng_size = 53; circ = QuantumCircuit(rng_size, rng_size)
circ.h(range(rng_size)) # Applies hadamard gate to all qubits
circ.measure(range(rng_size), range(rng_size)) # Measures all qubits
counts = execute(circ, backend, shots=1000).result().get_counts()

# Save & display animation of quantum circuit execution 
filename = "quantum-shots_53q_unknown53a.gif"
save_quantum_animation(filename, "gate", 3, counts, "unknown53a")
img = Image(filename); img.reload(); display(img)
print(circ.draw())
```

53-qubits quantum device:  
[![](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_53q_unknown53a_rng.gif)](https://raw.githubusercontent.com/teavuihuang/qiskit-shots-animator/main/examples/images/random_number_generator/quantum-shots_53q_unknown53a_rng.gif)






## Author and Citation
Tea Vui Huang. (2020, November 10). 
Qiskit Quantum-Computer Microwave-Pulse Animator. https://doi.org/10.5281/zenodo.4266489
