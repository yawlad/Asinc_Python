import yaml

data = {
    '15€': ['1',2,3,4,5,6, '10'],
    '25$': 2022,
    '35 продукты ₦': {'third': 3,
            'third_': '\uff85'}
}

def dump_data(data):
    with open('home_02/task_03/file.yaml', 'w+', encoding='utf-8') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=True, allow_unicode=True)
        
def check_work():
    with open('home_02/task_03/file.yaml', 'r', encoding='utf-8') as yaml_file:
        assert yaml.safe_load(yaml_file) == data   
        
dump_data(data)
check_work()