import json
import sys
import subprocess
import platform
import os

def collect_sources_and_working_dir(target_id, targets_dict, collected_targets=None, collected_sources=None):
    if collected_targets is None:
        collected_targets = set()
    if collected_sources is None:
        collected_sources = []
    if target_id in collected_targets:
        # already processed this target
        return collected_sources, None
    collected_targets.add(target_id)
    target = targets_dict.get(target_id)
    if not target:
        # Could not find target, raise an error
        raise ValueError(f"Target '{target_id}' not found.")
    # First, process included targets
    for included_target_id in target.get('include_targets', []):
        collect_sources_and_working_dir(included_target_id, targets_dict, collected_targets, collected_sources)
    # Then add the sources from the current target
    for source in target.get('sources', []):
        if source not in collected_sources:
            collected_sources.append(source)
    # Return the working directory of the current target
    return collected_sources, target.get('working_dir')

def main():
    # Read the JSON file
    with open('simulation/targets.json', 'r') as f:
        data = json.load(f)

    # Build the targets dictionary
    targets_dict = {target['id']: target for target in data['build_targets']}

    # Get the target_id from command line arguments or use default_target
    if len(sys.argv) > 1:
        target_id = sys.argv[1]
    else:
        target_id = data['default_target']

    # Collect sources and working directory
    try:
        sources, working_dir = collect_sources_and_working_dir(target_id, targets_dict)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if not working_dir:
        print(f"No working directory specified for target '{target_id}'.")
        sys.exit(1)

    # Build the iverilog command
    iverilog_cmd = ['iverilog', '-o', f'{target_id}.vvp'] + sources

    # Run the iverilog command in the specified working directory
    try:
        print('Running iverilog...')
        subprocess.check_call(iverilog_cmd, cwd=working_dir)
    except subprocess.CalledProcessError as e:
        print('Error running iverilog.')
        sys.exit(1)

    # Run the simulation
    vvp_cmd = ['vvp', f'{target_id}.vvp']
    try:
        print('Running simulation...')
        subprocess.check_call(vvp_cmd, cwd=working_dir)
    except subprocess.CalledProcessError as e:
        print('Error running simulation.')
        sys.exit(1)

    # Open the waveform file
    vcd_file = os.path.join(working_dir, f'{target_id}.vcd')
    if os.path.exists(vcd_file):
        system_name = platform.system()
        if system_name == 'Darwin':
            # macOS
            open_cmd = ['open', '-a', 'Scansion', vcd_file]
        else:
            # Assume Linux or Windows has gtkwave installed
            open_cmd = ['gtkwave', vcd_file]
        try:
            print('Opening waveform...')
            subprocess.Popen(open_cmd)
        except Exception as e:
            print('Error opening waveform viewer.')
            print(e)
    else:
        print(f'Waveform file {vcd_file} not found.')

if __name__ == '__main__':
    main()