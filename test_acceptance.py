import subprocess

print('testing docker')
docker_setup = subprocess.run(['docker', 'build', '.'])
docker_basic = subprocess.run(['docker', 'run', '-t', 'pycrawler-fxwood'])

docker_filter = subprocess.run(['docker', 'run', '-t', 'pycrawler-fxwood', '20', "the", "to", "of", "a", "and", "in", "for", "with", "On", "In"])

shell_basic = subprocess.run(['python3', 'crawler.py', '20'])

shell_filter = subprocess.run(['python3', 'crawler.py', '8', "the", "to", "of", "a", "and", "in", "for", "with", "On", "In"])

