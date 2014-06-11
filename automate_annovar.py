# Get a filename as an input
# Convert the vcf to an AnnoVar input file
# Run AnnoVar
# Parse and return the output

import sys
import os 
import subprocess
from ToolConfig import convert2annovar_script, table_annovar_script, annovar_db_folder, annovar_protocols, annovar_operation
import logging

def run_annovar(target_folder, target_vcf):
    outfile_name = target_vcf[:-4]
    convert_cmd = """perl %s --format vcf4 %s > %s.annoin""" % (convert2annovar_script, target_folder+target_vcf, target_folder+outfile_name)
    
    if "vcf4old" in convert_cmd:
        print "Careful! Annoin generation uses --format vcf4old flag!"
     
    subprocess.call(convert_cmd, shell=True, stdout = open("log_out.txt", "wa"), stderr = open("log_err.txt", "wa"))
    #print convert_cmd 
    
    annotate_cmd = """perl %s %s.annoin %s \
                   -buildver hg19 -out %s -remove \
                   -protocol %s -operation %s \
                   -nastring - """ % (table_annovar_script, target_folder+outfile_name, annovar_db_folder, target_folder+outfile_name, annovar_protocols, annovar_operation)
    
    logging.debug( annotate_cmd )
    subprocess.call(annotate_cmd, shell=True, stdout = open("log_out.txt", "wa"), stderr = open("log_err.txt", "wa"))
    
    annovar_output = target_folder + outfile_name + ".hg19_multianno.txt"
    
    return annovar_output 
    
##############################################################################################

if __name__ == '__main__':

    target_folder = os.getcwd() + "/"
    target_vcf = sys.argv[1]
    
    run_annovar(target_folder, target_vcf)