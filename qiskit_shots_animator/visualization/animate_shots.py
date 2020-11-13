#
# Copyright 2020 Tea Vui Huang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Animation functions for quantum output.
Simulates readout microwave (MW) pulses at the corresponding Rx read-out resonators

Quantum device images           Width x height (pixels)    Used by
---------------------------------------------------------------------------------
albatross.png                   500 x 100                  animate_shots_on_gate()
giraffe.png                     200 x 200                  animate_shots_on_gate()
snake.png                       200 x 200                  animate_shots_on_gate()
sparrow.png                     200 x 200                  animate_shots_on_gate()
sparrow_xray_labelled.png       300 x 300                  animate_shots_on_xray()
sparrow_xray_unlabelled.png     300 x 300                  animate_shots_on_xray()
unknown20a.png                  250 x 250                  animate_shots_on_gate()
unknown20b.png                  250 x 250                  animate_shots_on_gate()
unknown53a.png                  300 x 300                  animate_shots_on_gate()

Images modified from original images in:
IBM Research, qiskit's plot_gate_map() and https://github.com/Qiskit/ibmq-device-information
"""

from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import Circle
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np
import random
import io
import sys
import pkgutil

pkg_name = 'qiskit_shots_animator'
img_dir  = 'visualization/resources/'

err_incorrect_qubits_1 = 'ERROR: This quantum count require at least a '
err_incorrect_qubits_2 = '-qubit quantum processor'

supported_samples = {
  "sparrow"   : ( 5,200,200,300,300),
  "snake"     : ( 5,200,200,0,0),
  "giraffe"   : ( 5,200,200,0,0),
  "albatross" : (15,500,100,0,0),
  "unknown20a": (20,250,250,0,0),  
  "unknown20b": (20,250,250,0,0),  
  "unknown53a": (53,300,300,0,0), 
}
"""Supported samples for animate_shots_on_gate()

   sample_name: qubits, gate_width, gate_height, xray_width, xray_height
