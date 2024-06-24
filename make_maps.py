import subprocess
import os
import glob

PLOTTER_SCRIPT = os.path.join(os.environ["SUMO_HOME"],"tools/visualization/plot_net_dump.py")

def make_map(network_file, edgedata_file, output_file, title='Test Title', max_color_value=50):

    command = [
        'python',
        PLOTTER_SCRIPT, 
        '-n', network_file,
        '-i', edgedata_file, 
        '--measures', 'queueing_length,queueing_length',
        '--title', title,
        '--color-bar-label', 'Queue Length',
        '--max-width', '8', 
        '--min-width', '3',
        '--min-color-value', '0', 
        '--max-color-value', str(max_color_value),
        '--colormap', '#0:#9de96c,.5:#da9d15,1:#be0202', 
        '-b',
        '--default-width', '3', 
        '--default-color', '#9de96c',
        '--xlabel', 'Distance[m]', 
        '--ylabel', 'Distance[m]',
        '--internal',
        '-o', output_file
    ]

    subprocess.run(command, check=True)


def make_maps(network_file, case_name, title='Test Title', max_color_value=50):
    matching_files = glob.glob(f'grid4x4/**/{case_name}_edgedata.xml')
    for edgedata_file in matching_files:
        print(f"Processing {edgedata_file}...")
        output_dir = os.path.join(os.path.dirname(edgedata_file), case_name)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{case_name}.png")
        make_map(network_file, edgedata_file, output_file, title=title, max_color_value=max_color_value)

make_maps(
    network_file='grid4x4.net.xml',
    case_name='morning_1',
    title='Case 1 Queue Length Map',
    max_color_value=40
)
