import subprocess
import json

def run_pyan(input_file):
    try:
        result = subprocess.run(['pyan', input_file], capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        raise FileNotFoundError("Pyan not found in system path.")

def generate_call_graph(source_code_file):
    pyan_output = run_pyan(source_code_file)
    # Pyan vrací výstup ve formátu dot, takže jej můžeme převést na JSON pomocí nástroje dot
    dot_command = f'dot -Tjson -o {source_code_file}.json'
    subprocess.run(dot_command, input=pyan_output, shell=True, text=True)

    # Načteme JSON výstup
    with open(f'{source_code_file}.json', 'r') as json_file:
        call_graph_json = json.load(json_file)

    return call_graph_json

# Příklad použití:
source_code_file = 'your_c_or_cpp_file.c'
call_graph = generate_call_graph(source_code_file)
print(json.dumps(call_graph, indent=2))
