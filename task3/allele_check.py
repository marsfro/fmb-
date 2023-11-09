import argparse
import os
import pysam
import csv
import datetime

# Создать парсер аргументов командной строки
parser = argparse.ArgumentParser(description='Script for restoring reference alleles.')
parser.add_argument('-i', '--input', help='The SNP file.')
parser.add_argument('-o', '--output', help='The output file.')
parser.add_argument('-r', '--reference', help='The reference genome folder path.')
parser.add_argument('-l', '--log', help='The log file path.')

# Получить аргументы командной строки
args = parser.parse_args()
snp_file = args.input
output_file = args.output
reference_folder = args.reference
log_file = "log_file.txt"

# Создать лог файл
try:
    with open(log_file, "w") as f:
        f.write(f"Script execution started at: {datetime.datetime.now()}\n")
except Exception as e:
    print(f"An error occurred while creating the log file: {str(e)}")
    exit(1)

try:
    # Проверить существование входного файла
    if not os.path.isfile(snp_file):
        raise FileNotFoundError(f"Input file {snp_file} not found.")
    
    # Проверить формат конца строк входного файла
    with open(snp_file, "r") as file:
        first_line = file.readline()
        if not first_line.endswith(("\n", "\r\n")):
            raise ValueError("Invalid line ending format in the input file.")

    # Проверить заголовок входного файла
    with open(snp_file, "r") as file:
        csv_reader = csv.reader(file, delimiter="\t")
        header = next(csv_reader)
        if header != ['CHROM', 'POS', 'ID', 'allele1', 'allele2']:
            raise ValueError("Invalid input file header.")

    # Dictionary to store reference genomes
    reference_sequences = {}

    # Load reference genomes
    for chrom in range(1, 23):
        chromosome_file = os.path.join(reference_folder, f"chr{chrom}.fa")
        reference_sequences[f"chr{chrom}"] = pysam.Fastafile(chromosome_file)

    # Open snp_file and result_file in the same time
    with open(snp_file, "r") as file_in, open(output_file, "w", newline="") as file_out:
        csv_reader = csv.reader(file_in, delimiter="\t")
        next(csv_reader)  # Skip the header line
        csv_writer = csv.writer(file_out, delimiter="\t")
        csv_writer.writerow(["#CHROM", "POS", "ID", "REF", "ALT"])

        # Iterate over SNP rows
        for row in csv_reader:
            chrom = row[0]
            pos = int(row[1])
            ref_id = row[2]
            allele1 = row[3]
            allele2 = row[4]

            # Get the reference allele using pysam
            reference_genome = reference_sequences[chrom]
            ref_base = reference_genome.fetch(chrom, pos - 1, pos)

            # Determine the alternative allele
            if allele2 == allele1:
                alt_allele = allele1
            else:
                if ref_base == allele1:
                    alt_allele = allele2
                else:
                    alt_allele = allele1

            # Write the SNP information to the output file
            csv_writer.writerow([chrom, pos, ref_id, ref_base, alt_allele])

    with open(log_file, "a") as f:
        f.write(f"Script execution completed successfully at: {datetime.datetime.now()}\n")
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"An error occurred during script execution: {str(e)}\n")