"""


def recreate_shots_from_counts( counts ):
    """Recreate shots from job result counts

    Recreates the individual shot results for the number of times the quantum circuit is repeated
    
    Args:
        counts (dict): job result counts, e.g. For 1024 shots: {'000': 510, '111': 514}
        
    Returns:
        list: the recreated-shots, e.g. ['000', '000', '111', '111']
    """
    raw_shots = []
    for k, v in counts.items():
        k = k[::-1]
        for x in range(v):
            raw_shots.append(k.replace(" ", ""))
    return raw_shots


def compact_counts_to_100_shots(counts):
    """Compact counts to 100 shots

    This helps to reduce animation generation time, and file size
    
    Args:
        counts (dict): job result counts, e.g. For 1024 shots: {'000': 510, '111': 514}
        
    Returns:
        dict: the compacted-counts, e.g. {'000': 51, '111': 51}
    """
    big_counts = counts.copy()
    if (sum(counts.values())>100):
        total = sum(big_counts.values())/100
        for x in big_counts:
            big_counts[x] = int(big_counts[x]/total)
        big_counts = {x:y for x,y in big_counts.items() if y!=0}
    if (big_counts=={}): return counts
    return big_counts
    

def animate_shots_on_gate(frame, fig, ax, device, recreated_shots, labelled, microwave_color, microwave_intensity):
    """Animate circuit as microwave flashes on a quantum CPU diagram

    The function called by FuncAnimation() at each frame to update the animation frame
    Arguments are supplied via the fargs parameter in FuncAnimation()
    
    Example quantum devices:
    05-Qubit: Ourense, Valencia, Vigo 
    05-Qubit: Yorktown, Tenerife 
    14-Qubit: Melbourne 
    20-Qubit: Almaden, Boeblingen, Singapore
    20-Qubit: Johannesburg, Poughkeepsie
    53-Qubit: Rochester    
    
    Args:
        frame (int): unused, sent by FuncAnimation()
        device (str): name of quantum CPU, case-insensitive
        recreated_shots (list): the recreated-shots, e.g. ['000', '000', '111', '111']
        labelled (boolean): True or False
        microwave_color (str): Python colors, e.g. 'white', 'lightblue' etc
        microwave_intensity (int): 0.1 to 1.0 (weakest to strongest)
    """
    ax.set_aspect('equal')
    num_shots = len(recreated_shots[0])
    ax.clear()
        
    # snake   = ibmq_athens, ibmq_santiago   
    # giraffe = ibmq_vigo, ibmq_ourense, ibmq_valencia   
    # sparrow = ibmqx2, ibmq_yorktown, ibmq_tenerife
    if (device=='giraffe') or (device=='snake') or (device=='sparrow'):
        if (num_shots>5):
            print(err_incorrect_qubits_1 + str(num_shots) + err_incorrect_qubits_2); raise Exception
            ax.axis('off')
            return
        else:
            img_name = device + '.png'
            if (__name__=='__main__'): img = plt.imread(img_name)
            else: img = plt.imread(io.BytesIO(pkgutil.get_data(pkg_name, img_dir + img_name)))            
            ax.imshow(img)
            # q0,q1,q2,q3,q4
            alpha_xy = [ (30,100), (100,31), (100,100),(170,100), (100,169) ]

        
    # albatross = ibmq_16_melbourne
    elif ( (device=='albatross') ):
        if (num_shots>15):
            print(err_incorrect_qubits_1 + str(num_shots) + err_incorrect_qubits_2); raise Exception
            ax.axis('off')
            return
        else:
            img_name = device + '.png'
            if (__name__=='__main__'): img = plt.imread(img_name)
            else: img = plt.imread(io.BytesIO(pkgutil.get_data(pkg_name, img_dir + img_name)))            
            ax.imshow(img)
            # q00,q01,q02,q03,q04,q05,q06
            # q14,q13,q12,q11,q10,q09,q08,q07
            alpha_xy = [ (55,22), (111,22), (167,22), (222,22), (278,22), (334,22), (390,22),  
                         (446,76), (390,76), (334,76), (278,76), (222,76), (167,76), (111,76), (55,76) ]
        
        
    # unknown20a = Johannesburg, Poughkeepsie
    # unknown20b = Almaden, Boeblingen, Singapore 
    elif (device=='unknown20a') or (device=='unknown20b'):
        if (num_shots>20):
            print(err_incorrect_qubits_1 + str(num_shots) + err_incorrect_qubits_2); raise Exception
            ax.axis('off')
            return
        else:
            img_name = device + '.png'
            if (__name__=='__main__'): img = plt.imread(img_name)
            else: img = plt.imread(io.BytesIO(pkgutil.get_data(pkg_name, img_dir + img_name)))
            ax.imshow(img)
            # q0,q1,q2,q3,q4, ...
            alpha_xy = [ (20,32) , (69,32) , (121, 32), (173,32), (225,32),
                         (20,92) , (69,92) , (121, 92), (173,92), (225,92),
                         (20,154), (69,154), (121, 154),(173,154),(225,154),
                         (20,217), (69,217), (121, 217),(173,217),(225,217) ]           
        
        
    # unknown53a = ibmq_rochester 
    elif (device=='unknown53a'):
        if (num_shots>53):
            print(err_incorrect_qubits_1 + str(num_shots) + err_incorrect_qubits_2); raise Exception
            ax.axis('off')
            return
        else:
            img_name = device + '.png'
            if (__name__=='__main__'): img = plt.imread(img_name)
            else: img = plt.imread(io.BytesIO(pkgutil.get_data(pkg_name, img_dir + img_name)))            
            ax.imshow(img)
            # q0,q1,q2,q3,q4, ...
            alpha_xy = [       (85,18), (117,18), (149,18), (181,18), (213,18),
                               (85,46),                               (213,46), 
            (19, 75), (52,75), (85,75), (117,75), (149,75), (181,75), (213,75), (246,75), (279,75),
            (19,106),                             (149,106),                              (279,106), 
            (19,135), (52,135),(85,135),(117,135),(149,135),(181,135),(213,135),(246,135),(279,135),
                               (85,165),                              (213,165), 
            (19,195), (52,195),(85,195),(117,195),(149,195),(181,195),(213,195),(246,195),(279,195),
            (19,224),                             (149,224),                              (279,224), 
            (19,253), (52,253),(85,253),(117,253),(149,253),(181,253),(213,253),(246,253),(279,253),
                               (85,283),                              (213,283)]        


    # Unknown device 
    else:
        print("ERROR: Unknown QPU, please use one of these: " + str(supported_samples)); raise Exception
        ax.axis('off')
        return
   
   
    # Create a circle at each x,y pair
    rnd = random.randint(0, len(recreated_shots)-1)
    for i in range(len(recreated_shots[0])):
        circ = Circle(alpha_xy[i], 14, color=microwave_color, alpha=int(recreated_shots[rnd][i])*microwave_intensity)
        ax.add_patch(circ)
    ax.axis('off')


def animate_shots_on_xray(frame, fig, ax, device, recreated_shots, labelled, microwave_color, microwave_intensity):
    """Animate circuit as microwave flashes on x-ray photo of quantum computer chip
    
    The function called by FuncAnimation() at each frame to update the animation frame
    Arguments are supplied via the fargs parameter in FuncAnimation()
    Microwave measurement pulses interact with qubits via readout resonators and are reflected back
    
    Example quantum devices:
    05-Qubit: Yorktown, Tenerife 
    
    Args:
        frame (int): unused, sent by FuncAnimation()
        device (str): name of quantum CPU, case-insensitive
        recreated_shots (list): the recreated-shots, e.g. ['000', '000', '111', '111']
        labelled (boolean): True or False
        microwave_color (str): Python colors, e.g. 'white', 'lightblue' etc
        microwave_intensity (int): 0.1 to 1.0 (weakest to strongest)
    """    
    ax.set_aspect('equal')
    num_shots = len(recreated_shots[0])
    ax.clear()

    # labelled: default = True
    if (labelled==True): img_name = 'sparrow_xray_labelled.png'
    else: img_name = 'sparrow_xray_unlabelled.png'    
    
    # Same image for all 5-qubit computers
    if (True):
        if (num_shots>5):
            print("ERROR: X-Ray only supports up to 5-qubit")
            print(err_incorrect_qubits_1 + str(num_shots) + err_incorrect_qubits_2); raise Exception      
        else:
            if (__name__=='__main__'): img = plt.imread(img_name)
            else: img = plt.imread(io.BytesIO(pkgutil.get_data(pkg_name, img_dir + img_name)))            
            ax.imshow(img)
            # r0,r1,r2,r3,r4
            alpha_xy = [ (141,245), (27,226), (37,97), (27,27), (141,27) ]
            delta_x  = [ 134,  91,  37, 91, 134 ]
            delta_y  = [  27,  45, 103, 44,  26 ]
            
    # Create a circle at each x,y pair
    # Rectangle(xy, width, height, angle=0.0, **kwargs)[source]
    rnd = random.randint(0, len(recreated_shots)-1)
    for i in range(len(recreated_shots[0])):
        rect = FancyBboxPatch(alpha_xy[i],delta_x[i],delta_y[i],boxstyle='round,pad=5,rounding_size=20', color=microwave_color,
        alpha=int(recreated_shots[rnd][i])*microwave_intensity)
        ax.add_patch(rect)
    ax.axis('off')


def get_fig_size(ani_type, ani_qpu):
    """Return figsize(width, height) in inches
    
    Args:
        ani_type (str): 'gate' or ¨xray'
        ani_qpu (str): sample name, e.g. 'albatross'
        
    Returns:
        width: inches
        height: inches
    """      
    fig_width=0; fig_height=0;
    if (ani_qpu in supported_samples):
        if (ani_type=="gate"): 
            fig_width  = supported_samples[ani_qpu][1]
            fig_height = supported_samples[ani_qpu][2]
        else:
            fig_width  = supported_samples[ani_qpu][3]
            fig_height = supported_samples[ani_qpu][4]
    return fig_width/100, fig_height/100
    

def get_supported_samples():
    """Return dictionary of supported_samples
    """      
    return supported_samples


def get_sample(backend, circuit):
    """Auto-select QPU
    
    Either use sample_name from backend if available, or determine using num of qubits from circuit
    
    Args:
        backend: backend
        circuit: circuit
        
    Returns:
        sample_name: sample_name
    """          
    sample_name = ""
    backend_dict = backend.configuration().to_dict()
    if ("sample_name" not in backend_dict): backend_dict["sample_name"] = ""
    if (backend_dict["simulator"]==True) or (backend_dict["sample_name"] not in supported_samples):
        # fit num_qubits in circuit
        for sample_name in supported_samples:
            sample_qubits = supported_samples[sample_name][0]
            if (sample_qubits>=circuit.num_qubits): break      
    else:
        sample_name = backend_dict["sample_name"].lower()
    return sample_name
    
    
def save_quantum_animation(ani_filename, ani_type, ani_fps, ani_counts, ani_qpu, **kwargs):
    """Save Quantum animation
    
    Save Quantum animation to looping GIF file
    
    Args:
        ani_filename (str): file name to save as
        ani_type (str): 'gate' or ¨xray'
        ani_fps (int): shots per second, equals to frame per second
        ani_counts (dict): job result counts, e.g. For 1024 shots: {'000': 510, '111': 514}
        ani_qpu (str): sample name, e.g. 'albatross'                
        labelled (boolean): True or False, only for ani_type='xray'
        microwave_color (str): Python colors, e.g. 'white', 'lightblue' etc
        microwave_intensity (int): 0.1 to 1.0 (weakest to strongest)
        
    Returns:
        status: True if successul, or False if not
    """          
    # Make ani_qpu lowercase
    if type(ani_qpu)==str:  ani_qpu = ani_qpu.lower() 
    
    # Set minimum shots per sec to 1
    if (ani_fps<1): ani_fps=1
    
    # Check animation type
    if type(ani_type)==str: ani_type = ani_type.lower() 
    if (ani_type!="gate") and (ani_type!="xray"):
        print("ERROR: Animation type not supported, use 'gate' or 'xray'")
        return
    
    # Check params for animation type
    if (ani_type=="gate") and (ani_qpu==""):
        print("ERROR: Animation type 'gate' must have a sample name, use auto-select or provide one, e.g. 'sparrow'")
        return
            
    # microwave_color: default = white
    microwave_color = ""
    if ('microwave_color' not in kwargs): kwargs['microwave_color']='white'
    microwave_color = kwargs['microwave_color']
    if (microwave_color==""): microwave_color="white"
        
    # microwave_intensity: default = 0.5, min = 0.1, max = 1.0
    microwave_intensity = ""
    if ('microwave_intensity' not in kwargs): 
        if (ani_type=="gate"): kwargs['microwave_intensity']=0.7
        else: kwargs['microwave_intensity']=0.5
    microwave_intensity = kwargs['microwave_intensity']
    if (microwave_intensity<0.1): microwave_intensity=0.1
    if (microwave_intensity>1): microwave_intensity=1            
            
    # labelled: default = True
    if ('labelled' not in kwargs): kwargs['labelled']=True
    labelled = kwargs['labelled']
                        
    # Create plot    
    matplotlib.use('Agg')
    plt.close('all')
    fig, ax = plt.subplots(1, figsize=(get_fig_size(ani_type, ani_qpu)), dpi=100)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.close(fig)    
    
    # Expand counts to shots
    ani_counts2 = compact_counts_to_100_shots(ani_counts)
    recreated_shots = recreate_shots_from_counts(ani_counts2)
    
    # Select frame function to use 
    if (ani_type=="xray"): frame_func = animate_shots_on_xray
    else: frame_func = animate_shots_on_gate    
    ani = animation.FuncAnimation(fig, frame_func, fargs=(fig, ax, ani_qpu, recreated_shots, labelled, microwave_color, microwave_intensity),
                                  repeat=False, interval=(1/ani_fps), frames=sum(ani_counts2.values()))
        
    # save animation as looping gif
    writergif = animation.PillowWriter(fps=ani_fps) 
    try:
        ani.save(ani_filename, writer=writergif)
    except:
        print("ERROR: Could not create/save animation")
        return False
    return True
