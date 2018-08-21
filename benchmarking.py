from controller import Controller
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',
                    dest='file',
                    action='store',
                    required=True,
                    type=str,
                    help='File to read.')

parser.add_argument('-r', '--repo',
                    dest='repo',
                    action='store',
                    required=True,
                    type=str,
                    help='Location of records.')

parser.add_argument('-t', '--tag',
                    dest='tag',
                    action='store',
                    required=True,
                    type=str,
                    help='Tag for outfiles and logging.')

arguments = parser.parse_args()

# Run the program
cont = Controller(arguments.file, arguments.repo, arguments.tag, 'Linkage', cutoff=4,
                block_on=['SIN', 'DOB'],
                exact=['SIN', 'DOB', 'PhoneNum', 'Province'],
                string=['Name'])

# Add timers and memory usage stats to log files
if not os.path.isdir('logs/' + arguments.tag + '/'):
    os.mkdir('logs/' + arguments.tag + '/')

f = open('logs/' + arguments.tag + '/job_times.txt', 'a+')
f.write(str(cont.timers['job_timer'].time) + '\n')

f = open('logs/' + arguments.tag + '/read_times.txt', 'a+')
f.write(str(cont.timers['read_timer'].time) + '\n')

f = open('logs/' + arguments.tag + '/run_times.txt', 'a+')
f.write(str(cont.timers['run_timer'].time) + '\n')

f = open('logs/' + arguments.tag + '/write_times.txt', 'a+')
f.write(str(cont.timers['write_timer'].time) + '\n')

f = open('logs/' + arguments.tag + '/df_memory.txt', 'a+')
f.write(str(cont.mem_usage[0]) + '\n')
